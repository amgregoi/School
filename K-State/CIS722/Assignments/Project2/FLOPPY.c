/* Andy Gregoire
 * CIS722 - Proj2
 * it does run
*/


/* change path to header file */
#include "/usr/src/drivers/floppy/floppy.h"


/*Our Ram Disk Definition */
#define RDISK			2
#define RSIZE			368640
#define RDENSITY		40
#define RSECTORS		9

/*our change to nr drives to account for our new ram disk: 2 to 3*/
#define NR_DRIVES          3	/* maximum number of drives */

/* our global vars */
PRIVATE phys_bytes rbase;
PRIVATE struct device rdevice;
PRIVATE int rseg;

/* our prototypes */
FORWARD _PROTOTYPE( void rf_init, (void)								);
FORWARD _PROTOTYPE( struct device*rf_prepare, (int device) 				);
FORWARD _PROTOTYPE( int rf_transfer, (int proc_nr, int opcode, off_t position, iovec_t *iov, unsigned nr_reg)		);
FORWARD _PROTOTYPE( int rf_do_open, (struct driver *dp, message *m_ptr) );
FORWARD _PROTOTYPE( void rf_gemoetry, (struct partition *entry)		);


/*===========================================================================*
 *				floppy_task				  								     *
 *===========================================================================*/
PUBLIC void main()
{
/* Initialize the floppy structure and the timers. */

  struct floppy *fp;
  int s;

  printf("---------------- Andys Ram Disk ---------------- \n");
  
  f_next_timeout = TMR_NEVER;
  tmr_inittimer(&f_tmr_timeout);

  for (fp = &floppy[0]; fp < &floppy[NR_DRIVES]; fp++) {
	fp->fl_curcyl = NO_CYL;
	fp->fl_density = NO_DENS;
	fp->fl_class = ~0;
	tmr_inittimer(&fp->fl_tmr_stop);
  }

  /* Set IRQ policy, only request notifications, do not automatically 
   * reenable interrupts. ID return on interrupt is the IRQ line number. 
   */
  irq_hook_id = FLOPPY_IRQ;
  if ((s=sys_irqsetpolicy(FLOPPY_IRQ, 0, &irq_hook_id )) != OK)
  	panic("FLOPPY", "Couldn't set IRQ policy", s);
  if ((s=sys_irqenable(&irq_hook_id)) != OK)
  	panic("FLOPPY", "Couldn't enable IRQs", s);

  /* our rf_init call to allocate memory */
  rf_init();
	
  driver_task(&f_dtab);
}

/*===========================================================================*
 *				rf_init				    									 *
 *===========================================================================*/
PRIVATE void rf_init()
{
  int s;

  if(allocmem(RSIZE, &rbase) < 0)
  {
    panic("MEMORY", "allocmem failed.", errno);
  }

  rdevice.dv_size = cvul64(RSIZE); /* cvul64 - converts an unsigned long */
  rdevice.dv_base = cvul64(&rbase);/* to a 64 bit number 		 */
  
  if(OK != (s=sys_segctl(&rseg, (u16_t *) &s, (vir_bytes *) &s, rbase, RSIZE)))
  	{
  	  panic("MEMORY", "Couldn't install remote segment.", s);
  	}
}


/*===========================================================================*
 *				f_prepare				  								     *
 *===========================================================================*/
PRIVATE struct device *f_prepare(device)
int device;
{
/* Prepare for I/O on a device. */

  f_device = device;
  f_drive = device & ~(DEV_TYPE_BITS | FORMAT_DEV_BIT);
  
  if (f_drive < 0 || f_drive >= NR_DRIVES) return(NIL_DEV);

  /* calls our rf_prepare if the device is ram disk */
  if(device == RDISK)
  {
  	return rf_prepare(device);
  }
  
  f_fp = &floppy[f_drive];
  f_dv = &f_fp->fl_geom;
  if (f_fp->fl_density < NT) {
	f_dp = &fdensity[f_fp->fl_density];
	f_sectors = f_dp->secpt;
	f_fp->fl_geom.dv_size = mul64u((long) (NR_HEADS * f_sectors
					* f_dp->cyls), SECTOR_SIZE);
  }

  /* A partition? */
  if ((device &= DEV_TYPE_BITS) >= MINOR_fd0p0)
	f_dv = &f_fp->fl_part[(device - MINOR_fd0p0) >> DEV_TYPE_SHIFT];

  return f_dv;
}


/*===========================================================================*
 *				rf_prepare				     								 *
 *===========================================================================*/
PRIVATE struct device *rf_prepare(device)
int device;
{
   f_dv = &rdevice;
   return f_dv;
}

/*===========================================================================*
 *				f_transfer				 								     *
 *===========================================================================*/
PRIVATE int f_transfer(proc_nr, opcode, position, iov, nr_req)
int proc_nr;			/* process doing the request */
int opcode;			/* DEV_GATHER or DEV_SCATTER */
off_t position;			/* offset on device to read or write */
iovec_t *iov;			/* pointer to read or write request vector */
unsigned nr_req;		/* length of request vector */
{
  struct floppy *fp = f_fp;
  iovec_t *iop, *iov_end = iov + nr_req;
  int s, r, errors;
  unsigned block;	/* Seen any 32M floppies lately? */
  unsigned nbytes, count, chunk, sector;
  unsigned long dv_size = cv64ul(f_dv->dv_size);
  vir_bytes user_addr;
  vir_bytes uaddrs[MAX_SECTORS], *up;
  u8_t cmd[3];

  /* calls our rf_transfer if ram disk */
  if(f_device == RDISK)
  {
  	return rf_transfer(proc_nr, opcode, position, iov, nr_req);
  }
  
  /* Check disk address. */
  if ((position & SECTOR_MASK) != 0) return(EINVAL);

  errors = 0;
  while (nr_req > 0) {
	/* How many bytes to transfer? */
	nbytes = 0;
	for (iop = iov; iop < iov_end; iop++) nbytes += iop->iov_size;

	/* Which block on disk and how close to EOF? */
	if (position >= dv_size) return(OK);		/* At EOF */
	if (position + nbytes > dv_size) nbytes = dv_size - position;
	block = div64u(add64ul(f_dv->dv_base, position), SECTOR_SIZE);

	if ((nbytes & SECTOR_MASK) != 0) return(EINVAL);

	/* Using a formatting device? */
	if (f_device & FORMAT_DEV_BIT) {
		if (opcode != DEV_SCATTER) return(EIO);
		if (iov->iov_size < SECTOR_SIZE + sizeof(fmt_param))
			return(EINVAL);

		if ((s=sys_datacopy(proc_nr, iov->iov_addr + SECTOR_SIZE,
			SELF, (vir_bytes) &fmt_param, 
			(phys_bytes) sizeof(fmt_param))) != OK)
			panic("FLOPPY", "Sys_vircopy failed", s);

		/* Check that the number of sectors in the data is reasonable,
		 * to avoid division by 0.  Leave checking of other data to
		 * the FDC.
		 */
		if (fmt_param.sectors_per_cylinder == 0) return(EIO);

		/* Only the first sector of the parameters now needed. */
		iov->iov_size = nbytes = SECTOR_SIZE;
	}

	/* Only try one sector if there were errors. */
	if (errors > 0) nbytes = SECTOR_SIZE;

	/* Compute cylinder and head of the track to access. */
	fp->fl_cylinder = block / (NR_HEADS * f_sectors);
	fp->fl_hardcyl = fp->fl_cylinder * f_dp->steps;
	fp->fl_head = (block % (NR_HEADS * f_sectors)) / f_sectors;

	/* For each sector on this track compute the user address it is to
	 * go or to come from.
	 */
	for (up = uaddrs; up < uaddrs + MAX_SECTORS; up++) *up = 0;
	count = 0;
	iop = iov;
	sector = block % f_sectors;
	for (;;) {
		user_addr = iop->iov_addr;
		chunk = iop->iov_size;
		if ((chunk & SECTOR_MASK) != 0) return(EINVAL);

		while (chunk > 0) {
			uaddrs[sector++] = user_addr;
			chunk -= SECTOR_SIZE;
			user_addr += SECTOR_SIZE;
			count += SECTOR_SIZE;
			if (sector == f_sectors || count == nbytes)
				goto track_set_up;
		}
		iop++;
	}
  track_set_up:

	/* First check to see if a reset is needed. */
	if (need_reset) f_reset();

	/* See if motor is running; if not, turn it on and wait. */
	start_motor();

	/* Set the stepping rate and data rate */
	if (f_dp != prev_dp) {
		cmd[0] = FDC_SPECIFY;
		cmd[1] = f_dp->spec1;
		cmd[2] = SPEC2;
		(void) fdc_command(cmd, 3);
		if ((s=sys_outb(FDC_RATE, f_dp->rate)) != OK)
			panic("FLOPPY","Sys_outb failed", s);
		prev_dp = f_dp;
	}

	/* If we are going to a new cylinder, perform a seek. */
	r = seek();

	/* Avoid read_id() if we don't plan to read much. */
	if (fp->fl_sector == NO_SECTOR && count < (6 * SECTOR_SIZE))
		fp->fl_sector = 0;

	for (nbytes = 0; nbytes < count; nbytes += SECTOR_SIZE) {
		if (fp->fl_sector == NO_SECTOR) {
			/* Find out what the current sector is.  This often
			 * fails right after a seek, so try it twice.
			 */
			if (r == OK && read_id() != OK) r = read_id();
		}

		/* Look for the next job in uaddrs[] */
		if (r == OK) {
			for (;;) {
				if (fp->fl_sector >= f_sectors)
					fp->fl_sector = 0;

				up = &uaddrs[fp->fl_sector];
				if (*up != 0) break;
				fp->fl_sector++;
			}
		}

		if (r == OK && opcode == DEV_SCATTER) {
			/* Copy the user bytes to the DMA buffer. */
			if ((s=sys_datacopy(proc_nr, *up,  SELF, 
				(vir_bytes) tmp_buf,
				(phys_bytes) SECTOR_SIZE)) != OK)
			panic("FLOPPY", "Sys_vircopy failed", s);
		}

		/* Set up the DMA chip and perform the transfer. */
		if (r == OK) {
			if (dma_setup(opcode) != OK) {
				/* This can only fail for addresses above 16MB
				 * that cannot be handled by the controller, 
 				 * because it uses 24-bit addressing.
				 */
				return(EIO);
			}
			r = fdc_transfer(opcode);
		}

		if (r == OK && opcode == DEV_GATHER) {
			/* Copy the DMA buffer to user space. */
			if ((s=sys_datacopy(SELF, (vir_bytes) tmp_buf, 
				proc_nr, *up, 
				(phys_bytes) SECTOR_SIZE)) != OK)
			panic("FLOPPY", "Sys_vircopy failed", s);
		}

		if (r != OK) {
			/* Don't retry if write protected or too many errors. */
			if (err_no_retry(r) || ++errors == MAX_ERRORS) {
				return(EIO);
			}

			/* Recalibrate if halfway. */
			if (errors == MAX_ERRORS / 2)
				fp->fl_calibration = UNCALIBRATED;

			nbytes = 0;
			break;		/* retry */
		}
	}

	/* Book the bytes successfully transferred. */
	position += nbytes;
	for (;;) {
		if (nbytes < iov->iov_size) {
			/* Not done with this one yet. */
			iov->iov_addr += nbytes;
			iov->iov_size -= nbytes;
			break;
		}
		nbytes -= iov->iov_size;
		iov->iov_addr += iov->iov_size;
		iov->iov_size = 0;
		if (nbytes == 0) {
			/* The rest is optional, so we return to give FS a
			 * chance to think it over.
			 */
			return(OK);
		}
		iov++;
		nr_req--;
	}
  }
  return(OK);
}

/*===========================================================================*
 *				rf_transfer				 								     *
 *===========================================================================*/
PRIVATE int rf_transfer(proc_nr, opcode, position, iov, nr_req)
int proc_nr;			/* process doing the request */
int opcode;				/* DEV_GATHER or DEV_SCATTER */
off_t position;			/* offset on device to read or write */
iovec_t *iov;			/* pointer to read or write request vector */
unsigned nr_req;		/* length of request vector */
{
  int seg;
  unsigned count;
  vir_bytes user_vir;
  struct device *dev;
  unsigned long dv_size;
  
  dev = &rdevice;
  dv_size = cv64ul(dev->dv_size); 	/* cv64ul - converts 64bit number to an unsigned */
  seg = RDISK;			  			/* long if it fits, otherwise returns ULONG_MAX  */

  while(nr_req > 0)
  {
    
    count = iov->iov_size;										/* amount */
    user_vir = iov->iov_addr;									/* location */

	
    if(position >= dv_size) return(OK);							/* EOF */
    if(position + count > dv_size) count = dv_size - position;
	
	/* sys_vircopy function parameters from minix3 wiki */
	/* int sys_vircopy(endpoint_t src_proc, vir_bytes src_vir, endpoint_t dst_proc, vir_bytes dst_vir, phys_bytes bytes); */
    if(opcode == DEV_GATHER)
      sys_vircopy(SELF, rseg, position, proc_nr, D, user_vir, count);
    else
      sys_vircopy(proc_nr, D, user_vir, SELF, rseg, position, count);
	  
    position += count;		/* increments position */
    iov->iov_addr += count; /* increments address location */
    if((iov->iov_size -= count) == 0) 
	{
		iov++; 
		nr_req--;
	}
  }
  return(OK);
}

/*===========================================================================*
 *				f_do_open				   									 *
 *===========================================================================*/
PRIVATE int f_do_open(dp, m_ptr)
struct driver *dp;
message *m_ptr;			/* pointer to open message */
{
/* Handle an open on a floppy.  Determine diskette type if need be. */

  int dtype;
  struct test_order *top;

  /* our call to rf_do_open if ram disk */
  if(m_ptr->DEVICE == RDISK)
  {
	return rf_do_open(dp, m_ptr);
  }
  
  /* Decode the message parameters. */
  if (f_prepare(m_ptr->DEVICE) == NIL_DEV) return(ENXIO);

  dtype = f_device & DEV_TYPE_BITS;	/* get density from minor dev */
  if (dtype >= MINOR_fd0p0) dtype = 0;

  if (dtype != 0) {
	/* All types except 0 indicate a specific drive/medium combination.*/
	dtype = (dtype >> DEV_TYPE_SHIFT) - 1;
	if (dtype >= NT) return(ENXIO);
	f_fp->fl_density = dtype;
	(void) f_prepare(f_device);	/* Recompute parameters. */
	return(OK);
  }
  if (f_device & FORMAT_DEV_BIT) return(EIO);	/* Can't format /dev/fdN */

  /* The device opened is /dev/fdN.  Experimentally determine drive/medium.
   * First check fl_density.  If it is not NO_DENS, the drive has been used
   * before and the value of fl_density tells what was found last time. Try
   * that first.  If the motor is still running then assume nothing changed.
   */
  if (f_fp->fl_density != NO_DENS) {
	if (motor_status & (1 << f_drive)) return(OK);
	if (test_read(f_fp->fl_density) == OK) return(OK);
  }

  /* Either drive type is unknown or a different diskette is now present.
   * Use test_order to try them one by one.
   */
  for (top = &test_order[0]; top < &test_order[NT-1]; top++) {
	dtype = top->t_density;

	/* Skip densities that have been proven to be impossible */
	if (!(f_fp->fl_class & (1 << dtype))) continue;

	if (test_read(dtype) == OK) {
		/* The test succeeded, use this knowledge to limit the
		 * drive class to match the density just read.
		 */
		f_fp->fl_class &= top->t_class;
		return(OK);
	}
	/* Test failed, wrong density or did it time out? */
	if (f_busy == BSY_WAKEN) break;
  }
  f_fp->fl_density = NO_DENS;
  return(EIO);			/* nothing worked */
}


/*===========================================================================*
 *				rf_do_open				    								 *
 *===========================================================================*/
PRIVATE int rf_do_open(dp, m_ptr)
struct driver *dp;
message *m_ptr;			/* pointer to open message */
{
   return(OK);
}

/*===========================================================================*
 *				f_geometry				   									 *
 *===========================================================================*/
PRIVATE void f_geometry(entry)
struct partition *entry;
{
	/* our call to rf_geometry if ram disk */
	if(f_device == RDISK)
	{
		rf_geometry(entry);
		return; /* returns so we dont reset values below */
	}

  entry->cylinders = f_dp->cyls;
  entry->heads = NR_HEADS;
  entry->sectors = f_sectors;
}

/*===========================================================================*
 *				rf_geometry				    								 *
 *===========================================================================*/
PRIVATE void rf_geometry(entry)
struct partition *entry;
{
  entry->cylinders = RDENSITY;						/* num tracks / side 	*/
  entry->heads = NR_HEADS; 							/* num heads (2) 		*/
  entry->sectors = RSECTORS;						/* num sectors / track  */
}


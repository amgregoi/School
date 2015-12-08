#include <lib.h>
#include <unistd.h>
#include "../servers/pm/semaphore.h"
#include "semlib.h"

PUBLIC int init_sem(void)
{
  message m;

  m.op = INIT;
  return(_syscall(MM, SEMOP, &m));
}

PUBLIC int create_sem(int key, int initial_val)
{
  message m;

  m.op = CREATE;
  m.keyval = key;
  m.ival = initial_val;
  return(_syscall(MM, SEMOP, &m));
}

PUBLIC int p(int sem_desc)
{
 message m;

 m.op = P;
 m.desc = sem_desc;
 return(_syscall(MM, SEMOP, &m));
}

PUBLIC int v(int sem_desc)
{
 message m;

 m.op = V;
 m.desc = sem_desc;
 return(_syscall(MM, SEMOP, &m));
}

PUBLIC int delete_sem(int sem_desc)
{
 message m;

 m.op = DELETE;
 m.desc = sem_desc;
 return(_syscall(MM, SEMOP, &m));
}


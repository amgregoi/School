TITLE Keyboard Toggle Keys             (Keybd.asm)


INCLUDE Irvine32.inc
INCLUDE Macros.inc
;#######################################  Both Elevators Closed Pic  #######################################
mPic0 MACRO
	call crlf
	mwrite "           *****			    *****"
	call crlf
	mwrite "           *****			    *****"
	call crlf
	mwrite "           *****			    *****"
	call crlf  
	mwrite "           *****			    *****"
	call crlf
ENDM

;#######################################  Elevator 1 open, Elevator 2 closed pic  #######################################
mpic1 MACRO
	call crlf
	mwrite "           *****			    *****"
	call crlf
	mwrite "           *   *			    *****"
	call crlf
	mwrite "           *   *			    *****"
	call crlf  
	mwrite "           *****			    *****"
	call crlf
ENDM

;#######################################  Elevator 1 closed, Elevator 1 Open pic  #######################################
mPic2 MACRO
	call crlf
	mwrite "           *****			    *****"
	call crlf
	mwrite "           *****			    *   *"
	call crlf
	mwrite "           *****			    *   *"
	call crlf  
	mwrite "           *****			    *****"
	call crlf
ENDM

;#######################################  Both Elevators Open pic #######################################
mPic3 MACRO
	call crlf
	mwrite "           *****			    *****"
	call crlf
	mwrite "           *   *			    *   *"
	call crlf
	mwrite "           *   *			    *   *"
	call crlf  
	mwrite "           *****			    *****"
	call crlf
ENDM
;#######################################  ALARM  #######################################
mAlarm MACRO
	push eax
	mtest
	mpic0
	mwrite "		Elevator going to bottom floor"
	mov eax, 4000
	call Delay
	call clrscr
	mtest
	mov eax, 07h
	call writechar
	mpic3
	call crlf
ENDM

;#######################################  Door Operations for Elevator 1  #######################################
mDoor MACRO
	push eax
	mtest
	mpic0
	mwrite "	Opening Door"
	mov eax, 07h
	call writechar
	mov eax, 2000
	call Delay
	call clrscr
	mtest
	mpic1
	mwrite "	 Door Open"
	mov eax, 1000
	call Delay
	call clrscr
	mtest
	mpic0
	mwrite "	Closing Door"	
	mov eax, 2000
	call Delay
	pop eax
	
	
ENDM

;#######################################  kDoor Operations for Elevator 2  #######################################
mDoor2 MACRO
	push eax
	mtest
	mpic0
	mwrite "					Opening Door"
	mov eax, 07h
	call writechar
	mov eax, 2000
	call Delay
	call clrscr
	mtest
	mpic2
	mwrite "					Door Open"
	mov eax, 1000
	call Delay
	call clrscr
	mtest
	mpic0
	mwrite "					Closing Door"	
	mov eax, 2000
	call Delay
	pop eax
	
ENDM

;#######################################  Elevator1 Motion Operation   #######################################
mInternalDoor MACRO
	call clrscr
	push eax
	mtest
	mpic0
	mwrite "     Elevator in Motion"
	mov eax, 4000
	call Delay
	call clrscr
	mtest
	mpic1
	mwrite "	Door Opening"
	mov eax, 07h
	call writechar
	mov eax, 3000
	call Delay
	call clrscr
	mtest
	mpic0
	mwrite "	Door Closing"	
	mov eax, 4000
	call Delay
	pop eax
	mpic0
ENDM

;#######################################  Elevator2 Motion Operation  #######################################
mInternalDoor2 MACRO
	call clrscr
	push eax
	mtest
	mpic0
	mwrite "					 Elevator in Motion"
	mov eax, 4000
	call Delay
	call clrscr
	mtest
	mpic2
	mwrite "					Door Opening"
	mov eax, 07h
	call writechar
	mov eax, 3000
	call Delay
	call clrscr
	mtest
	mpic0
	mwrite "					Door Closing"	
	mov eax, 4000
	call Delay
	pop eax
	mpic0
ENDM

;#######################################  Internal/External Display Board Options  #######################################
mMenu MACRO

	mwrite "						   ~~~~ Options ~~~~"
	call crlf
	mwrite "					0: Down			9: Up"
	call crlf
	mwrite "					L: Exit Elevator	d: Bypass Key "
	call crlf
	mwrite "					s: Alarm		f: Fire Alarm "
	call crlf
	mwrite "					g: Open Door		h: Close Door "
	call crlf
	mwrite "					b: Emergency Telephone "
	mwrite "									  ~~~~Elevator 1~~~~"
	call crlf
	mwrite "					1: First Floor		5: Fifth Floor"
	call crlf
	mwrite "					2: Second Floor		6: Sixth Floor"
	call crlf
	mwrite "					3: Third Floor		7: Seventh Floor"
	
	mwrite	"					4: Fourth floor		8: Eighth Floor"
	call crlf
	mwrite "						  ~~~~Elevator 2~~~~"
	call crlf
	mwrite "					q: First Floor		t: Fifth Floor"
	call crlf
	mwrite "					w: Second Floor		y: Sixth Floor"
	call crlf
	mwrite "					e: Third Floor		u: Seventh Floor"
	mwrite	"					r: Fourth floor		i: Eighth Floor"
	call crlf
	call crlf
ENDM 

;#######################################  Elevator Floor Log  #######################################
mtest MACRO
	mMenu
	mwrite "   Elevator 1: Floor "
		mov eax, Elevator1
		call writedec
		mwrite "              Elevator 2: Floor "
		mov eax, Elevator2
		call writedec
ENDM


.data
Elevator1 SDWORD ?
Elevator2 SDWORD ?
.code
program:

	call clrscr
	mov Elevator1, 1
	mov Elevator2, 1
		

;#######################################  Choose which Elevator to use  #######################################
		Chfloor:
				call clrscr
				mtest
				mpic0
				call crlf
				mwrite "Enter the floor level you are on (1 - 8)"		;this chooses which Elevator is closest and uses it
				call crlf												;Dependent on which floor the elevators is currently on
				call readchar											;this is always brought up after leaving the elevator 'L'

				cmp eax, 561
				je one
				cmp eax, 818
				je two
				cmp eax, 1075											;Converts readchar values to decimal values
				je three												;Used for permitting setting off alarms outside of elevator
				cmp eax, 1332											
				je four
				cmp eax, 1589
				je five
				cmp eax, 1846
				je six
				cmp eax, 2103
				je seven
				cmp eax, 2360
				je eight
				cmp eax, 8051
				cmp eax, 8051
				je Alarm				; Alarm
				cmp eax, 8292
				je Bypass				; Bypass Key
				cmp eax, 8550
				je Fire					; Fire Alarm
				cmp eax, 2864
				je zero
				cmp eax, 2617
				je nine


			zero:
				mov eax, 0
				jmp done
			one:
				mov eax, 1
				jmp done
			two:
				mov eax, 2
				jmp done
			three:
				mov eax, 3
				jmp done
			four:
				mov eax, 4
				jmp done
			five:
				mov eax, 5
				jmp done
			six:
				mov eax, 6
				jmp done
			seven:
				mov eax, 7
				jmp done
			eight:
				mov eax, 8
				jmp done
			nine:
				mov eax, 9
				jmp done

	done:

				mov ebx, eax
				cmp eax, 0
				je Chfloor
				cmp eax, 8
				jg Chfloor



		Choose:
				cmp Elevator1, ebx
				je menu
				cmp Elevator2, ebx
				je menu2
				cmp Elevator1, ebx
				jl L1
				jmp L2
		
				L1:
					mov ecx, ebx
					sub ecx, Elevator1
					jmp done1
				L2:
					mov ecx, Elevator1
					sub ecx, ebx
					jmp done1
				done1:
				cmp Elevator2, ebx
				jl L3
				jmp L4

				L3:
					mov edx, ebx
					sub edx, Elevator2
					jmp done2
				L4:
					mov edx, Elevator2
					sub edx, ebx
					jmp done2

				done2:

				cmp ecx, edx
					jg Menu2			;Elevator2 Menu
				cmp ecx, edx
					jle Menu			;Elevator1 Menu
				jmp Choose
;#######################################  End - Choose which Elevator to use  #######################################

;#######################################  Elevator1 Options (up, down, alarm, etc..)  #######################################
		Menu:
				call clrscr
				mtest
				mpic0
				mwrite " Enter Direction ( Up or Down)"
				call crlf
				call readchar
				cmp eax, 2617
				je Doorx
				cmp eax, 2864
				je Doorx
				cmp eax, 8051
				je Alarm				; Alarm
				cmp eax, 8292
				je Bypass				;Bypass Key
				cmp eax, 8550
				je Fire					;Fire Alarm
				jmp Exits
;#######################################  End - Elevator1 Options (up, down, alarm, etc..)  #######################################

;#######################################  Elevator2 Options (up, down, alarm, etc..)  #######################################
		Menu2:
				call clrscr
				mtest
				mpic0
				mwrite " Enter Direction ( Up or Down)"
				call crlf
				call readchar
				cmp eax, 2617
				je Doory
				cmp eax, 2864
				je Doory
				cmp eax, 8051
				je Alarm				; Alarm
				cmp eax, 8292
				je Bypass				; Bypass Key
				cmp eax, 8550
				je Fire					;Fire Alarm
				jmp Exitt
;#######################################  End - Elevator2 Options (up, down, alarm, etc..)  #######################################

;#######################################  Elevator1 Input (Inside)  #######################################
		Doorx:
				mov Elevator1, ebx
				mInternalDoor

		Internal:
				call clrscr
				mtest
				mpic0
				mwrite "Enter Desired Floor (Elevator 1) "			
				call crlf
				call readchar
				cmp eax, 561
				je floor1
				cmp eax, 818
				je floor2
				cmp eax, 1075
				je floor3
				cmp eax, 1332
				je floor4
				cmp eax, 1589
				je floor11
				cmp eax, 1846
				je floor12
				cmp eax, 2103
				je floor13
				cmp eax, 2360
				je floor14
				cmp eax, 8051
				je Alarm
				cmp eax, 8292
				je Bypass
				cmp eax, 8550
				je Fire
				cmp eax, 9836
				je Chfloor
				cmp eax, 8807
				je Open1
				cmp eax, 12386
				je ETelephone
				jmp Internal
;#######################################  End - Elevator1 Input (Inside)  #######################################
		
;#######################################  Elevator2 Input (Inside)  #######################################

		Doory:
				mov Elevator2, ebx
				mInternalDoor2
		Internal2:
				call clrscr
				mtest
				mpic0
				mwrite "Enter Desired Floor (Elevator 2) "
				call crlf
				call readchar
				cmp eax, 4209
				je floor5
				cmp eax, 4471
				je floor6
				cmp eax, 4709
				je floor7
				cmp eax, 4978
				je floor8
				cmp eax, 5236
				je floor15
				cmp eax, 5497
				je floor16
				cmp eax, 5749
				je floor17
				cmp eax, 5993
				je floor18
				cmp eax, 8051
				je Alarm
				cmp eax, 8292
				je Bypass
				cmp eax, 8550
				je Fire
				cmp eax, 9836
				je Chfloor
				cmp eax, 8807
				je Open2
				cmp eax, 12386
				je ETelephone2
				jmp Internal2		
;#######################################  End - Elevator2 Input (Inside)  #######################################

		
;#######################################  Eelvator 1 Floors #######################################
		floor1:							;Floor1
				mov Elevator1, 1
				call clrscr
				mtest
				mpic0
				mInternalDoor
				call Clrscr
				mtest
				mPic0
				jmp Internal

		floor2:							;Floor2
				mov Elevator1, 2
				call clrscr
				mMenu
				mInternalDoor
				call Clrscr
				mtest
				mPic0
				jmp Internal

		floor3:							;Floor3
				mov Elevator1, 3
				call clrscr
				mMenu
				mInternalDoor
				call Clrscr
				mtest
				mPic0
				jmp Internal

		floor4:							;Floor4
				mov Elevator1, 4
				call clrscr
				mtest
				mInternalDoor
				call Clrscr
				mMenu
				mPic0
				jmp Internal

		floor11:						;Floor5
				mov Elevator1, 5
				call clrscr
				mtest
				mpic0
				mInternalDoor
				call Clrscr
				mtest
				call writedec
				mPic0
				jmp Internal

		floor12:						;Floor6
				mov Elevator1, 6
				call clrscr
				mMenu
				mInternalDoor
				call Clrscr
				mtest
				mPic0
				jmp Internal

		floor13:						;Floor7
				mov Elevator1, 7
				call clrscr
				mMenu
				mInternalDoor
				call Clrscr
				mtest
				mPic0
				jmp Internal

		floor14:						;Floor8
				mov Elevator1, 8
				call clrscr
				mtest
				mInternalDoor
				call Clrscr
				mMenu
				mPic0
				jmp Internal

		Open1:
				call Clrscr
				mtest
				mpic0
				mov eax, 1000
				call delay
			point1:
				call clrscr
				mtest
				mpic1
				mwrite "Elevator Open: h to close elevator"
				call crlf
				call readchar
				cmp eax, 9064
				je Internal
				jmp point1

		ETelephone:
				call Clrscr
				mtest
				mpic0
				mwrite "What is your Emergency? "
				call crlf
				call readdec
				call crlf
				mwrite " Help is on the way! "
				mov eax, 2000
				call delay
				jmp Internal
;####################################### End -  Elevator 1 Floors #######################################


	
;#######################################  Elevator 2 Floors #######################################
		floor5:							; Floor 1
				mov Elevator2, 1
				call clrscr
				mtest
				mpic0
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2

		floor6:							; Floor 2
				mov Elevator2, 2
				call clrscr
				mMenu
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2

		floor7:							; Floor 3
				mov Elevator2, 3
				call clrscr
				mMenu
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2

		floor8:							; Floor 4
				mov Elevator2, 4
				call clrscr
				mMenu
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2

		floor15:						; Floor 5
				mov Elevator2, 5
				call clrscr
				mtest
				mpic0
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2

		floor16:						; Floor 6
				mov Elevator2, 6
				call clrscr
				mMenu
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2

		floor17:						; Floor 7
				mov Elevator2, 7
				call clrscr
				mMenu
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2

		floor18:						; Floor 8
				mov Elevator2, 8
				call clrscr
				mMenu
				mInternalDoor2
				call Clrscr
				mtest
				mPic0
				jmp Internal2
		Open2:
				call Clrscr
				mtest
				mpic0
				mov eax, 1000
				call delay
			point2:
				call clrscr
				mtest
				mpic2
				mwrite "Elevator Open: h to close elevator"
				call crlf
				call readchar
				cmp eax, 9064
				je Internal2
				jmp point2
		ETelephone2:
				call Clrscr
				mtest
				mpic0
				mwrite "What is your Emergency? "
				call crlf
				call readdec
				call crlf
				mwrite " Help is on the way! "
				mov eax, 2000
				call delay
				jmp Internal2
;#######################################  End - Elevator 2 Floors #######################################


		Exits:
				call Clrscr
				jmp menu
		Exitt:
				call Clrscr
				jmp menu2

;#######################################  Alarm #######################################
		Alarm:
				mov Elevator1, 1
				mov Elevator2, 1
				call clrscr
				mAlarm

				mwrite " Alarm Activated: 'S' to deactivate "
				call crlf
				call readchar
				cmp eax, 8051
				je program
				jmp Alarm
;#######################################  End - Alarm #######################################

;#######################################  Fire #######################################
		Fire: 
				mov Elevator1, 1
				mov Elevator2, 1
				call clrscr
				mAlarm
				mwrite "Fire Alarm Activated: 'f' to deactive "
				call crlf
				call readchar
				cmp eax, 8550
				je program
				jmp Fire
;#######################################  End - Fire #######################################

;#######################################  Bypass Key #######################################
		Bypass: 
				mov Elevator1, 1
				mov Elevator2, 1
				call clrscr
				mAlarm
				mwrite "Bypass Key Activated: 'd' to deactive "
				call crlf
				call readchar
				cmp eax, 8292
				je program
				jmp Bypass
;#######################################  End - Bypass Key #######################################

   
end program





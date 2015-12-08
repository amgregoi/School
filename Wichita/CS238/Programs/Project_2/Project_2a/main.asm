TITLE MASM Template						(main.asm)

; Description:
; Project 2A - Factorial 
; Revision date:

INCLUDE Irvine32.inc
.data
	Input1 WORD ?
	string BYTE "Enter Decimal Number: ",0
	string1 BYTE "This Program will take the Factorial of a User Given Number ",0
	Product DWORD ?
	Count WORD ?


.code
main PROC

	mov edx, OFFSET string1
	call WriteString
	call Crlf

	mov edx, OFFSET string
	call WriteString

	call ReadDec
	mov Input1, ax
	mov bx, 0
	mov cx, Input1
	mov count, cx

L1:
	add bx, Input1
	loop L1
sub bx, Input1

L2: 
	mov dx, bx
	mov bx, 0
	mov Input1, dx
	dec count
	mov cx, count
	cmp count, 1
	jg L1


mov ax, dx
mov Product, eax
call WriteDec


call DumpRegs
	
main ENDP

END main
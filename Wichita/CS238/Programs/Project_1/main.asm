TITLE MASM Template						(main.asm)

; Description:
; 
; Revision date:

INCLUDE Irvine32.inc
.data
	Input1 WORD ?
	Input2 WORD ?
	Product DWORD ?
	String1 BYTE "This Program will Multiply Two Inputed Numbers ",0
	String2 BYTE "Enter First Number: ",0
	String3 BYTE "Enter Second number: ",0


.code
main PROC

	mov edx, OFFSET String1
	call WriteString
	call Crlf

	mov edx, OFFSET String2
	call WriteString
	call ReadDec
	
	mov Input1, ax
	mov bx, 0

	mov edx, OFFSET String3
	call WriteString
	call ReadDec
	mov Input2, ax
	mov cx, Input2

	mov ax, 0
	


L1:
	add bx, Input1
	loop L1

mov ax, bx
mov Product, eax
call WriteDec

	
main ENDP

END main
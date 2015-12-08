TITLE MASM Template						(main.asm)

; Description:
; 
; Revision date:

INCLUDE Irvine32.inc
.data
	Input1 WORD ?
	Input2 WORD ?
	Product DWORD ?
	string1 BYTE "Enter first number (Smaller): ",0
	string2 BYTE "Enter second number (Larger): ",0
	string3 BYTE "____Fibonacci Series____",0
	string4 BYTE "This Program will create a Fibonacci Series based on two inputed numbers",0


.code
main PROC

	mov edx, OFFSET string4
	call WriteString
	call Crlf

	mov edx, OFFSET string1
	call WriteString
	call ReadDec
	mov Input1, ax
	mov bx, 0

	mov edx, OFFSET string2
	call WriteString
	call ReadDec
	mov Input2, ax
	mov cx, 8

	mov edx, OFFSET string3
	call WriteString
	call Crlf
	
	mov ax, Input1
	call WriteDec
	call Crlf
	mov ax, Input2
	call WriteDec
	call Crlf	


L1:
	add ax, Input1
	mov bx, ax
	call WriteDec
	call Crlf
	sub bx, Input1
	mov Input1, bx
	loop L1

main ENDP

END main
TITLE MASM Template						(main.asm)

; Description:
; 
; Revision date:

INCLUDE Irvine32.inc
.data


Input DWORD ?
Evenn DWORD 15 DUP(?)
Count1 DWORD ?
Count2 DWORD ?
Odd DWORD 15 DUP(?)
myMessage BYTE "MASM program example",0dh,0ah,0
string BYTE "This Program Will sort Inputed Numbers as Even or Odd  ",0
string0 BYTE "Printing Even Array:  ",0
string1 BYTE "Printing Odd Array ",0
string2 BYTE "Enter Value to be sorted: Enter 'Zero (0)' to exit ",0
string3 BYTE "********************************************************* ",0
string4 BYTE ", ",0
string5 BYTE "Note: Arrays with no values inserted are represented with a zero (0) ",0

.code
main PROC
	mov edx, OFFSET string
	call WriteString
	call Crlf

	mov esi, OFFSET Evenn-4
	mov edi, OFFSET Odd-4

	mov ebx, 0
	mov ecx, 0
	mov Count1, 0
	mov Count2, -1
	

L1:
		mov edx, OFFSET string2
		call WriteString
		call Crlf
		call ReadDec
		
		mov ebx, eax
		cmp eax, 0
		je L9
		cmp eax, 1
		je L3
		
L10:
		sub ebx, 2
		cmp ebx, 0
		jg L10

		cmp ebx, 0
		je L2
		jmp L3



L2:
		call Crlf
		call Crlf
		add Count1, 1
		add esi, 4
		mov [esi], eax
		jmp L1
L3:
		call Crlf
		call Crlf
		add Count2, 1
		add edi, 4
		mov [edi], eax
		jmp L1
L9:
		call Crlf
		mov edx, OFFSET string3
		call WriteString
		call Crlf
		mov edx, OFFSET string0
		call WriteString
		mov ecx, 1
		mov esi, OFFSET Evenn-4
		

L4:
		add esi, 4
		mov eax, [esi]
		call WriteDec
		mov edx, OFFSET string4
		call WriteString
		sub Count1, 1
		cmp Count1, 0
		jg L4
		 
call Crlf
mov ecx, 0
call Crlf
mov edx, OFFSET string1
call WriteString
mov edi, OFFSET Odd-4
L5:
		add edi, 4
		mov eax, [edi]
		call WriteDec
		mov edx, OFFSET string4
		call WriteString
		sub Count2, 1
		cmp Count2, 0
		jge L5

call Crlf
mov edx, OFFSET string3
call WriteString
call Crlf
mov edx, OFFSET string5
call WriteString
call Crlf
	
call ReadDec		; keep cmd open
		
	exit
main ENDP

END main
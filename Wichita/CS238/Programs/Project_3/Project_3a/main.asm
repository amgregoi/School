TITLE MASM Template						(main.asm)

; Description:
; 
; Revision date:

INCLUDE Irvine32.inc
.data
Input1 DWORD ?
Input2 DWORD ?
Count DWORD ?
Temp DWORD ?
Temp1 DWORD ?
Temp2 DWORD ?
Answer DWORD ?
string BYTE "Enter Decimal Number for n: ",0
string1 BYTE "Enter Decimal Number for r: ",0
string2 BYTE "This Program will find the Permutation of 2 inputed numbers: P(n,r) ",0
.code
;
main Proc
;
	mov edx, OFFSET string2
	call WriteString
	call Crlf

	mov edx, OFFSET string
	call WriteString
	call ReadDec
	mov Input1, eax
	mov Temp1, eax

	mov edx, OFFSET string1
	call WriteString
	call ReadDec
	mov Input2, eax
	

	sub Temp1, eax
	

;
fact proc
;

	mov ebx, 0
	mov ecx, Input1
	mov count, ecx

L1:
	add ebx, Input1
	loop L1
sub ebx, Input1

L2: 
	mov edx, ebx
	mov ebx, 0
	mov Input1, edx
	dec count
	mov ecx, count
	cmp count, 1
	jg L1

	mov Temp, edx

	mov ebx, 0
	mov ecx, Temp1
	mov count, ecx
	mov Temp2, ecx


L3:
	add ebx, Temp1
	dec ecx
	cmp ecx, 1
	jg L3

L4: 
	mov edx, ebx
	mov ebx, 0
	mov Temp1, edx
	dec count
	mov ecx, count
	cmp count, 1
	jg L3

;
myDiv proc
;

mov count, 0
L1:
	sub Temp, edx
	inc count
	cmp Temp, 1
	jg L1

mov ebx, Temp2
cmp ebx, 1
jne Equal
jmp Random

Random: 
	inc count

Equal:
	
mov eax, count
mov Answer, eax
call WriteDec
call Crlf

myDiv Endp
fact Endp
main Endp
End main
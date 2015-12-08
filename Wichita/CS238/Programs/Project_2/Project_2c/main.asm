TITLE MASM Template						(main.asm)

; Description:
; 
; Revision date:

INCLUDE Irvine32.inc
.data
Input DWORD 0Fh, 3Fh, 9Fh, 0BFh, 0FFh
.code
main Proc
Mov cx, 02h
Mov esi, 00h
L1: 
	Mov eax, [input+esi]
	Call SetTextColor
	Call Randomize
	Inc esi
	Inc esi
	Inc esi
	Inc esi
	Loop l1
main Endp
End main
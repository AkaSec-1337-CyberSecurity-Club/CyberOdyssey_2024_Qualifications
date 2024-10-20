bits 16:
section .boot;
global boot;

%define NULL_SEG 0
%define CODE_SEG 0x8
%define DATA_SEG 0x10
%define RCODE_SEG 0x18
%define RDATA_SEG 0x20

boot:
	mov	ah, 0x00;			Function: Set video mode
	mov	al, 0x03;			Mode: 80x25 text mode (mode 3 dzeb)
	int	0x10;				Call BIOS interrupt
	call	load_step1_5;			loading the second step from the second sector
	call	load_gdt;
	; pivoting to protected_mode
	cli;
	mov	eax, cr0;
	or	eax, 1;
	mov	cr0, eax;
	mov	ax, DATA_SEG
	jmp	CODE_SEG:kload;


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; GDT ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
gdt_data: 
	dd 0
	dd 0

;gdt_code:
	dw 0xFFFF
	dw 0
	db 0
	db 10011010b
	db 11001111b
	db 0

;gdt_data:
	dw 0xFFFF
	dw 0
	db 0
	db 10010010b
	db 11001111b
	db 0

; rmode gdt
; gdt code
	dw 0xFFFF
	dw 0
	db 0
	db 0x9e
	db 0
	db 0

; gdt data:
	dw 0xFFFF
	dw 0
	db 0
	db 0x92
	db 0
	db 0
gdt_end:

gdt_ptr: 
	dw gdt_end - gdt_data - 1;
	dd gdt_data
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

load_step1_5: 
	mov ah, 0x2;
	mov al, 0x3;			we just wanna read 2 sectors for now
	mov cl, 0x2;
	mov bx, 0x7e00;
	int 0x13;
	ret;

load_gdt:
	cli;
	pusha;
	lgdt 	[gdt_ptr];
	sti;
	popa;
	ret;

bits 32
kload:
	mov	ds, ax
	mov	ss, ax
	mov	es, ax
	mov	esp,kernel_stack_top;
	pusha
	extern	main
	call	main
	popa
	jmp -2;

times 510 - ($-$$) db 0
dw 0xaa55

section .bss
align 4
kernel_stack_bottom: equ $
	resb 16384 ; 16 KB
kernel_stack_top:

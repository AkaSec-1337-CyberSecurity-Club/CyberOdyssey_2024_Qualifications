bits 16:
section .boot;
global boot;
;org 0x7c00


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

print:
	lodsb	
	or al, al
	jz PrintReturn
	mov ah, 0eh
	int 10h
	jmp print
PrintReturn:
	ret

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
	; returning from c code
	; delete me please
	; returning to 16 bit mode
	mov	ax, RDATA_SEG
	mov	ds, ax
	mov	es, ax
	mov	ss, ax
	mov	sp, 0xFFFF
	jmp	RCODE_SEG:rmode_stub

bits 16
rmode_stub:
	mov	eax, cr0
	and	eax, 0xfffffffe
	mov	cr0, eax
	jmp 0:prot_to_real

prot_to_real:
	xor	ax, ax
	mov	ds, ax
	mov	es, ax
	mov	ss, ax
	sti
	call	load_flag;
	mov	si, 0x7d00;
	call	print;
	jmp -2;

load_flag:
	mov ah, 0x2;
	mov al, 0x1;
	mov cl, 0x5;
	mov bx, 0x7d00;
	int 0x13;
	ret;

msg: db "hello world", 0x0;

times 510 - ($-$$) db 0
dw 0xaa55

section .bss
align 4
kernel_stack_bottom: equ $
	resb 16384 ; 16 KB
kernel_stack_top:

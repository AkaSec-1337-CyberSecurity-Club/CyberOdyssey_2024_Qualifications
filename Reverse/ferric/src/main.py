#!/usr/bin/python3
import random
import string
import subprocess
import tempfile
import base64
import time

flag = "ODYSSEY{str34m_d34th_m3t4l_by_p4nch1k0}"

def gen_rand_pwd(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def gen_x86_64(pwd, rounds):
    ops = ["+", "-", "^", "rr", "rl"]
    res = int.from_bytes(pwd.encode(), "little")
    ret = ""
    for _ in range(rounds):
        op = random.choice(ops)
        rhs = random.randint(1, 10000)
        shv = random.randint(1, 63)
        if (op == "+"):
            res += rhs
            ret += f"\taddq ${rhs}, %rdi\n"
        if (op == "-"):
            res -= rhs
            ret += f"\tsubq ${rhs}, %rdi\n"
        if (op == "^"):
            res ^= rhs
            ret += f"\txorq ${rhs}, %rdi\n"
        if (op == "rl"):
            res = ((res << shv) | (res >> (64 - shv))) & 0xffffffffffffffff
            ret += f"\trolq ${shv}, %rdi\n"
        if (op == "rr"):
            res = ((res >> shv) | (res << (64 - shv))) & 0xffffffffffffffff
            ret += f"\trorq ${shv}, %rdi\n"
    ret += f"\tmovabsq ${res}, %rax\n"    
    ret += f"\tcmpq %rax, %rdi\n"
    return ret

def gen_arm(pwd, rounds):
    ops = ["+", "-", "^", "rr", "rl"]
    res = int.from_bytes(pwd.encode(), "little")
    ret = ""
    for _ in range(rounds):
        op = random.choice(ops)
        rhs = random.randint(1, 10000)
        shv = random.randint(1, 63)
        if (op == "+"):
            res += rhs
            ret += f"\tmov x1, #{rhs}\n"
            ret += f"\tadd x0, x0, x1\n"
        if (op == "-"):
            res -= rhs
            ret += f"\tmov x1, #{rhs}\n"
            ret += f"\tsub x0, x0, x1\n"
        if (op == "^"):
            res ^= rhs
            ret += f"\tmov x1, #{rhs}\n"
            ret += f"\teor x0, x0, x1\n"
        if (op == "rl"):
            res = ((res << shv) | (res >> (64 - shv))) & 0xffffffffffffffff
            ret += f"\tror x0, x0, #{64 - shv}\n"
        if (op == "rr"):
            res = ((res >> shv) | (res << (64 - shv))) & 0xffffffffffffffff
            ret += f"\tror x0, x0, #{shv}\n"
    upper = (res >> 32) & 0xffffffff
    lower = res & 0xffffffff
    upper_high = (upper >> 16) & 0xffff
    upper_low = upper & 0xffff
    lower_high = (lower >> 16) & 0xffff
    lower_low = lower & 0xffff
    ret += f"\tmovk x1, #{upper_high}, lsl 48\n"
    ret += f"\tmovk x1, #{upper_low}, lsl 32\n"
    ret += f"\tmovk x1, #{lower_high}, lsl 16\n"
    ret += f"\tmovk x1, #{lower_low}\n"
    ret += f"\tcmp x0, x1\n"
    return ret

def gen_mips(pwd, rounds):
    ops = ["+", "-", "^", "rr", "rl"]
    res = int.from_bytes(pwd.encode(), "little")
    ret = ""
    for _ in range(rounds):
        op = random.choice(ops)
        rhs = random.randint(1, 10000)
        shv = random.randint(1, 31)
        if op == "+":
            res += rhs
            ret += f"\tdaddiu $a0, $a0, {rhs}\n"
        if op == "-":
            res -= rhs
            ret += f"\tdaddiu $a0, $a0, -{rhs}\n"
        if op == "^":
            res ^= rhs
            ret += f"\txor $a0, $a0, {rhs}\n"
        if op == "rl":
            res = ((res << shv) | (res >> (64 - shv))) & 0xffffffffffffffff
            ret += f"\tdsll $t0, $a0, {shv}\n"
            ret += f"\tdsrl $t1, $a0, {64 - shv}\n"
            ret += f"\tor $a0, $t0, $t1\n"
        if op == "rr":
            res = ((res >> shv) | (res << (64 - shv))) & 0xffffffffffffffff
            ret += f"\tdsrl $t0, $a0, {shv}\n"
            ret += f"\tdsll $t1, $a0, {64 - shv}\n"
            ret += f"\tor $a0, $t0, $t1\n"
    
    upper = (res >> 32) & 0xffffffff
    lower = res & 0xffffffff
    upper_high = (upper >> 16) & 0xffff
    upper_low = upper & 0xffff
    lower_high = (lower >> 16) & 0xffff
    lower_low = lower & 0xffff

    ret += f"\tlui $v0, {upper_high}\n"      
    ret += f"\tori $v0, $v0, {upper_low}\n"  
    ret += f"\tori $v0, $v0, {lower_high}\n" 
    ret += f"\tori $v0, $v0, {lower_low}\n"  
    ret += f"\tbeq $a0, $v0, 0x0\n"
    return ret

def gen_s(pwd, rounds, arch):
    s_code = ""
    if (arch == "x86_64"):
        s_code = gen_x86_64(pwd, rounds)
    if (arch == "arm"):
        s_code = gen_arm(pwd, rounds)
    if (arch == "mips"):
        s_code = gen_mips(pwd, rounds)
    code = f"""
.section .text
.globl pwd_check

pwd_check:
{s_code}
"""
    return code

def gen_bin(code, arch):
    temp1 = tempfile.NamedTemporaryFile("w")
    temp1.write(code)
    temp1.flush()
    temp2 = tempfile.NamedTemporaryFile("rb")
    if (arch == "x86_64"):
        subprocess.run(['as', temp1.name, '-o', temp2.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(['strip', '-R', '.note.gnu.property', temp2.name], check=True)
        encoded = base64.b64encode(temp2.read()).decode()
    if (arch == "mips"):
        subprocess.run(['mips64-linux-gnuabi64-as', "-march=mips64", "-mabi=64", temp1.name, '-o', temp2.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['mips64-linux-gnuabi64-strip', '-R', '.gnu.attributes', '-R', '.pdr','-R', '.MIPS.options', "-R", ".MIPS.abiflags", temp2.name], check=True)
        encoded = base64.b64encode(temp2.read()).decode()
    if (arch == "arm"):
        subprocess.run(['aarch64-linux-gnu-as', temp1.name, '-o', temp2.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['aarch64-linux-gnu-strip', temp2.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        encoded = base64.b64encode(temp2.read()).decode()
    return encoded

def gen_level():
    pwd = gen_rand_pwd()
    rounds = random.randint(120, 140)
    arch = random.choice(["arm", "mips", "x86_64"])
    asm = gen_s(pwd, rounds, arch)
    bin = gen_bin(asm, arch)
    return bin, pwd


def main():
    print("here's an elf, figure out the password for all the 50 levels")
    print("you only have 3 seconds for each level, good luck!\n")
    level = 1
    max_levels = 50
    while level < max_levels:
        elf, pwd = gen_level()
        print(f"ELF: {elf}\n")
        start = int(time.time())
        try:
            out = input("password?: ")
        except:
            return
        end = int(time.time())
        if (end - start > 3):
            print("you ran out of time")
            return
        if (out.strip() == pwd):
            if (level + 1 >= max_levels):
                break
            print("correct! moving on to the next level")
            level += 1
        else:
            print("nope")
            return
    print(f"congrats! here's your flag: {flag}")

if __name__ == "__main__":
    main()
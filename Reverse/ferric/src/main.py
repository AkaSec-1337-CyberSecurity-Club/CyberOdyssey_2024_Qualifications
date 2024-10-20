#!/usr/bin/python3
import random
import string
import subprocess
import tempfile
import base64
import time
from typing import Tuple

flag = "ODYSSEY{str34m_d34th_m3t4l_by_p4nch1k0}"

def gen_pwd(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def gen_x86_64_asm(pwd: str, rounds: int) -> str:
    ops = {
        "+": lambda res, rhs: (res + rhs, f"\taddq ${rhs}, %rdi\n"),
        "-": lambda res, rhs: (res - rhs, f"\tsubq ${rhs}, %rdi\n"),
        "^": lambda res, rhs: (res ^ rhs, f"\txorq ${rhs}, %rdi\n"),
        "rl": lambda res, shv: (((res << shv) | (res >> (64 - shv))) & 0xffffffffffffffff, f"\trolq ${shv}, %rdi\n"),
        "rr": lambda res, shv: (((res >> shv) | (res << (64 - shv))) & 0xffffffffffffffff, f"\trorq ${shv}, %rdi\n")
    }
    
    res = int.from_bytes(pwd.encode(), "little")
    asm = ""
    
    for _ in range(rounds):
        op = random.choice(list(ops.keys()))
        rhs = random.randint(1, 10000)
        shv = random.randint(1, 63) if op in ["rl", "rr"] else None
        res, inst = ops[op](res, rhs if shv is None else shv)
        asm += inst
    
    asm += f"\tmovabsq ${res}, %rax\n\tcmpq %rax, %rdi\n"
    return asm

def gen_arm64_asm(pwd: str, rounds: int) -> str:
    ops = {
        "+": lambda res, rhs: (res + rhs, f"\tmov x1, #{rhs}\n\tadd x0, x0, x1\n"),
        "-": lambda res, rhs: (res - rhs, f"\tmov x1, #{rhs}\n\tsub x0, x0, x1\n"),
        "^": lambda res, rhs: (res ^ rhs, f"\tmov x1, #{rhs}\n\teor x0, x0, x1\n"),
        "rl": lambda res, shv: (((res << shv) | (res >> (64 - shv))) & 0xffffffffffffffff, f"\tror x0, x0, #{64 - shv}\n"),
        "rr": lambda res, shv: (((res >> shv) | (res << (64 - shv))) & 0xffffffffffffffff, f"\tror x0, x0, #{shv}\n")
    }
    
    res = int.from_bytes(pwd.encode(), "little")
    asm = ""
    
    for _ in range(rounds):
        op = random.choice(list(ops.keys()))
        rhs = random.randint(1, 10000)
        shv = random.randint(1, 63) if op in ["rl", "rr"] else None
        res, inst = ops[op](res, rhs if shv is None else shv)
        asm += inst
    
    upper = (res >> 32) & 0xffffffff
    lower = res & 0xffffffff
    asm += f"\tmovk x1, #{(upper >> 16) & 0xffff}, lsl 48\n"
    asm += f"\tmovk x1, #{upper & 0xffff}, lsl 32\n"
    asm += f"\tmovk x1, #{(lower >> 16) & 0xffff}, lsl 16\n"
    asm += f"\tmovk x1, #{lower & 0xffff}\n"
    asm += f"\tcmp x0, x1\n"
    return asm

def gen_mips64_asm(pwd: str, rounds: int) -> str:
    ops = {
        "+": lambda res, rhs: (res + rhs, f"\tdaddiu $a0, $a0, {rhs}\n"),
        "-": lambda res, rhs: (res - rhs, f"\tdaddiu $a0, $a0, -{rhs}\n"),
        "^": lambda res, rhs: (res ^ rhs, f"\txor $a0, $a0, {rhs}\n"),
        "rl": lambda res, shv: (((res << shv) | (res >> (64 - shv))) & 0xffffffffffffffff, 
                                f"\tdsll $t0, $a0, {shv}\n\tdsrl $t1, $a0, {64 - shv}\n\tor $a0, $t0, $t1\n"),
        "rr": lambda res, shv: (((res >> shv) | (res << (64 - shv))) & 0xffffffffffffffff, 
                                f"\tdsrl $t0, $a0, {shv}\n\tdsll $t1, $a0, {64 - shv}\n\tor $a0, $t0, $t1\n")
    }
    
    res = int.from_bytes(pwd.encode(), "little")
    asm = ""
    
    for _ in range(rounds):
        op = random.choice(list(ops.keys()))
        rhs = random.randint(1, 10000)
        shv = random.randint(1, 31) if op in ["rl", "rr"] else None
        res, inst = ops[op](res, rhs if shv is None else shv)
        asm += inst
    
    upper = (res >> 32) & 0xffffffff
    lower = res & 0xffffffff
    asm += f"\tlui $v0, {(upper >> 16) & 0xffff}\n"
    asm += f"\tori $v0, $v0, {upper & 0xffff}\n"
    asm += f"\tori $v0, $v0, {(lower >> 16) & 0xffff}\n"
    asm += f"\tori $v0, $v0, {lower & 0xffff}\n"
    asm += f"\tbeq $a0, $v0, 0x0\n"
    return asm

def gen_asm(pwd: str, rounds: int, arch: str) -> str:
    generators = {
        "x86_64": gen_x86_64_asm,
        "arm": gen_arm64_asm,
        "mips": gen_mips64_asm
    }
    return f"""
.section .text
.globl pwd_check

pwd_check:
{generators[arch](pwd, rounds)}
"""

def compile_and_encode(code: str, arch: str) -> str:
    with tempfile.NamedTemporaryFile("w") as temp1, tempfile.NamedTemporaryFile("rb") as temp2:
        temp1.write(code)
        temp1.flush()
        
        compile_cmds = {
            "x86_64": ['as', temp1.name, '-o', temp2.name],
            "mips": ['mips64-linux-gnuabi64-as', "-march=mips64", "-mabi=64", temp1.name, '-o', temp2.name],
            "arm": ['aarch64-linux-gnu-as', temp1.name, '-o', temp2.name]
        }
        
        strip_cmds = {
            "x86_64": ['strip', '-R', '.note.gnu.property', temp2.name],
            "mips": ['mips64-linux-gnuabi64-strip', '-R', '.gnu.attributes', '-R', '.pdr','-R', '.MIPS.options', "-R", ".MIPS.abiflags", temp2.name],
            "arm": ['aarch64-linux-gnu-strip', temp2.name]
        }
        
        subprocess.run(compile_cmds[arch], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(strip_cmds[arch], check=True)
        
        return base64.b64encode(temp2.read()).decode()

def gen_level() -> Tuple[str, str]:
    pwd = gen_pwd()
    rounds = random.randint(120, 140)
    arch = random.choice(["arm", "mips", "x86_64"])
    asm = gen_asm(pwd, rounds, arch)
    encoded_elf = compile_and_encode(asm, arch)
    return encoded_elf, pwd

def main():
    time_limit = 3
    max_levels = 50

    print("here's an elf, figure out the password for all the 50 levels")
    print(f"you only have {time_limit} seconds for each level, good luck!\n")
    
    for level in range(1, max_levels + 1):
        elf, pwd = gen_level()
        print(f"ELF: {elf}\n")
        
        start_time = time.time()
        try:
            user_input = input("password?: ")
        except EOFError:
            return
        
        if time.time() - start_time > time_limit:
            print("you ran out of time")
            return
        
        if user_input.strip() == pwd:
            if level == max_levels:
                print(f"congrats! here's your flag: {flag}")
                return
            print("correct! moving on to the next level")
        else:
            print("nope")
            return

if __name__ == "__main__":
    main()

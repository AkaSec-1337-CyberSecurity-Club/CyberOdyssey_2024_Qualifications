from z3 import *

def solve_first_part():
    solver = Solver()

    first_part = [BitVec(f'first_part[{i}]', 8) for i in range(8)]
    array = [BitVec(f'array[{i}]', 8) for i in range(8)]

    target = [ord(c) for c in "S,E{{Lw`"]

    for num in range(8):
        num2 = num & 3
        c = first_part[num]

        if num2 == 0:
            transformed = (c - 7) 
        elif num2 == 1:
            transformed = c & ord('f')
        elif num2 == 2:
            transformed = c | ord('(')
        else:  # num2 == 3
            transformed = c ^ ord('a')
        
        array[num] = (transformed + 10)
        solver.add(array[num] == target[num])

    if solver.check() == sat:
        model = solver.model()
        solution = [model[first_part[i]].as_long() for i in range(8)]
        return solution
    else:
        print("No solution found for the first part.")
        return None

def solve_second_part():
    solver = Solver()

    second_part = [BitVec(f'second_part[{i}]', 8) for i in range(8)]
    array = [BitVec(f'array[{i}]', 8) for i in range(8)]

    target = [ord(c) for c in "{GI&9%@/"]

    num2 = 0

    for num in range(8):
        num3 = (num // 3) * 3
        num4 = (second_part[(num + 1) % 8] >> (num3 - num + 3)) & 0xFFFF
        num5 = ((second_part[num] << (num - num3 + 2)) | num4) & 0xFFFF
        array[num] = (num5 * ord('%') + num2) % 256

        # Perform the final bit manipulations
        c = array[num]
        array[num] = (((c << 3) | (c >> 1)) & 0x0F) | (c & 0xF0)

        solver.add(array[num] == target[num])

        num2 += 7

    if solver.check() == sat:
        model = solver.model()
        solution = [model[second_part[i]].as_long() for i in range(8)]
        return solution
    else:
        print("No solution found for the second part.")
        return None

first_part_solution = solve_first_part()
second_part_solution = solve_second_part()

if first_part_solution and second_part_solution:
    payload = bytes(first_part_solution + second_part_solution)

    host = 'rev.akasec.club'
    port = 7331

    conn = remote(host, port)

    conn.recvuntil(b"License please: ")

    conn.sendline(payload)

    print(conn.recvall())
else:
    print("Failed to find solutions for both parts.")

from pwn import *


r = remote("crypto.akasec.club", 1998)

class Solver:
    def __init__(self, size):
        self.size = size
        self.solved = False
        self.known = [False for _ in range(size)]
        self.rand_data = [0 for _ in range(size)]

    def to_vec(self, num):
        vec = list(bin(num)[2:])
        vec = [int(i) for i in vec][::-1]
        return vec
    
    def eval_or(self, val):
        _or_vec = self.to_vec(val)
        for i in range(len(_or_vec)):
            if _or_vec[i] == 0:
                self.known[i] = True
                self.rand_data[i] = 0
        return self.percent()

    def percent(self):
        percent = sum(self.known) / self.size
        return round(percent, 2)
    
    def get_rand_data(self):
        r = [str(i) for i in self.rand_data[::-1]]
        return int("".join(r), 2)
    
    def get_partial_rand_data(self):
        l = self.size - sum(self.know)
        r = [str(i) for i in self.rand_data[l:]]
        return int("".join(r), 2)
    
    def fill_unknown(self):
        for i in range(self.size):
            if not self.known[i]:
                self.rand_data[i] = 1
    

def recv():
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()

def get_resp(choice):
    recv()
    r.send((str(choice) + "\n").encode())
    #r.recvline()
    out = r.recvline()
    out = out.strip().decode()
    data = out.split(" ")[-1]
    return int(data)

def get_or():
    return get_resp(1)

def get_xor():
    return get_resp(2)

def get_bit_length():
    max_l = 0
    for _ in range(30):
        l = len(bin(get_or())[2:])
        if l > max_l:
            max_l = l
    return max_l


from symbolic_mt import Untwister

def split_32bits(f):
    return [f[i:i+32] for i in range(len(f))]

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def split_32bits(f, pad=1):
    s = numberToBase(f, (0xffffffff + 1))
    Z = [bin(i)[2:] for i in s]
    Z[0] = Z[0] + "?"*pad
    return Z[::-1]


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def split_32bits(f, pad=1):
    s = numberToBase(f, 0xffffffff + 1)
    Z = [bin(i)[2:] for i in s]
    Z[0] = Z[0] + "?"*pad
    return Z[::-1]

def generate_data():
  data = []
  r = random.Random()
  r.seed(0x1337)
  for _ in range(300):
    data.append(r.getrandbits(303))
  return r, data

def fix_data(data, pad=17):
  new_data = []
  for d in data:
    new_data += split_32bits(d, pad=pad)
  return new_data

def bruh():
  ut = Untwister()
  r1, data = generate_data()
  data = fix_data(data)
  print("Got data")
  for d in data:
    ut.submit(d)
  return ut.get_random(), r1

def pred(data, pad=17):
    ut = Untwister()
    data = fix_data(data, pad=pad)
    print("Got data")
    for d in data:
        ut.submit(d)
    return ut.get_random()


max_bit_length = get_bit_length()
print("Max bit length: ", max_bit_length)

s = Solver(max_bit_length)

def iter():
    _or = get_or()
    return s.eval_or(_or)

def solve():
    for i in range(100):
        print("solve: ", i, end="\r")
        # Pray to god it converges
        iter()
    s.fill_unknown()
    return s.get_rand_data()

rand_data = solve()
rand_data_2 = int(bin(rand_data)[3:], 2)
print("Found rand_data:", rand_data)
print("Possible one: ", rand_data_2)
pad = 32 - (max_bit_length % 32)

rand_shit = []
rand_shit_2 = []
for i in range(300):
    print(i, end="\r")
    x = get_xor()
    rand = x ^ rand_data
    rand_2 = x ^ rand_data_2
    rand_shit.append(rand)
    rand_shit_2.append(rand_2)

next_shit = 0
try:
    random = pred(rand_shit, pad=pad)
    next_shit = random.getrandbits(max_bit_length)
    print(next_shit)
except:
    random = pred(rand_shit_2, pad=pad)
    next_shit = random.getrandbits(max_bit_length)
finally:
    recv()
    r.send("3\n".encode())
    r.send((str(next_shit) + "\n").encode())
    while True:
        print(r.recvline())

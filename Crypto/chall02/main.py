from Crypto.Util.number import getPrime, bytes_to_long, isPrime
from random import randint
from secret import secret_function

FLAG = bytes_to_long(b'ODYSSEY{rigl_flag}')
    
def main():
    p, q, a, b = secret_function()
    n = p * q
    e = 65537
    c = pow(FLAG, e, n)
    print(f"c = {c}")
    print(">> Hints <<")
    print(f"{p%2}, {p%3}, {p%a}")
    print(f"{q%2}, {q%3}, {q%b}")



if __name__ == "__main__":
    main()

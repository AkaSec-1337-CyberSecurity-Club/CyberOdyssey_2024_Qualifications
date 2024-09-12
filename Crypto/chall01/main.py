from Crypto.Util.number import bytes_to_long
import os
import random

FLAG = bytes_to_long(b'ODYSSEY{whahahhahahhahahahhahhhhhh}')

def main():
    choice = input("How many encryption you are asking for : ")
    for i in range(int(choice)):
        key = random.getrandbits(len(bin(FLAG)[2:]))
        print(f">> {FLAG | key}")
    your_key = input("Enter your key: ")
    if int(your_key) == random.getrandbits(len(bin(FLAG)[2:])):
        print(f"{FLAG}")
    print("Lah y3awn")

if __name__ == "__main__":
    main()
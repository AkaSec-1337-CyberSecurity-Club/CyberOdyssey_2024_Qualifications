from Crypto.Util.number import bytes_to_long
import random

FLAG = b'ODYSSEY{c_la_vie}'
rand_data = random.getrandbits(len(bin(bytes_to_long(FLAG))[2:]))

def main():
    while True:
        choice = input("1- Encrypt with OR\n2- Encrypt with XOR\n3- Predict Next Key\n4- Exit\n")
        if choice == '1':
            key = random.getrandbits(len(bin(bytes_to_long(FLAG))[2:]))
            print(f">> {rand_data | key}")
        elif choice == '2':
            key = random.getrandbits(len(bin(bytes_to_long(FLAG))[2:]))
            print(f">> {rand_data ^ key}")
        elif choice == '3':
            your_key = input("Enter your key: ")
            if int(your_key) == random.getrandbits(len(bin(bytes_to_long(FLAG))[2:])):
                print(f"{FLAG}")
        elif choice == '4':
            print("Lah y3awn")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
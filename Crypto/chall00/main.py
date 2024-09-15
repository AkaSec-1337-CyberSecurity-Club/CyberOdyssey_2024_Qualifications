from Crypto.Util.number import *
import time
import os

FLAG = b'ODYSSEY{khkhkkhkhkhkhkhkkhkhkhkkhkhkhkhkkhkhkhkkhk}'
LINE1 = " _______  ______    _______  __    _  _______  _______  ___      _______  __    _  _______    _______  _______  _______  _______  _______  _______  _______ \n"
LINE2 = "|       ||    _ |  |       ||  |  | ||  _    ||       ||   |    |       ||  |  | ||       |  |   _   ||       ||       ||       ||   _   ||       ||       |\n"
LINE3 = "|_     _||   | ||  |    ___||   |_| || |_|   ||   _   ||   |    |   _   ||   |_| ||    ___|  |  |_|  ||       ||    ___||_     _||  |_|  ||_     _||    ___|\n"
LINE4 = "  |   |  |   |_||_ |   |___ |       ||       ||  | |  ||   |    |  | |  ||       ||   |___   |       ||       ||   |___   |   |  |       |  |   |  |   |___ \n"
LINE5 = "  |   |  |    __  ||    ___||  _    ||  _   | |  |_|  ||   |___ |  |_|  ||  _    ||    ___|  |       ||      _||    ___|  |   |  |       |  |   |  |    ___|\n"
LINE6 = "  |   |  |   |  | ||   |___ | | |   || |_|   ||       ||       ||       || | |   ||   |___   |   _   ||     |_ |   |___   |   |  |   _   |  |   |  |   |___ \n"
LINE7 = "  |___|  |___|  |_||_______||_|  |__||_______||_______||_______||_______||_|  |__||_______|  |__| |__||_______||_______|  |___|  |__| |__|  |___|  |_______|\n"
HEADER = [LINE1,LINE2,LINE3,LINE4,LINE5,LINE6,LINE7, "\n\n"]
MENU = "1- Encrypt\n2- Predict N\n3- Exit\n"

class MyEncryption:
    def __init__(self):
        self.primes = []
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.primes = [self.p, self.q]
        self.n = self.p * self.q
        self.e = 0x10001
        self.flag = bytes_to_long(FLAG)
    
    def encrypt(self, counter):
        n = 1
        self.primes = self.primes[:2]
        for i in range(counter):
            print(f"Generating new primes for round {i+1}")
            new_p = getPrime(1024)
            new_q = getPrime(1024)
            self.primes.append(new_p)
            self.primes.append(new_q)
        for prime in self.primes:
            n *= prime
        self.n = n
        return new_p, pow(self.flag, self.e, n)

def main():
    myrsa = MyEncryption()
    counter = 0
    while True:
        for line in HEADER:
            print(line, end='')
            time.sleep(0.2)
        print(MENU)
        choice = input("Enter your choice: ")
        if choice == '1':
            counter += 1
            p, encrypted_flag = myrsa.encrypt(counter)
            print(f"p = {p}\nencrypted_flag = {encrypted_flag}")
        elif choice == '2':
            your_n = int(input("Enter your N: "))
            if your_n == myrsa.n:
                print(f"Papapapapa wa nta nadi f dakxi dyal matimatic hak flag dyalk w ghyrha mnhna: {FLAG}")
                exit()
        elif choice == '3':
            print("Ka3ka3 hh yallah bye bye")
            exit()
        else:
            print("khoya 3afak rahna mzrobin, khtar mzyan wla ghyrha")
            time.sleep(1.5)
            os.system("clear")

if __name__ == "__main__":
    main()

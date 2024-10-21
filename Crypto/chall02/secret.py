from Crypto.Util.number import isPrime
from random import randint
import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def lcm_of_array(arr):
    result = arr[0]
    for num in arr[1:]:
        result = lcm(result, num)
    return result

def secret_function():
    keys = []
    nums = []
    for i in range(2):
        while True:
            a = randint(1000, 3000)
            arr_a = [i for i in range(1, a)]
            p = lcm_of_array(arr_a) - 1
            if isPrime(p):
                nums.append(a)
                keys.append(p)
                break
    return keys[0], keys[1], nums[0], nums[1]
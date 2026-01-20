# -----------------------------------------------------------------------
# SP24 CMPSC 360 Extra Credit Assignment 2
# RSA Implementation
# 
# Name: <kyle Courtney>
# ID: <971755630>
# 
# 
# You cannot use any external/built-in libraries to help compute gcd
# or modular inverse. You cannot use RSA, cryptography, or similar libs
# for this assignment. You must write your own implementation for generating
# large primes. You must wirte your own implementation for modular exponentiation and
# modular inverse.
# 
# You are allowed to use randint from the built-in random library
# -----------------------------------------------------------------------

from typing import Tuple
import random
import math

# Type defs
Key = Tuple[int, int]
charNum_map = {}

def mod_ex(b, e, m):
    result = 1
    b = b % m  
    while e > 0:
        if e % 2:
            result = (result * b) % m
            e = e - 1
        else:
            b = (b ** 2) % m
            e = e // 2
    return result % m

def is_prime(n, k = 5): 
    if n == 1 or n == 4 or n == 0:
        return False
    elif n == 2 or n == 3:
        return True
    else:
        for _ in range(k):
            a = random.randint(2, n - 2)
            if mod_ex(a, n - 1, n) != 1: #Fermat's little theorem 
                return False
    return True

def gcd(a, b): #extended Euclidean Algorithm
    if b == 0:
        return a
    return gcd(b, a % b)

def modular_inverse(e, k):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1

    while e > 0:
        temp1 = k//e
        temp2 = k - temp1 * e
        k = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if k == 1:
        return d

def generate_e(k): #finds an e between 1 and k where gcd(e, k)==1
    e = 3
    while gcd(e, k) != 1:
        e += 2
    return e

def generate_prime(n: int) -> int: #randomly selects n-bit and checks if n-bit number is prime
    '''
    Description: Generate an n-bit prime number
    Args: n (No. of bits)
    Returns: prime number
    
    NOTE: This needs to be sufficiently fast or you may not get
    any credit even if you correctly return a prime number.
    '''
    prime_candidate = random.getrandbits(n)
    while is_prime(prime_candidate, n) != True:
        prime_candidate = random.getrandbits(n)
    return prime_candidate

def generate_keypair(p: int, q: int) -> Tuple[Key, Key]: #generates tuples(pub, pri)
    '''
    Description: Generates the public and private key pair
    if p and q are distinct primes. Otherwise, raise a value error
    
    Args: p, q (input integers)

    Returns: Keypair in the form of (Pub Key, Private Key)
    PubKey = (n,e) and Private Key = (n,d)
    '''
    if p == q:
        raise ValueError
    if not is_prime(p):
        return ValueError
    if not is_prime(q):
        return ValueError
    
    n = p * q
    k = (p - 1) * (q - 1)
    e = generate_e(k)
    d = modular_inverse(e, k)

    if d < 0:
        d = k + d

    assert(d > 0)
    public_key: Key = (n, e)
    private_key: Key = (n, d)
    return (public_key, private_key)

def chunk_to_num(string):
    num = 0
    for char in string:
        num = num * 96 + (ord(char) - 32)
    return num

def num_to_chunk(num, blocksize):
    chars = []
    for _ in range(blocksize):
        chars += chr(((num % 96) + 32))
        num = num//96
    return "".join(reversed(chars))

def rsa_encrypt(m: str, pub_key: Key, blocksize: int) -> int:
    '''
    Description: Encrypts the message with the given public
    key using the RSA algorithm.

    Args: m (input string)

    Returns: c (encrypted cipher)
    NOTE: You CANNOT use the built-in pow function (or any similar function)
    here.
    '''
    n, e = pub_key
    cipher = []

    while len(m) % blocksize != 0:
        m += chr(32)  # Padding with space

    for i in range(0, len(m), blocksize):
        chunk = m[i : i + blocksize]
        chunk_num = chunk_to_num(chunk)
        en_chunk = mod_ex(chunk_num, e, n)
        charNum_map[chr(en_chunk % 96)] = en_chunk
        cipher.append(chr(en_chunk % 96))
    return "".join(cipher)


def rsa_decrypt(c: str, priv_key: Key, blocksize: int) -> int:
    '''
    Description: Decrypts the ciphertext using the private key
    according to RSA algorithm

    Args: c (encrypted cipher string)

    Returns: m (decrypted message, a string)
    NOTE: You CANNOT use the built-in pow function (or any similar function)
    here.
    '''
    n,d = priv_key
    plain = []
    
    for char in c:
        num = charNum_map[char]
        plain.append(num_to_chunk(mod_ex(num, d, n), blocksize))
    return "".join(plain).rstrip(chr(32))

num = chunk_to_num("abc")
print(num)
print(num_to_chunk(num, 3))

keys = generate_keypair(generate_prime(512), generate_prime(512))
plantext = "K++ 2%~(P."
block_size = 1

c = rsa_encrypt(plantext, keys[0], block_size)
decrypted = rsa_decrypt(c, keys[1], block_size)
if decrypted == plantext:
    print(decrypted)
else:
    print("decrypt didn't work:", decrypted)
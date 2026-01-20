from typing import Tuple
import random
import math

Key = Tuple[int, int]

def gcd(a, b):
    while b:
        a, b = b, a % b 
    return abs(b)

# def generate_keypair(p: int, q: int) -> Tuple[Key, Key]:
#     '''
#     Description: Generates the public and private key pair
#     if p and q are distinct primes. Otherwise, raise a value error
    
#     Args: p, q (input integers)

#     Returns: Keypair in the form of (Pub Key, Private Key)
#     PubKey = (n,e) and Private Key = (n,d)
#     '''
#     if p == q:
#         raise ValueError
#     if not isPrime(p) and isPrime(q):
#         raise ValueError
    
#     n = p * q
#     k = (p - 1) * (q - 1)
#     e = generate_e(k)
    

#     public_key: Key = (n, e[0])
#     private_key: Key = (n, e[1])
#     return (public_key, private_key)


def inverse(e, k):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_k = k

    while e > 0:
        temp1 = temp_k//e
        temp2 = temp_k - temp1 * e
        temp_k = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_k == 1:
        return (d + k) % k
    
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
    plain = ""
    for char in c:
        num = ord(char)
        #plain_num = mod_ex(num, d, n)
        #plain += num_to_chunk(plain_num, blocksize)
    return plain
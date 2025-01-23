import argparse
import os
import time
import re
import hmac
import struct
from hashlib import sha1

myrc4key = "bXlyYzRrZXk="

def rc4(content : bytes, key: bytes) -> bytes:
    S = list(range(256))
    j = 0

    if isinstance(key, str):
        key = key.encode()

    key_length = len(key)

    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    output = bytearray(len(content))

    for n in range(len(content)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        t = (S[i] + S[j]) % 256
        output[n] = content[n] ^ S[t]

    return output

def encryptPassword(filename : str) -> None:
    if not os.path.exists(filename):
        return print("error: file not found.")

    with open(filename, "r") as fd:
        key = fd.read()

    if len(key) < 64:
        return print("error: key must be 64 hexadecimal characters.")
    
    key = key.lower().strip()
    if not re.match(r"^[0-9a-fA-F]+$", key):
        return print("error: key must only contain hexadecimal characters.")
    
    key = rc4(bytes.fromhex(key), myrc4key) # encrypt key

    with open("ft_otp.key", "wb+") as fd:
        fd.write(key)
    print("Encryption successful. Key saved to ft_otp.key")

def genTOTP(key: bytes):
    key = rc4(key, myrc4key) # decrypt key

    step = int(time.time() // 30).to_bytes(8, 'big')
    shash = hmac.digest(key, step, sha1)

    binary = dynamic_truncation(shash)
    otp = binary % 10 ** 6
    print(f"{otp:06d}")

def dynamic_truncation(hs: bytes) -> int:
    offset = hs[-1] & 0b1111 # take first 4 bits

    # generate 8 numbers based on the offset
    return ((hs[offset] & 0x7F) << 24 |
            (hs[offset + 1] & 0xFF) << 16 |
            (hs[offset + 2] & 0xFF) << 8 |
            (hs[offset + 3] & 0xFF))

def ft_otp():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-g", help="File containing the key to encrypt.")
    argparser.add_argument("-k", help="File containing the encrypted key to generate OTP.")
    args = argparser.parse_args()

    if(args.g and args.k):
        return print("Choice between -g or -k argument")
    elif args.g:
        encryptPassword(args.g)
    elif args.k:
        
        if not os.path.exists(args.k):
            return print("error: key file not found.")
        
        if not os.path.isfile(args.k):
            return print("error: key file is not a file.")
        
        with open(args.k, "rb") as f:
            key = f.read()

        genTOTP(key)
    else:
        print("Need -g or -k argument")

if __name__ == "__main__":
    ft_otp()
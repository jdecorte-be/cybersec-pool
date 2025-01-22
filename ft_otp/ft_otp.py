import argparse
import os
import time
import re
import hmac
import struct
from hashlib import sha1

def rc4(content, content_size):
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + content[i % content_size]) % 256
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

def encryptPassword(filename):
    if not os.path.exists(filename):
        print("error: file not found.")
        return

    with open(filename, "r") as fd:
        key = fd.read()

    if len(key) < 64:
        print("error: key must be 64 hexadecimal characters.")
        return
    
    key = key.lower().strip()
    if not re.match(r"^[0-9a-fA-F]+$", key):
        print("error: key must only contain hexadecimal characters.")
        return

    with open("ft_otp.key", "wb+") as fd:
        fd.write(key.encode("ascii"))
    print("Encryption successful. Key saved to ft_otp.key")

def genTOTP(key: bytes):
    step = int(time.time() // 30) 
    shash = hmac.digest(key, struct.pack('>Q', step), sha1)

    binary = dynamic_truncation(shash)
    otp = binary % 10 ** 6
    print(f"{otp:06d}")

def dynamic_truncation(hs: bytes) -> int:
    offset = hs[-1] & 0x0F
    return ((hs[offset] & 0x7F) << 24 |
            (hs[offset + 1] & 0xFF) << 16 |
            (hs[offset + 2] & 0xFF) << 8 |
            (hs[offset + 3] & 0xFF))

def ft_otp():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-g", help="File containing the key to encrypt.")
    argparser.add_argument("-k", help="File containing the encrypted key to generate OTP.")
    args = argparser.parse_args()

    if args.g:
        encryptPassword(args.g)
    elif args.k:
        if not os.path.exists(args.k):
            print("error: key file not found.")
            return
        if not os.path.isfile(args.k):
            return print("error: key file is not a file.")
        with open(args.k, "rb") as f:
            key = f.read()
        genTOTP(bytes.fromhex(key.decode("ascii")))
    else:
        print("Need -g or -k argument")

if __name__ == "__main__":
    ft_otp()
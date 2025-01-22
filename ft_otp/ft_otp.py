import argparse
import os
import math
import time
import re
import hmac
import datetime
import hashlib
import struct
# import pyotp

# https://datatracker.ietf.org/doc/html/rfc6238
# password -> encrypt -> file ft_otp.key
# ft_otp.key -> decrypt -> otp password -> result
def rc4(content, content_size):
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + content[i % content_size]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    output = bytearray(content_size)
    for n in range(content_size):
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        t = (S[i] + S[j]) % 256
        output[n] = content[n] ^ S[t]

    return output
    
# Handle g flag
def encryptPassword(filename):
    if not os.path.exists(filename):
        return print("error: file not found.")

    with open(filename, "r") as fd:
        key = fd.read()
    byte = str.encode(key, "ascii")

    size = len(byte)
    if size < 64:
        return print("error: key must be 64 hexadecimal characters.")

    key = key.lower().strip()
    if not re.match(r"^[0-9a-fA-F]+$", key):
        return print("error: key must be 64 hexadecimal characters.")
    
    with open("ft_otp.key", "wb+") as fd:
        fd.write(rc4(byte, size))

def genTOTP(secret: bytes, period=30, algorithm="sha1"):
    # https://datatracker.ietf.org/doc/html/rfc6238
    secret = rc4(secret, len(secret)).decode("ascii")

    step = int(time.time() // period)
    shash = hmac.digest(secret, struct.pack(">Q", step), algorithm)

    binary = dt(shash)    
    otp = binary % 10 ** 6
    print(f"{otp:06d}")

def dt(hs:bytes):
    offset = hs[-1] & 0x0f
    bincode = (hs[offset]  & 0x7f) << 24 | (hs[offset+1] & 0xff) << 16 | (
		hs[offset+2] & 0xff) <<  8 | (hs[offset+3] & 0xff)
    return bincode

def ft_otp():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-g")
    argparser.add_argument("-k")
    args = argparser.parse_args()

    if args.g:
        encryptPassword(args.g)
    elif args.k:
        with open(args.k, "rb") as f:
            content = f.read()
        genTOTP(content)
    else:
        print("Need -g or -k argument")  

def genTOTPTest():
    secret = "3132333435363738393031323334353637383930"
    testtime = 59
    step = math.floor(testtime // 30).to_bytes(8, byteorder="big")
    print(step)
    print(f"utcTime: {datetime.datetime.fromtimestamp(testtime)}")
    
    ohmac = hmac.new(secret.encode(), step, hashlib.sha1)
    # shash = hmac.digest(secret.encode(), step, "SHA1")
    shash = ohmac.hexdigest()

    # take the last 4 bits of the hash
    offset = int(shash[-1], 16)

    # read 32 bits starting at the offset
    binary = int(shash[(offset * 2): ((offset * 2) + 8)], 16) & 0x7fffffff
    # binary = (
    #     ((shash[offset] & 0x7f) << 24) | \
    #     ((shash[offset + 1] & 0xff) << 16) | \
    #     ((shash[offset + 2] & 0xff) << 8) | \
    #     (shash[offset + 3] & 0xff)
    # )
    # print(binary)

    otp = binary % 1000000
    print(f"{otp:06d}")

def testRC4():
    t1 = b"test"
    print(rc4(t1, len(t1)))
    print(rc4(t1, len(t1)))
    

if __name__ == "__main__":
    testRC4()
    # genTOTPTest()
    # ft_otp()

    

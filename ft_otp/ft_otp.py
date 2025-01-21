import argparse
import string




# https://datatracker.ietf.org/doc/html/rfc6238
# password -> encrypt -> file ft_otp.key
# ft_otp.key -> decrypt -> otp password -> result
# 
def rc4(content, content_size):
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + content[i % content_size]) & 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    output = bytearray(content_size)
    for n in range(content_size):
        k = (k + 1) & 256
        j = (j + S[i]) & 256

        S[i], S[j] = S[j], S[i]

        t = (S[i] + S[j]) & 256
        output[n] ^= S[t]

    return output
    
# Handle g flag
def encryptPassword(filename):
    with open(filename) as fd:
        content = fd.read()
    byte = str.encode(content, "utf-8")
    size = len(byte)
    if size < 64:
        return print("error: key must be 64 hexadecimal characters.")
    encrypted = rc4(byte, len(byte))
    print(encrypted)
    encrypted = rc4(byte, len(byte))
    print(encrypted)



def genTOTP():
    None



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-g")
    argparser.add_argument("-k")
    args = argparser.parse_args()

    if args.g:
        encryptPassword(args.g)
    elif args.k:
        genTOTP()
    else:
        print("Need -g or -k argument")
    
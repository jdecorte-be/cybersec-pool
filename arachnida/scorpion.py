import sys
from PIL import Image
from PIL.ExifTags import TAGS
import time
import os

def readExif(filename):
    try:
        with Image.open(filename) as img:
            exif_data = img.getexif()
            for tag, value in exif_data.items():
                if tag in TAGS:
                    print(f' * {TAGS[tag]}: {value}')
                else:
                    print(f' * {tag}: {value}')
    except Exception as e:
        print("Error reading exif data: ", filename, e)


def scorpion():
    args = sys.argv
    if(len(args) <= 1):
        return print("Error: scorpion need at least 1 file")
    
    supported_format = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    for i in range(1, len(args)):
        if args[i].endswith(supported_format):
            print(f"\nMetaData for {args[i]}")
            print(f"Creation date: {time.ctime(os.path.getctime(args[i]))}")
            print(f"Modification date: {time.ctime(os.path.getmtime(args[i]))}")
            print(f"Size file (bytes): {os.path.getsize(args[i])}")
            readExif(args[i])
        else:
            print("\nError: Unsupported file format", args[i])

if __name__ == "__main__":
    scorpion()

    

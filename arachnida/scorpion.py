import argparse
import PIL.Image

def readExif(filename):
    with PIL.Image.open(filename) as img:
        exif_data = img.getexif()
        print(exif_data)



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("FILE1")
    args = argparser.parse_args()
    readExif(args.FILE1)

    

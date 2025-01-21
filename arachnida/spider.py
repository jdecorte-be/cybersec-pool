import argparse
import requests
from urllib.parse import urljoin, urlparse
import os
import uuid
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.srcs = []
        self.href = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.href.append(value)
        elif tag == "img":
            for name, value in attrs:
                if name == "src":
                    self.srcs.append(value)

    def handle_endtag(self, tag):
        # print(tag)
        None

    def handle_data(self, data):
        # print(data)
        None

def is_same_domain(src, base):
    dsrc = urlparse(src).netloc
    dbase = urlparse(base).netloc
    return dsrc == dbase or dsrc.endswith(f".{dbase}")

def guess_extension(content_type):
    content_type_map = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
    }
    return content_type_map.get(content_type, ".jpg") 

def isAnImage(url):
    r = requests.get(url)
    if not r.ok:
        return False
    return r.headers["content-type"] in ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/jpg"]

def saveImage(url, path):
    if not os.path.exists(path):
        os.makedirs(path)

    r = requests.get(url, stream=True)
    if r.ok:
        extension = guess_extension(r.headers["content-type"])
        name = uuid.uuid4().hex + extension

        with open(path + name, "wb") as f:
                f.write(r.content)
        print("Downloaded " + url)
    else:
        print("Failed to download " + url)

def recursiveWalk(depth, url, path, isrecursive=False):    
    if depth == 0:
        return
    try:
        print("Retrieving " + url)
        r = requests.get(url)
        r.raise_for_status()
        content = r.text
        if not content.strip():
            print("No content retrieved from " + url)
            return
    except requests.exceptions.RequestException as e:
        print(e)
        return
    
    parser = MyHTMLParser()
    parser.feed(content)
    
    for src in parser.srcs:
        src = urljoin(url, src)
        if not src.startswith("#") and is_same_domain(src, url):
            if isAnImage(src):
                saveImage(src, path)

    for href in parser.href:
        href = urljoin(url, href)
        if not src.startswith("#") and is_same_domain(href, url):
            recursiveWalk(depth - 1, href, path, True)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-r", action="store_true")
    argparser.add_argument("-l", type=int, default=5)
    argparser.add_argument("-p", type=str, default="./data/")
    argparser.add_argument("URL", type=str)
    args = argparser.parse_args()

    recursiveWalk(args.l, args.URL, args.p, args.r)

# case 1 
# is under domain
# case 2
# is url in the website or outside
# case 2
# is normal href, like : /abc/def.html
# case 3
# is full url

# https://picsum.photos
# https://www.vangoghmuseum.nl/en/collection
# https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=laptop&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=laptop
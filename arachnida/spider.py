import argparse
import requests
from urllib.parse import urljoin, urlparse
import os
import uuid
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self) -> None:
        self.srcs: list[str] = []
        self.href: list[str] = []
        super().__init__()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.href.append(value)
        elif tag == "img":
            for name, value in attrs:
                if name == "src":
                    self.srcs.append(value)

    def handle_endtag(self, tag: str) -> None:
        # print(tag)
        pass

    def handle_data(self, data: str) -> None:
        # print(data)
        pass


def is_same_domain(src: str, base: str) -> bool:
    dsrc = urlparse(src).netloc
    dbase = urlparse(base).netloc
    return dsrc == dbase or dsrc.endswith(f".{dbase}")


def guess_extension(content_type: str) -> str:
    content_type_map = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
    }
    return content_type_map.get(content_type, ".jpg")


def isAnImage(url: str) -> bool:
    try:
        r = requests.get(url, timeout=15)
        if not r.ok:
            return False
        return r.headers["content-type"] in ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/jpg"]
    except requests.exceptions.RequestException:
        return False


def saveImage(url: str, path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        r = requests.get(url, timeout=15)
        if r.ok:
            extension = guess_extension(r.headers["content-type"])
            name = uuid.uuid4().hex + extension

            with open(os.path.join(path, name), "wb") as f:
                f.write(r.content)
            print("Downloaded " + url)
        else:
            print("Failed to download " + url)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")


def recursiveWalk(depth: int, url: str, path: str, isrecursive: bool = False, visited_urls = set()) -> None:
    if depth == 0:
        return
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        print("Retrieving " + url)
        r = requests.get(url, timeout=15)
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
        if is_same_domain(src, url):
            if isAnImage(src):
                saveImage(src, path)

    if not isrecursive:
        return

    for href in parser.href:
        href = urljoin(url, href)
        if is_same_domain(href, url):
            recursiveWalk(depth - 1, href, path, isrecursive, visited_urls)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-r", action="store_true")
    argparser.add_argument("-l", type=int, default=5)
    argparser.add_argument("-p", type=str, default="./data/")
    argparser.add_argument("URL", type=str)
    args = argparser.parse_args()

    if args.l < 0:
        print("Invalid depth")
    elif args.l != 5 and not args.r:
        print("Recursive mode is not enabled")
    else:
        args.URL = urlparse(args.URL).scheme + "://" + urlparse(args.URL).netloc
        recursiveWalk(args.l, args.URL, args.p, args.r)


# case 1 
# is under domain
# case 2
# is url in the website or outside
# case 2
# is normal href, like : /abc/def.html
# case 3
# is full url

# http://books.toscrape.com/
# https://picsum.photos
# https://giphy.com/explore/website
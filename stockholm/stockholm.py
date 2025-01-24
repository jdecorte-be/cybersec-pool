#!/usr/bin/env python3.11
import argparse
import os

name = "Stockholm"
#  It must only work in a folder called infection in the user’s HOME directory
inf_folder = "/usr/home/infection"

def recursivePathWalk():
    for root, dirs, files in os.walk(inf_folder):
        for file in files:
            print(os.path.join(root, file))
    


def stockholm():
    argparser = argparse.ArgumentParser(description='Stockholm')
    argparser.add_argument('-v', '--version', action='version', version=f'{name} 1.0.0')
    argparser.add_argument('-r', '--reverse', type=str, help='Reverse the infection')
    argparser.add_argument('-s', '--silent', action='store_true', help='Silent mode')
    args = argparser.parse_args()

if __name__ == "__main__":
    stockholm()
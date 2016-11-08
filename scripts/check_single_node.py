#!/usr/bin/env python3

'''
Check wheather the given graph contains single node
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os,sys
import argparse

def read_gr_file(grfile):
    count=0
    # Read from grfile or stdin and store in a suitable data structure
    if grfile is None:
        file = sys.stdin
    else:
        file = open(grfile)
    for line in file:
        count=count+1
        line=line.strip()
        # assumes the .gr file is valid
        if len(line.split())==1:
           print(line.strip(),count)
           break
           


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    args = parser.parse_args()
    read_gr_file(args.grfile)
   


if __name__ == '__main__':
    main()


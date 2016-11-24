#!/usr/bin/env python3

'''
Perform Mapping on a given list
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os
import argparse
import bitarray
import random
import ntpath
import sys


def read_map_gr_file(grfile):
    # Read from grfile or stdin and store in a suitable data structure
    if grfile is None:
        file = sys.stdin
    else:
        file = open(grfile)
    for line in file:
        # assumes the .gr file is valid
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            # need to read vertice and edges count?
            temp = line.split(' ')
            vcount = int(temp[2])
            ecount = int(temp[3])
            pi=list(range(1,vcount+1))
            random.shuffle(pi)
            print(line.strip())     
            continue
            
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        if pi[a-1]<pi[b-1]:
            print(pi[a-1], pi[b-1])
        else: 
            print(pi[b-1], pi[a-1])
    file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    args = parser.parse_args()
    read_map_gr_file(args.grfile)


if __name__ == '__main__':
    main()
    
    



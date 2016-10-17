#!/usr/bin/env python3

'''
Translate .uai files into .gr
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os
import argparse


def read_uai_file(uaifile):
    # Read from uaifile and store in a suitable data structure
    lines = []
    return lines


def translate(graph):
    # return output graph
    # [...]
    return []


def print_gr_file(graph):
    # Print graph to (already opened) outfile stream
    # [...]
    print('Not yet implemented')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("uaifile", help=".uai file containing the input graph")
    args = parser.parse_args()

    graph = read_uai_file(args.uaifile)
    grgraph = translate(graph)
    print_gr_file(grgraph)

if __name__ == '__main__':
    main()


#!/usr/bin/env python3

'''
Perform BFS on a given graph
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os
import argparse

def read_gr_file(grfile):
    # Read from grfile and store in a suitable data structure
    # [...]
    # return graph
    pass

def perform_BFS(graph, center, radius):
    # return output graph
    # [...]
    pass

def print_gr_file(graph, outfile):
    # Print graph to (already opened) outfile stream
    # [...]
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph")
    parser.add_argument("--center", "-c", help="start the BFS from this vertex", nargs='?')
    parser.add_argument("--radius", "-r", help="perform BFS up to this depth")
    args = parser.parse_args()

    # [...]


if __name__ == '__main__':
    main()


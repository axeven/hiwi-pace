#!/usr/bin/env python3

'''
Perform Graph generator on a given graph
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os
import argparse
import bitarray
import random
import ntpath
import sys


def read_gr_file(grfile):
    # Read from grfile or stdin and store in a suitable data structure
    if grfile is None:
        file = sys.stdin
    else:
        file = open(grfile)
    graph = []
    for line in file:
        # assumes the .gr file is valid
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            # need to read vertice and edges count?
            temp = line.split(' ')
            vcount = int(temp[2])
            ecount = int(temp[3])
            graph = [[] for i in range(vcount + 1)]
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        graph[a].append(b)
        graph[b].append(a)
    file.close()
    return graph, vcount, ecount


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
    with open(uaifile) as file:
        lines = file.readlines()
        file.readlines()
    graph = {}
    for line in lines:
        # assumes the .gr file is valid
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            # need to read vertices and edges count?
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        if a not in graph:
            graph[a] = [b]
        else:
            graph[a].append(b)
        if b not in graph:
            graph[b] = [a]
        else:
            graph[b].append(a)
    return graph


def translate(graph):
    # return output graph
    # [...]
    Globalqueue = [center]  ##Globalqueue will store all the vertices of the small graph
    q = []
    q[0] = [center]
    q[1] = graph[center]  ##storing all  the neighbours
    r = 1
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


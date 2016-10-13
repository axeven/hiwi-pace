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
    lines = []
    with open(grfile) as file:
        lines = file.readlines()
    graph = {}
    for line in lines:
        # assumes the .gr file is valid
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            # need to read vertice and edges count?
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

    graph = read_gr_file(args.grfile)
    perform_BFS(graph, args.center, args.radius)


if __name__ == '__main__':
    main()


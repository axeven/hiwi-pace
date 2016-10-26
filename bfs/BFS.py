#!/usr/bin/env python3

'''
Perform BFS on a given graph
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os
import argparse
import random
import ntpath
import sys

def read_gr_file(grfile):
    # Read from grfile or stdin and store in a suitable data structure
    if grfile is None:
        file = sys.stdin
    else:
        file = open(grfile)
    graph = {}
    for line in file:
        # assumes the .gr file is valid
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            # need to read vertice and edges count?
            temp = line.split(' ')
            vcount = int(temp[2])
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        if a not in graph:
            graph[a] = set([b])
        else:
            graph[a].add(b)
        if b not in graph:
            graph[b] = set([a])
        else:
            graph[b].add(a)
    file.close()
    return graph, vcount


def perform_BFS(graph, center, radius):
    # return output graph
    # [...]
    Globalqueue = set([center])  ##Globalqueue will store all the vertices of the small graph
    q = {}
    q[0] = set([center])
    r = 1
    while r <= radius:
        q[r] = set()
        for i in q[r - 1]:
            if i in graph:
                for j in graph[i]:
                    if j not in Globalqueue:
                        q[r].add(j)
                        Globalqueue.add(j)
        r = r + 1

    new_graph = {}
    for i in Globalqueue:
        if i in graph:
            new_graph[i] = graph[i]
            new_graph[i] = new_graph[i].intersection(Globalqueue)
    Globalqueue = sorted(list(Globalqueue))
    indexmap = {}
    idx = 1

    for i in Globalqueue:
        indexmap[i] = idx
        idx += 1
    ng = {}
    for index in range(0, len(new_graph)):
        if Globalqueue[index] in new_graph:
            ng[index + 1] = set([])
            for j in new_graph[Globalqueue[index]]:
                ng[index + 1].add(indexmap[j])
    return ng


def print_gr_file(graph, file, center, radius):  ##, ##outfile):
    # Print graph to (already opened) outfile stream
    # [...]
    count = 0
    if file is None:
        filename = "unknown file"
    else:
        filename = ntpath.basename(file)
    print("c Derived via BFS in " + filename)
    print("c Induced subgraph with")
    print("c center: " + str(center))
    print("c radius: " + str(radius))
    for i in graph:
        temp = sorted(list(graph[i]))
        for index in range(0, len(graph[i])):
            if (i <= temp[index]):
                count = count + 1
    print("p tw", len(graph), count)
    for i in graph:
        temp = sorted(list(graph[i]))
        for index in range(0, len(graph[i])):
            if (i <= temp[index]):
                print(i, temp[index])
                count = count + 1
            else:
                i = i


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    parser.add_argument("--center", "-c", help="start the BFS from this vertex", nargs='?', type=int)
    parser.add_argument("--radius", "-r", help="perform BFS up to this depth", type=int)
    args = parser.parse_args()
    graph, N = read_gr_file(args.grfile)
    if args.radius is None:
        args.radius = random.randrange(1, N)
    if args.center is None:
        args.center = random.randrange(1, N + 1)
    newgraph = perform_BFS(graph, args.center, args.radius)
    print_gr_file(newgraph, args.grfile, args.center, args.radius)

if __name__ == '__main__':
    main()

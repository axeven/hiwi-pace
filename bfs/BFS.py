#!/usr/bin/env python3

'''
Perform BFS on a given graph
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
            graph = [None for i in range(vcount + 1)]
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        if graph[a] is None:
            graph[a] = bitarray.bitarray(vcount + 1)
            graph[a].setall(False)
        graph[a][b] = True
        if graph[b] is None:
            graph[b] = bitarray.bitarray(vcount + 1)
            graph[b].setall(False)
        graph[b][a] = True
    file.close()
    return graph, vcount, ecount


def perform_BFS(graph, center, radius):
    added_to_queue = bitarray.bitarray(len(graph))
    added_to_queue.setall(False)
    queue = [center]
    added_to_queue[center] = True
    r = 1
    new_vertice_count = 1
    while r <= radius:
        next_queue = []
        for q in queue:
            for i in range(1, len(graph)):
                if graph[q][i] and not added_to_queue[i]:
                    next_queue.append(i)
                    added_to_queue[i] = True
                    new_vertice_count += 1
        queue = next_queue
        r += 1
        if len(queue) == 0:
            # the case when the radius is bigger than the sub graph
            break

    if new_vertice_count == len(graph) - 1:  # minus one because graph[0] padding
        # the case when the graph is connected and the radius is bigger than the graph
        return graph

    new_graph = [None for i in range(new_vertice_count + 1)]
    x = 1
    new_e_count = 0
    for i in range(1, len(added_to_queue)):
        if added_to_queue[i]:
            new_graph[x] = bitarray.bitarray(new_vertice_count + 1)
            new_graph[x].setall(False)
            y = 1
            for j in range(1, len(added_to_queue)):
                if added_to_queue[j]:
                    if graph[i][j]:
                        new_graph[x][y] = True
                        new_e_count += 1
                    y += 1
            x += 1
    return new_graph, int(new_e_count / 2)


def print_gr_file(graph, ecount, header=None):
    if header is not None:
        print(header)
    print("p tw", len(graph) - 1, ecount)
    for i in range(1, len(graph)):
        for j in range(i + 1, len(graph)):
            if graph[i][j]:
                print(str(i), str(j))


def get_header(file, center, radius):
    if file is None:
        filename = "unknown file"
    else:
        filename = ntpath.basename(file)
    return "c Derived via BFS in " + filename \
           + "\nc Induced subgraph with\nc center: " \
           + str(center) + "\nc radius: " + str(radius)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    parser.add_argument("--center", "-c", help="start the BFS from this vertex", nargs='?', type=int)
    parser.add_argument("--radius", "-r", help="perform BFS up to this depth", type=int)
    args = parser.parse_args()
    graph, V, E = read_gr_file(args.grfile)
    if args.radius is None:
        args.radius = random.randrange(1, V)
    if args.center is None:
        args.center = random.randrange(1, V + 1)
    newgraph, E = perform_BFS(graph, args.center, args.radius)
    print_gr_file(newgraph, E, get_header(args.grfile, args.center, args.radius))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

'''
Convert an arbitrary .td file into a nice .td
A nice .td contains a tree decomposition such that every bag must satisfy one of the following condition:
  1. It is a leaf and the bag contains the empty set
  2. It is a node having one child and its bag differ (symmetric difference) by exactly one vertex to the bag of its
     child
  3. It is a node having two children and its bag is equal to the bags of its children
The root of the tree is the vertex 1
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os
import argparse
import bitarray
import random
import ntpath
import sys


def read_td_file(tdfile, root):
    # Read from tdfile or stdin and store in a suitable data structure
    if tdfile is None:
        file = sys.stdin
    else:
        file = open(tdfile)
    graph = []
    bags = []
    for line in file:
        # assumes the .td file is valid
        if line[0] == 'c':
            continue
        if line[0] == 's':
            temp = line.split(' ')
            bcount = int(temp[2])
            ecount = int(temp[3])
            vcount = int(temp[4])
            graph = [[] for i in range(bcount + 1)]
            bags = [[] for i in range(bcount + 1)]
            continue
        if line[0] == 'b':
            # reading the bags
            w = line.split(' ')
            len1 = len(w)
            index = int(w[1])
            for i in range(2, len1):
                bags[index].append(int(w[i]))
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        graph[a].append(b)
        graph[b].append(a)
    file.close()
    # make the graph directed and using the root as guide
    tree = graph2tree(graph, root)
    return tree, bags, ecount, vcount


def graph2tree(graph, root):
    used = bitarray.bitarray(len(graph))
    used.setall(False)
    tree = [[] for i in range(len(graph))]
    queue = [root]
    while len(queue) > 0:
        next_queue = []
        for node in queue:
            used[node] = True
            for child in graph[node]:
                if not used[child]:
                    next_queue.append(child)
                    tree[node].append(child)
        queue = next_queue
    return tree


def perform_nice_tree(tree, bags):
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tdfile", help=".gr file containing the input graph", nargs='?')
    args = parser.parse_args()
    root = 1
    tree, bags, E, V = read_td_file(args.tdfile, root)
    print(tree)
    print(bags)
    perform_nice_tree(tree, bags)
    # if args.radius is None:
    #    args.radius = random.randrange(1, V)
    # if args.center is None:
    #    args.center = random.randrange(1, V + 1)
    # newgraph, V, E = perform_BFS(graph, V, E, args.center, args.radius)
    # print_gr_file(newgraph, E, get_header(args.grfile, args.center, args.radius))


if __name__ == '__main__':
    main()

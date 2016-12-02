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

def read_td_file(tdfile):
    # Read from grfile or stdin and store in a suitable data structure
    if tdfile is None:
        file = sys.stdin
    else:
        file = open(tdfile)
    tree = []
    bags=[]
    index=0
    for line in file:
        
        # assumes the .td file is valid
        if line[0] == 'c':
            temp = line.split(' ')
            bcount=int(temp[8])
            bags = [[] for i in range(bcount + 1)]
            continue
        if line[0] == 's':
            # need to read vertice and edges count?
            temp = line.split(' ')
            vcount = int(temp[2])
            ecount = int(temp[3])
            tree = [[] for i in range(vcount + 1)]
            continue      
        if line[0] == 'b':
        #reading the bags
            w = line.split(' ')
            len1= len(w)
            index=index+1
            for i in range (1,len1):
               a=int(w[i])                 
               bags[index].append(a)
                   
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        tree[a].append(b)
        tree[b].append(a)
    file.close()
    
    return tree,bags
def perform_nice_tree(tree,bags):


    
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tdfile", help=".gr file containing the input graph", nargs='?')
    #parser.add_argument("--center", "-c", help="start the BFS from this vertex", nargs='?', type=int)
    #parser.add_argument("--radius", "-r", help="perform BFS up to this depth", type=int)
    args = parser.parse_args()
    tree,bags=read_td_file(args.tdfile)
    perform_nice_tree(tree,bags)
    #if args.radius is None:
    #    args.radius = random.randrange(1, V)
    #if args.center is None:
    #    args.center = random.randrange(1, V + 1)
    #newgraph, V, E = perform_BFS(graph, V, E, args.center, args.radius)
    #print_gr_file(newgraph, E, get_header(args.grfile, args.center, args.radius))


if __name__ == '__main__':
    main()

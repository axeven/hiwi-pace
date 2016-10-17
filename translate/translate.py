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
    index=0
    i=0
    count_clique=0
    count_clique =int(lines[3])	
    for index in range(4,4+count_clique):
        #print (lines[index])
        
        v=lines[index].split(' ')
        w=len(v)
        v[-1] = v[-1].strip()
        v[-1] = v[-1].strip(' ')
        w=len(v)
        #print ("w",w) 
        if (w>3) :
          graph[i]=(v[1:w])
          i=i+1
    print (graph)    
        
    return graph


def translate(graph):
    # return output graph
    # [...]
    ng = {}
    #for index in range(0,len(graph)):
     #   ng[index+1] = graph[Globalqueue[index]]
    ng = graph
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


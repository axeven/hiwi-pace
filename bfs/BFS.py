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
    Globalqueue=[center] ##Globalqueue will store all the vertices of the small graph
    q={}
    q[0]=[center] 
    r=1
    while r<=radius:
       q[r]=[]
       for i in  q[r-1]:
          q[r] =list(set(graph[i]).union(q[r]))
       q[r] =list(set(q[r])-set(Globalqueue)) 
       Globalqueue= list(set(q[r]).union(Globalqueue))
       r=r+1
    
    
    new_graph={}
    for i in Globalqueue:
       new_graph[i]=graph[i]
       new_graph[i]=list(set(new_graph[i]).intersection(Globalqueue)) 
    Globalqueue=sorted(Globalqueue)
    indexmap={}
    idx=1
    
    for i in Globalqueue:
       indexmap[i]=idx
       idx += 1
    for i in new_graph:
        for index in range(0,len(new_graph[i])):          
           new_graph[i][index]= indexmap[new_graph[i][index]]
    ng = {}
    for index in range(0,len(new_graph)):
        ng[index+1] = new_graph[Globalqueue[index]]
    
    return ng         
    

def print_gr_file(graph):##, ##outfile):
    # Print graph to (already opened) outfile stream
    # [...]
    count=0
    print ("c Derived via BFS in input_grfilename")
    print ("c whose md5sum is md5sum_of_input_grfile")
    print ("c Induced subgraph with c center: center c radius: radius")
    for i in graph:
       for index in range(0,len(graph[i])):
            if (i<=graph[i][index]):
                count=count+1
    print ("p tw",len(graph),count)
    for i in graph:
       for index in range(0,len(graph[i])):
            if (i<=graph[i][index]):
                print (i, graph[i][index])
                count=count+1 
            else:
                i=i
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph")
    parser.add_argument("--center", "-c", help="start the BFS from this vertex", nargs='?')
    parser.add_argument("--radius", "-r", help="perform BFS up to this depth")
    args = parser.parse_args()

    graph = read_gr_file(args.grfile)
    newgraph = perform_BFS(graph, int(args.center), int(args.radius))
    print_gr_file(newgraph)

if __name__ == '__main__':
    main()


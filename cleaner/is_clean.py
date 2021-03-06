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
import itertools
from collections import OrderedDict	

def read_gr_file(grfile):
    # Read from grfile or stdin and store in a suitable data structure
    if grfile is None:
        file = sys.stdin
    else:
        file = open(grfile,"r")
    graph = []
    clean="dirty"
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
            new_graph= [[] for i in range(vcount + 1)]
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        graph[a].append(b)
        graph[b].append(a)
        
        if a==b :
           clean= "dirty"
        else:
           clean="clean"
    file.close()
    if clean=="clean": 
     for index in range (0,len(graph)-1): 
       if len(graph[index]) != len(set(graph[index])):
          clean="dirty"
          break
         
    return graph, vcount, ecount, clean


def perform_BFS(graph, V, E, center, radius):
    #perform BFS
    added_to_queue = bitarray.bitarray(V + 1)  # added_to_queue[0] is a padding
    added_to_queue.setall(False)
    queue = [center]
    added_to_queue[center] = True
    r = 1
    new_vertice_count = 1
    while r <= radius:
        next_queue = []
        for q in queue:
            for i in graph[q]:
                if not added_to_queue[i]:
                    next_queue.append(i)
                    added_to_queue[i] = True
                    new_vertice_count += 1
        queue = next_queue
        r += 1
        if len(queue) == 0:
            # the case when the radius is bigger than the sub graph
            break

    if new_vertice_count == V:
        # the case when the graph is connected and the radius is bigger than the graph
        return graph,added_to_queue, V, E

    new_label = {}
    old_label = [-1]  # padding
    idx = 1
    for i in range(1, len(added_to_queue)):
        if added_to_queue[i]:
            new_label[i] = idx
            old_label.append(i)
            idx += 1
    new_graph = [[] for i in range(new_vertice_count + 1)]
    new_e_count = 0
    for i in range(1, new_vertice_count + 1):
        for j in graph[old_label[i]]:
            if added_to_queue[j]:
                new_graph[i].append(new_label[j])
                new_e_count += 1

    return graph,added_to_queue, new_vertice_count,new_e_count

def perform_clean(graph,Globalqueue,vcount,new_vcount):
    #return output_degree
    #[...]
    degree={}
    for i in range(1,len(graph)):       
       	  degree[i]=len(graph[i])
    ## checking connectivity
    if new_vcount==vcount:
        connect="connected"
    else:
        connect="not connected"
    return(degree,connect)
 
def print_gr_file(file, degree,connect,vcount,ecount,clean):  ##, ##outfile):
    # Print graph to (already opened) outfile stream
    # [...]
    count = 0
    counter={}
    
    if file is None:
        filename = "unknown file"
    else:
        filename = ntpath.basename(file)
    for j in degree.values():
       if j not in counter:
           counter[j]=0
       counter[j]+=1	
    final_list=[0]*(max(counter.keys())+1)
    for i in counter:
          final_list[i]=counter[i]  
    #checking that it is clean or dirty  
    if final_list[0]==0 and final_list[1]==0 and clean=="clean": 
        clean="clean"
    else:
        clean="dirty"  
    number_of_vertices= vcount
    number_of_edges=ecount
    print(filename, clean ,number_of_vertices,int(number_of_edges),connect," ".join(str(x) for x in final_list))
    return clean

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    args = parser.parse_args()
    graph, vcount, ecount,clean = read_gr_file(args.grfile)
    radius = vcount
    center = random.randrange(1, vcount + 1)
    graph,added_to_queue, new_vertice_count,new_e_count= perform_BFS(graph,vcount,ecount,center,radius)
    degree,connect=perform_clean(graph,added_to_queue,vcount,new_vertice_count)
    clean=print_gr_file(args.grfile,degree,connect,vcount,ecount,clean)
    if clean=="clean":
      sys.exit(0)
    else:
      sys.exit(-1)
if __name__ == '__main__':
    main()

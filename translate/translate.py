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
        if (w>2) :
          graph[i]=(v[1:w])
          i=i+1
        
    return graph,int(lines[1]) 

def translate(graph):
    # return output graph
    # [...]
    ng = {}
    ng = graph
    new_graph={}
    count=0
    i=0
    j=0
    
    for index in range(0,len(ng)):
        new_graph[count]=[]
        ng[index]=sorted(ng[index])
        if len(ng[index])<=2:
           new_graph[count]= ng[index]
           count=count+1
           
        else:
           while i<len(ng[index]):
               
               
               for j in range(i+1,len(ng[index])):
                   new_graph[count]=[]
                   new_graph[count].append(ng[index][i])
                   new_graph[count].append(ng[index][j])
                   count= count+1 
                   
                   
               i=i+1                
    return new_graph  
    


def print_gr_file(graph,count):
    # Print graph to (already opened) outfile stream
    # [...]
    ##count = set( val for dic in graph for val in dic.values())
    print ("p tw",count,len(graph))
    for i in graph:
       for index in range(0,len(graph[i])):
            print (int(graph[i][index])+1,int(graph[i][index+1])+1)
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("uaifile", help=".uai file containing the input graph")
    args = parser.parse_args()

    graph, count = read_uai_file(args.uaifile)
    grgraph = translate(graph)
    print_gr_file(grgraph,count)

if __name__ == '__main__':
    main()


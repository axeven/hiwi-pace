#!/usr/bin/env python3

'''
Make a gr file 'clean'
A gr file is clean if it's graph is connected and has minimum degree at least 2
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import os
import argparse
import array
import random
import ntpath
import sys


def read_gr_file(grfile):
    print('Reading ...')
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


def remove_degree_one_vertices(graph):
    print('Removing degree one ...')
    queue = []
    added_to_queue = set()
    for u, vs in graph.items():
        if len(vs) < 2:
            queue.append(u)
            added_to_queue.add(u)
    while len(queue) != 0:
        pop = queue[0]
        queue = queue[1:]
        for v in graph[pop]:
            graph[v].remove(pop)
            if v not in added_to_queue and len(graph[v]) < 2:
                queue.append(v)
                added_to_queue.add(v)
        del graph[pop]
    return graph


def get_largest_component(graph, vcount):
    print('Getting largest component ...')
    components = {}
    component_members = {}
    queue = []
    added_to_queue = [False for i in range(vcount+1)]
    added_to_queue_count = 0
    for u in graph:
        if not added_to_queue[u]:
            queue.append(u)
            label = u
            components[label] = {}
            component_members[label] = set([u])
            added_to_queue[u] = True
            added_to_queue_count += 1
            while len(queue) != 0:
                pop = queue[0]
                queue = queue[1:]
                for v in graph[pop]:
                    if v not in component_members[label]:
                        queue.append(v)
                        added_to_queue[v] = True
                        added_to_queue_count += 1
                        component_members[label].add(v)
                components[label][pop] = graph[pop]
    max_label = 0
    max_size = 0
    for label, members in component_members.items():
        size = len(members)
        if size > max_size:
            max_size = size
            max_label = label
    return components[max_label]


def relabel_graph(graph):
    print('Relabeling ...')
    vertices = sorted(list(graph.keys()))
    need_relabel = False
    for i in range(0, len(vertices)):
        if i != vertices[i]:
            need_relabel = True
            break
    if not need_relabel:
        return graph
    new_label = {}
    for i in range(0, len(vertices)):
        new_label[vertices[i]] = i
    new_graph = {}
    for u in vertices:
        new_graph[new_label[u]] = set()
        for v in graph[u]:
            new_graph[new_label[u]].add(new_label[v])
    return new_graph


def print_gr_file(graph, file):  ##, ##outfile):
    # Print graph to (already opened) outfile stream
    # [...]
    count = 0
    if file is None:
        filename = "unknown file"
    else:
        filename = ntpath.basename(file)
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
    args = parser.parse_args()
    graph, N = read_gr_file(args.grfile)
    print_gr_file(relabel_graph(get_largest_component(remove_degree_one_vertices(graph), N)))


if __name__ == '__main__':
    main()

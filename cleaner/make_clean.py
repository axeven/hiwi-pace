#!/usr/bin/env python3

'''
Make a gr file 'clean'
A gr file is clean if it's graph is connected and has minimum degree at least 2
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import argparse

import sys
from bitarray import bitarray


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
            graph = [[] for i in range(vcount + 1)]
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        graph[a].append(b)
        graph[b].append(a)
    file.close()
    return graph, vcount, ecount


def print_gr_file(graph, ecount, header=None):
    if header is not None:
        print(header)
    print("p tw", len(graph) - 1, ecount)
    for i in range(1, len(graph)):
        for j in graph[i]:
            if j > i:
                print(str(i), str(j))


def remove_edges_on_degree_one_vertices(graph, V, E):
    print('Removing degree one ...')
    queue = []
    added_to_queue = bitarray(V + 1)  # index 0 is a padding
    for i in range(1, V + 1):
        if len(graph[i]) < 2:
            queue.append(i)
            added_to_queue[i] = True
    new_e = E
    while len(queue) != 0:
        pop = queue[0]
        queue = queue[1:]
        for v in graph[pop]:
            graph[v].remove(pop)
            if not added_to_queue[v] and len(graph[v]) < 2:
                queue.append(v)
                added_to_queue[v] = True
        new_e -= len(graph[pop])
        graph[pop] = []
    return graph, V, new_e


def get_largest_component(graph, vcount):
    print('Getting largest component ...')
    queue = []
    added_to_queue = bitarray(vcount + 1)
    added_to_queue.setall(False)
    added_to_queue_count = 0
    max_component = []
    max_component_members = bitarray(vcount+1)
    max_component_members.setall(False)
    max_component_members_count = 0
    for u in range(1, vcount + 1):
        if not added_to_queue[u]:
            queue.append(u)
            component = [[] for i in range(vcount + 1)]
            component_members = bitarray(vcount+1)
            component_members.setall(False)
            component_members[u] = True
            component_members_count = 1
            added_to_queue[u] = True
            added_to_queue_count += 1
            while len(queue) != 0:
                pop = queue[0]
                queue = queue[1:]
                for v in graph[pop]:
                    if not component_members[v]:
                        queue.append(v)
                        added_to_queue[v] = True
                        added_to_queue_count += 1
                        component_members[v] = True
                        component_members_count += 1
                component[pop] = graph[pop]
            if component_members_count > max_component_members_count:
                max_component = component
                max_component_members = component_members
                max_component_members_count = component_members_count
    return max_component, max_component_members, component_members_count, int(sum(len(vs) for vs in max_component) / 2)


def relabel_graph(graph, selected_vertices):
    print('Relabeling ...')
    old_label = [-1]
    new_vertice_count = 0
    for i in range(1, len(selected_vertices)):
        if selected_vertices[i]:
            old_label.append(i)
            new_vertice_count += 1
    new_label = {}
    for i in range(0, len(old_label)):
        new_label[old_label[i]] = i
    new_graph = [[] for i in range(new_vertice_count + 1)]
    new_e_count = 0
    for i in range(1, new_vertice_count + 1):
        for j in graph[old_label[i]]:
            if selected_vertices[j]:
                new_graph[i].append(new_label[j])
                new_e_count += 1
    return new_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    args = parser.parse_args()
    graph, V, E = read_gr_file(args.grfile)
    graph, V, E = remove_edges_on_degree_one_vertices(graph, V, E)
    new_graph, Vs, V_, E_ = get_largest_component(graph, V)
    if V != V_:
        new_graph = relabel_graph(new_graph, Vs)
    print_gr_file(new_graph, E_)


if __name__ == '__main__':
    main()

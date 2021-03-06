#!/usr/bin/env python3

'''
Perform Graph generator on a given graph
Copyright 2016, Holger Dell
Licensed under GPLv3.
'''

import argparse
import random
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
            graph = [[] for i in range(vcount + 1)]
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        graph[a].append(b)
        graph[b].append(a)
    file.close()

    return graph, vcount, ecount


def copy_graph(graph):
    new_G = [[]]
    for index in range(1, len(graph)):
        new_G.append([])
        for j in range(0, len(graph[index])):
            new_G[index].append(graph[index][j])
    return new_G


def graph_generator(graph, V, C):
    # Make the graph instances
    new_G = copy_graph(graph)
    n = []
    for i in range(2, C + 1):
        new_G = glue(graph, new_G)
    new_V = C * V - (C - 1) * 2
    new_E = int(sum(len(v) for v in new_G) / 2)

    return new_G, new_E, new_V


def glue(graph, new_G):
    V = len(graph) - 1
    new_V = len(new_G) - 1
    u = random.randrange(1, V + 1)
    v = u
    while u == v:
        v = random.randrange(1, V + 1)
    min_selected = min(u, v)
    max_selected = max(u, v)

    min_mapped = random.randrange(1, new_V + 1)
    max_mapped = min_mapped
    while min_mapped == max_mapped:
        max_mapped = random.randrange(1, new_V + 1)

    for index in range(1, V + 1):
        if index == min_selected:
            new_index = min_mapped
        elif index == max_selected:
            new_index = max_mapped
        else:
            new_index = len(new_G)
            new_G.append([])
        for x in graph[index]:
            if x < min_selected:
                new_G[new_index].append(x + new_V)
            elif x == min_selected:
                new_G[new_index].append(min_mapped)
            elif x < max_selected:
                new_G[new_index].append(x + new_V - 1)
            elif x == max_selected:
                new_G[new_index].append(max_mapped)
            else:
                new_G[new_index].append(x + new_V - 2)

    # removing duplicate edges
    new_G[min_mapped] = list(set(new_G[min_mapped]))
    new_G[max_mapped] = list(set(new_G[max_mapped]))
    return new_G


def relabel_graph(graph, selected_vertices):
    # print('Relabeling ...')
    selected_vertices.sort()

    old_to_new = dict.fromkeys(selected_vertices)
    for i in range(1, len(selected_vertices) + 1):
        old_to_new[selected_vertices[i - 1]] = i

    new_graph = [[] for i in range(len(selected_vertices) + 1)]
    for i in range(1, len(selected_vertices) + 1):
        new_graph[i] = list(map(lambda j: old_to_new[j],
                                graph[selected_vertices[i - 1]]))
    return new_graph


def remove_degree_zero_vertices(graph, V, E):
    selected = []
    for i in range(len(graph)):
        if len(graph[i]) > 0:
            selected.append(i)
    if len(selected) == len(graph) - 1:
        return graph, V, E
    graph = relabel_graph(graph, selected)
    return graph, len(selected), int(sum(len(v) for v in graph) / 2)


def print_gr_file(graph, vcount, ecount):
    print("p tw", vcount, ecount)
    for i in range(1, len(graph)):
        graph[i] = sorted(graph[i])
        for j in graph[i]:
            if j > i:
                print(str(i), str(j))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    parser.add_argument("--C", "-C", help="the number of blocks to be generated", nargs='?', type=int)
    parser.add_argument("--s", "-s", help="Specifies the random seed to be used in this execution of the program",
                        type=int)
    args = parser.parse_args()
    graph, V, E = read_gr_file(args.grfile)
    if args.C is None:
        args.C = 2

    if args.s is None:
        args.s = random.randrange(1, V + 1)
    random.seed(args.s)

    print("c randomly_glue_graphs.py -C", args.C, "-s", args.s, args.grfile)
    new_G, new_E, new_V = graph_generator(graph, V, args.C)
    new_G, new_E, new_V = remove_degree_zero_vertices(new_G, new_E, new_V)
    print_gr_file(new_G, new_V, new_E)


if __name__ == '__main__':
    main()

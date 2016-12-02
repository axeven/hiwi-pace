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

import time


class Component:
    def __init__(self, container_size):
        self.graph = [[] for i in range(container_size + 1)]
        self.members = bitarray(container_size + 1)
        self.members.setall(False)
        self.count = 0

    def add_vertice(self, v):
        self.members[v] = True
        self.count += 1

    def __gt__(self, other):
        return self.count > other.count

    def __contains__(self, item):
        return self.members[item]

    def __getitem__(self, item):
        return self.graph[item]

    def __setitem__(self, key, value):
        self.graph[key] = value

    def __delitem__(self, key):
        pass

    def __str__(self):
        return str(self.graph) + '\n' + str(self.members) + '\n' + str(self.count)


def read_gr_file_and_clean(grfile):
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
            # ecount = int(temp[3]) we do not read vertice count because we are removing
            # self loop and duplicates
            graph = [set() for i in range(vcount + 1)]
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        if a != b:
            graph[a].add(b)
            graph[b].add(a)
    file.close()
    ecount = 0
    for i in range(len(graph)):
        graph[i] = list(graph[i])
        ecount += len(graph[i])
    return graph, len(graph) - 1, int(ecount / 2)


def print_gr_file(graph, vcount, ecount, header=None):
    if header is not None:
        print(header)
    print("p tw", vcount, ecount)
    for i in range(1, len(graph)):
        graph[i] = sorted(graph[i])
        for j in graph[i]:
            if j > i:
                print(str(i), str(j))


def remove_edges_on_degree_one_vertices(graph, V, E):
    # print('Removing degree one ...')
    new_v = V
    new_e = E
    queue = []
    added_to_queue = bitarray(V + 1)  # index 0 is a padding
    added_to_queue.setall(False)
    for i in range(1, V + 1):
        if len(graph[i]) < 2:
            queue.append(i)
            added_to_queue[i] = True
    while len(queue) != 0:
        next_queue = []
        for pop in queue:
            for v in graph[pop]:
                graph[v].remove(pop)
                if not added_to_queue[v] and len(graph[v]) < 2:
                    next_queue.append(v)
                    added_to_queue[v] = True
            new_e -= len(graph[pop])
            new_v -= 1
            graph[pop] = []
        queue = next_queue
    V = new_v
    E = new_e
    return graph, V, E


def reduce_degree_two_vertices(graph, V, E):
    # print('Reducing degree two ...')
    new_v = V
    new_e = E
    for i in range(1, V + 1):
        if len(graph[i]) == 2:
            [u, v] = graph[i]
            if u not in graph[v]:
                graph[u].remove(i)
                graph[v].remove(i)
                graph[u].append(v)
                graph[v].append(u)
                graph[i] = []
                new_v -= 1
                new_e -= 1
    V = new_v
    E = new_e
    return graph, V, E


def get_largest_component(graph):
    # print('Getting largest component ...')
    container_size = len(graph)
    added_to_queue = bitarray(container_size)
    added_to_queue.setall(False)
    added_to_queue_count = 0
    max_component = Component(container_size)
    cur_component = []  # a list of vertices
    max_component = []
    for u in range(1, container_size):
        if not added_to_queue[u]:
            queue = [u]
            cur_component = [u]
            added_to_queue[u] = True
            while len(queue) != 0:
                next_queue = []
                for q in queue:
                    for v in graph[q]:
                        if added_to_queue[v] == False:
                            next_queue.append(v)
                            added_to_queue[v] = True
                            cur_component.append(v)
                queue = next_queue
            if len(cur_component) > len(max_component):
                max_component = cur_component
                if len(max_component) > container_size / 2:
                    # if more than half of vertices is in one component
                    # then that component is definitely the largest one
                    break

    return graph, max_component, len(max_component), int(sum(len(graph[v]) for v in max_component) / 2)


def assert_valid_graph(graph, V, E):
    # assumes if node does not have edges then those node does not exists
    node_exists = bitarray(len(graph))
    node_exists.setall(False)
    should_exists = bitarray(len(graph))
    should_exists.setall(False)
    v_count = 0
    e_count = 0
    for u in range(len(graph)):
        if len(graph[u]) > 0:
            node_exists[u] = True
            v_count += 1
            e_count += len(graph[u])
            for v in graph[u]:
                if v == 0:
                    print(u, 'is referencing 0')
                    sys.exit(-1)
                if u == v:
                    print(u, 'is referencing itself')
                    sys.exit(-1)
                should_exists[v] = True
    e_count = int(e_count / 2)
    if v_count != V:
        print('V count does not match: {:d} and {:d}'.format(V, v_count))
        sys.exit(-1)
    if e_count != E:
        print('E count does not match: {:d} and {:d}'.format(E, e_count))
        sys.exit(-1)

    for i in range(len(node_exists)):
        if not node_exists[i] and should_exists[i]:
            print('Error: {:d} does not have reference'.format(i))
            sys.exit(-1)
        if node_exists[i] and not should_exists[i]:
            print('Error: {:d} is not referenced'.format(i))
            sys.exit(-1)


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grfile", help=".gr file containing the input graph", nargs='?')
    parser.add_argument('--debug', help='enable debug assertion', dest='debug',
                        action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    if args.debug:
        start_time = time.time()
    graph, V, E = read_gr_file_and_clean(args.grfile)
    if args.debug:
        print("file read: V={:d} E={:d}  time: {:f}".format(V, E, time.time() - start_time))
        assert_valid_graph(graph, V, E)
    orig_V = V

    graph, V, E = remove_edges_on_degree_one_vertices(graph, V, E)
    if args.debug:
        print("removed degree-1 vertices: V={:d} E={:d}  time: {:f}".format(V, E, time.time() - start_time))
        assert_valid_graph(graph, V, E)

    graph, V, E = reduce_degree_two_vertices(graph, V, E)
    if args.debug:
        print("reduced degree-2 vertices: V={:d} E={:d}  time: {:f}".format(V, E, time.time() - start_time))
        assert_valid_graph(graph, V, E)

    graph, Vs, V, E = get_largest_component(graph)
    if args.debug:
        print("got largest component: V={:d} E={:d}  time: {:f}".format(V, E, time.time() - start_time))
        # assert_valid_graph(graph, V, E)

    if orig_V != V:
        graph = relabel_graph(graph, Vs)
        if args.debug:
            print("relabeled graph: V={:d} E={:d}  time: {:f}".format(V, E, time.time() - start_time))
            assert_valid_graph(graph, V, E)
    print_gr_file(graph, V, E)


if __name__ == '__main__':
    main()

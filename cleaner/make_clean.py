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
    queue = []
    new_v = V
    added_to_queue = bitarray(V + 1)  # index 0 is a padding
    added_to_queue.setall(False)
    for i in range(1, V + 1):
        if len(graph[i]) < 2:
            queue.append(i)
            added_to_queue[i] = True
    new_e = E
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
    return graph, new_v, new_e


def get_largest_component(graph):
    # print('Getting largest component ...')
    container_size = len(graph)
    added_to_queue = bitarray(container_size)
    added_to_queue.setall(False)
    added_to_queue_count = 0
    max_component = Component(container_size)
    for u in range(1, container_size):
        if not added_to_queue[u]:
            queue = [u]
            component = Component(container_size)
            component.add_vertice(u)
            added_to_queue[u] = True
            added_to_queue_count += 1
            while len(queue) != 0:
                next_queue = []
                for q in queue:
                    for v in graph[q]:
                        if v not in component:
                            next_queue.append(v)
                            added_to_queue[v] = True
                            added_to_queue_count += 1
                            component.add_vertice(v)
                    component[q] = graph[q]
                queue = next_queue
            if component > max_component:
                max_component = component
                if max_component.count > container_size / 2:
                    # if more than half of vertices is in one component
                    # then that component is definitely the largest one
                    break
    return max_component.graph, max_component.members, max_component.count, int(
        sum(len(vs) for vs in max_component) / 2)


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
    parser.add_argument('--debug', help='enable debug assertion', dest='debug',
                        action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    graph, V, E = read_gr_file_and_clean(args.grfile)
    if args.debug:
        assert_valid_graph(graph, V, E)
    graph, V_, E_ = remove_edges_on_degree_one_vertices(graph, V, E)
    if args.debug:
        assert_valid_graph(graph, V_, E_)
    graph, Vs, V_, E_ = get_largest_component(graph)
    if args.debug:
        assert_valid_graph(graph, V_, E_)
    if V != V_:
        graph = relabel_graph(graph, Vs)
        if args.debug:
            assert_valid_graph(graph, V_, E_)
    print_gr_file(graph, V_, E_)


if __name__ == '__main__':
    main()

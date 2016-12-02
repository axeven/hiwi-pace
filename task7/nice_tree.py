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


def read_td_file(tdfile, root):
    # Read from tdfile or stdin and store in a suitable data structure
    if tdfile is None:
        file = sys.stdin
    else:
        file = open(tdfile)
    graph = []
    bags = []
    for line in file:
        # assumes the .td file is valid
        if line[0] == 'c':
            continue
        if line[0] == 's':
            temp = line.split(' ')
            bcount = int(temp[2])
            ecount = int(temp[3])
            vcount = int(temp[4])
            graph = [[] for i in range(bcount + 1)]
            bags = [[] for i in range(bcount + 1)]
            continue
        if line[0] == 'b':
            # reading the bags
            w = line.split(' ')
            index = int(w[1])
            bags[index] = sorted([int(w[i]) for i in range(2, len(w))])
            continue
        v = line.split(' ')
        a = int(v[0])
        b = int(v[1])
        graph[a].append(b)
        graph[b].append(a)
    file.close()
    # make the graph directed by using the root as guide
    tree = graph2tree(graph, root)
    return tree, bags, ecount, vcount


def graph2tree(graph, root):
    # make the graph directed by using the root as guide
    used = bitarray.bitarray(len(graph))
    used.setall(False)
    tree = [[] for i in range(len(graph))]
    queue = [root]
    while len(queue) > 0:
        next_queue = []
        for node in queue:
            used[node] = True
            for child in graph[node]:
                if not used[child]:
                    next_queue.append(child)
                    tree[node].append(child)
        queue = next_queue
    return tree


def diff_of_sorted_lists(a, b):
    c = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        elif a[i] < b[j]:
            c.append(a[i])
            i += 1
        else:
            j += 1
    while i < len(a):
        c.append(a[i])
        i += 1
    return c


def intersection_of_sorted_lists(a, b):
    c = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            c.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return c


def union_of_sorted_lists(a, b):
    c = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            c.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    while i < len(a):
        c.append(a[i])
        i += 1
    while j < len(b):
        c.append(b[j])
        j += 1
    return c


def insert_new_node_differs_by_one(parent, tree, bags):
    child_bag = []
    assert (len(tree[parent]) <= 1)
    if len(tree[parent]) == 1:
        child_bag = bags[tree[parent][0]]
    parent_bag = bags[parent]
    diff = diff_of_sorted_lists(parent_bag, child_bag)
    if len(diff) > 0:
        diff = diff[:len(diff) - 1]
        new_bag = intersection_of_sorted_lists(parent_bag, child_bag)
        new_bag = union_of_sorted_lists(new_bag, diff)
    else:
        # the parent is a subset of the child
        new_bag = child_bag[0:len(parent_bag) + 1]
    bags.append(new_bag)
    tree.append(list(tree[parent]))
    tree[parent] = [len(tree) - 1]


def insert_clones_as_children(parent, tree, bags):
    assert (len(tree[parent]) >= 2)
    add_left = True
    add_right = True
    if len(tree[parent]) == 2:
        if bags[tree[parent][0]] == bags[parent]:
            add_left = False
        if bags[tree[parent][1]] == bags[parent]:
            add_right = False
    assert (add_left or add_right)
    children_left = []
    children_right = []
    if add_left and add_right:
        children_left = tree[parent][0:int(len(tree[parent]) / 2)]
        children_right = tree[parent][int(len(tree[parent]) / 2):]
        tree[parent] = [-1, -1]  # dummies
    elif add_left:
        children_left = [tree[parent][0]]
    elif add_right:
        children_right = [tree[parent][1]]
    if add_left:
        bags.append(list(bags[parent]))
        tree.append(children_left)
        tree[parent][0] = len(tree) - 1
    if add_right:
        bags.append(list(bags[parent]))
        tree.append(children_right)
        tree[parent][1] = len(tree) - 1


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


def remove_ignored_nodes(tree, bags):
    # ignored nodes are identified by having 0 child but non empty bag after the make_nice operation
    selected_vertices = []
    for v in range(1, len(tree)):
        if len(tree[v]) == 0 and len(bags[v]) > 0:
            continue
        selected_vertices.append(v)
    if len(selected_vertices) == len(tree) - 1:
        return tree, bags
    tree = relabel_graph(tree, selected_vertices)
    bags = [bags[i] for i in selected_vertices]
    bags = [[]] + bags
    return tree, bags


def make_nice_node(node, tree, bags):
    if len(tree[node]) == 0:
        # if it's a leaf and has empty bag then it is nice
        if len(bags[node]) == 0:
            print(node, bags[node], tree[node], 'is nice')
            return
        # if the bag is not empty then create a new child that differs by one
        print('making', node, bags[node], tree[node], 'nice')
        insert_new_node_differs_by_one(node, tree, bags)
    elif len(tree[node]) == 1:
        child = tree[node][0]
        diff_a = diff_of_sorted_lists(bags[node], bags[child])
        diff_b = diff_of_sorted_lists(bags[child], bags[node])
        # if it has once child and their symmetric difference is exactly one then it is nice
        if (len(diff_a) == 1 and len(diff_b) == 0) or (len(diff_a) == 0 and len(diff_b) == 1):
            print(node, bags[node], tree[node], 'is nice')
            return
        print('making', node, bags[node], tree[node], 'nice')
        # if the child is actually the same as parent then ignore the child
        # the child will be removed later
        if len(diff_a) == 0 and len(diff_b) == 0:
            tree[node] = tree[child]
            tree[child] = []
        # create a new child that differs by one
        insert_new_node_differs_by_one(node, tree, bags)
    elif len(tree[node]) == 2:
        child_equal = True
        for child in tree[node]:
            if bags[node] != bags[child]:
                child_equal = False
                break
        # if it has two children and their bag are the same as parent's then it is nice
        if child_equal:
            print(node, bags[node], tree[node], 'is nice')
            return
        # if not, then insert (at most) two clones as children, set the previous children as grand children
        print('making', node, bags[node], tree[node], 'nice')
        insert_clones_as_children(node, tree, bags)
    else:
        # if children is more then 2 then insert two clones as children, set the previous children as grand children
        print('making', node, bags[node], tree[node], 'nice')
        insert_clones_as_children(node, tree, bags)


def make_nice_tree(tree, bags, root):
    queue = [root]
    while len(queue) > 0:
        next_queue = []
        for node in queue:
            make_nice_node(node, tree, bags)
            for child in tree[node]:
                next_queue.append(child)
        queue = next_queue
    return tree, bags


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tdfile", help=".gr file containing the input graph", nargs='?')
    args = parser.parse_args()
    root = 1
    tree, bags, E, V = read_td_file(args.tdfile, root)
    print(tree)
    print(bags)
    tree, bags = make_nice_tree(tree, bags, root)
    tree, bags = remove_ignored_nodes(tree, bags)
    print(tree)
    print(bags)
    # if args.radius is None:
    #    args.radius = random.randrange(1, V)
    # if args.center is None:
    #    args.center = random.randrange(1, V + 1)
    # newgraph, V, E = perform_BFS(graph, V, E, args.center, args.radius)
    # print_gr_file(newgraph, E, get_header(args.grfile, args.center, args.radius))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import argparse
import os
import subprocess
import re

from common import get_folder_list, get_file_list, find_matching_file


def extract_file_if_necessary(file, tmpdir):
    tmp_file = tmpdir + '/' + os.path.basename(file)
    while os.path.exists(tmp_file):
        tmp_file += '_'
    if file.endswith('.bz2'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['bzcat', file],
                            stdout=f,
                            stderr=f, )
        return tmp_file
    if file.endswith('.xz'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['xzcat', file],
                            stdout=f,
                            stderr=f, )
        return tmp_file
    if file.endswith('.tar.gz'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['tar', '-xOf', tmp_file, os.path.basename(file)[:-len('.tar.gz')]],
                            stdout=f,
                            stderr=f, )
        return tmp_file
    return file


def get_vertice_and_edge_count_from_gr(file):
    with open(file, 'r') as f:
        for line in f:
            if line.startswith('p tw'):
                s = line.split(' ')
                return int(s[2]), int(s[3])
    return 0, 0


def check_gr_diff(inputf, outputf):
    """

    """
    grfiles = get_file_list(inputf, '.gr')
    no_matching = []
    diff = []
    for gr in grfiles:
        matching = find_matching_file(gr, outputf)
        if matching is None:
            no_matching.append(gr)
            continue
        # file_a = extract_file_if_necessary(gr)
        # file_b = extract_file_if_necessary(matching)
        # if get_vertice_and_edge_count_from_gr(file_a) != get_vertice_and_edge_count_from_gr(file_b):
            # diff.append((gr, matching))
    return diff, no_matching


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_a", '-a', help="first folder to be checked", required=True)
    parser.add_argument("--folder_b", '-b', help="second folder to be checked", required=True)
    parser.add_argument("--output", '-o', help="output file", required=True)

    args = parser.parse_args()
    diff_files, no_match = check_gr_diff(args.folder_a, args.folder_b)
    print('{:d} different matching found.'.format(len(diff_files)))
    if len(no_match) > 0:
        print('{:d} files does not have a match.'.format(len(no_match)))
        for i in no_match:
            print(i)

if __name__ == '__main__':
    main()

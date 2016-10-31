#!/usr/bin/env python3
import argparse
import os
import subprocess
import re

from common import get_folder_list, get_file_list


def find_matching_file(file, target_folder):
    """
    Find a matching of a file, possibly archived, in the target_folder.
    """
    base_name = os.path.basename(file)
    stem_name = base_name[:base_name.rfind('.')]
    matching = None
    archive_ext = ['.bz2', '.xv']
    if os.path.isfile(target_folder + '/' + base_name):
        matching = target_folder + '/' + base_name
    for ext in archive_ext:
        if matching is None and os.path.isfile(target_folder + '/' + base_name + ext):
            matching = target_folder + '/' + base_name + ext
            break
        if matching is None and os.path.isfile(target_folder + '/' + stem_name + ext):
            matching = target_folder + '/' + stem_name + ext
            break
    return matching


def extract_file_if_necessary(file, tmpdir):
    tmp_file = tmpdir + '/' + os.path.basename(file)
    while os.path.exists(tmp_file):
        tmp_file += '_'
    if file.endswith('.bz2'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['bzcat', file],
                                  stdout=f,
                                  stderr=f,)
        return tmp_file
    if file.endswith('.xz'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['xzcat', file],
                                  stdout=f,
                                  stderr=f,)
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
        file_a = extract_file_if_necessary(gr)
        file_b = extract_file_if_necessary(matching)
        if get_vertice_and_edge_count_from_gr(file_a) != get_vertice_and_edge_count_from_gr(file_b):
            diff.append((gr, matching))
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

if __name__ == '__main__':
    main()

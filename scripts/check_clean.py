#!/usr/bin/env python3.5
import argparse
import os

from common import get_folder_list, get_file_list, find_matching_file


def is_clean_file_clean(file):
    with open(file, 'r') as f:
        # assumes the filename does not contain any spaces
        for line in f:
            s = line.split(' ')
            if s[1] == 'clean':
                return True
            else:
                return False


def check_clean(inputf, ext='.clean', remove_dirty=False, print_interval = 1000):
    """
    Check for output of is_clean.py inside of inputf folder.
    Print if there are some dirty result
    """
    clean_files = get_file_list(inputf, ext)
    counter = 0
    dirty_files = []
    for file in clean_files:
        clean = is_clean_file_clean(inputf + file)
        if not clean:
            dirty_files.append(inputf + file)
            if remove_dirty:
                to_remove = find_matching_file(inputf + file, os.path.dirname(inputf + file), True)
                print(to_remove)
        counter += 1
        if counter % print_interval == 0:
            print('{:d} files checked'.format(counter))
    print('{:d} files checked'.format(counter))
    if len(dirty_files) == 0:
        print('No dirty instance found.')
    else:
        print('{:d} dirty instance(s) found:'.format(len(dirty_files)))
        for file in dirty_files:
            print(file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", '-i', help="input folder", required=True)
    parser.add_argument("--extension", '-e', help="extension of the clean file to be checked", default='.clean')
    parser.add_argument('--remove_dirty', '-rm', help='flag whether the dirty files should be removed', dest='remove_dirty', action='store_true')
    parser.set_defaults(remove_dirty=False)
    args = parser.parse_args()
    check_clean(args.input, args.extension, args.remove_dirty)


if __name__ == '__main__':
    main()


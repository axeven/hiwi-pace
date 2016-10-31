#!/usr/bin/env python3.5
import argparse

from common import get_file_list, get_folder_list


def is_clean_file_clean(file):
    with open(file, 'r') as f:
        # assumes the filename does not contain any spaces
        for line in f:
            s = line.split(' ')
            if s[1] == 'clean':
                return True
            else:
                return False


def check_clean(inputf, ext='.clean', print_interval = 1000):
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
        counter += 1
        if counter % print_interval == 0:
            print('{:d} files checked'.format(counter))

    if len(dirty_files) == 0:
        print('No dirty instance found.')
    else:
        print('Dirty instance(s) found:')
        for file in dirty_files:
            print(file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input folder", required=True)
    parser.add_argument("--extension", help="extension of the clean file to be checked", default='.clean')
    args = parser.parse_args()
    check_clean(args.input, args.extension)


if __name__ == '__main__':
    main()


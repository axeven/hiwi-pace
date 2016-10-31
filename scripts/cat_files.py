#!/usr/bin/env python3.5
import argparse

from common import get_file_list, get_folder_list


def cat_files(inputf, ext='.clean'):
    """
    Check for files with a certain extension inside of inputf folder.
    Print those files into stdout
    """
    files = get_file_list(inputf, ext)
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                print(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", '-i', help="input folder", required=True)
    parser.add_argument("--extension", '-e', help="extension of the files to be gathered", default='.clean')
    args = parser.parse_args()
    cat_files(args.input, args.extension)


if __name__ == '__main__':
    main()


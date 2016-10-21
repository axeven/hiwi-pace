#!/usr/bin/env python3
import argparse
import os
import re


def get_folder_list(folder):
    dirs = []
    for sub in os.listdir(folder):
        if os.path.isdir(folder + '/' + sub):
            dirs.append(sub)
    return dirs


def get_file_list(folder, ext=None):
    files = []
    for sub in os.listdir(folder):
        if os.path.isfile(folder + '/' + sub):
            if ext is None:
                files.append(sub)
            else:
                if sub.endswith(ext):
                    files.append(sub)
    return files


def get_radius_from_grfile(grfile, default=0):
    match = re.match('.*?([0-9]+).*', grfile)
    if match is not None:
        return int(match.group(match.lastindex))
    return default


def do_task4(inputf, outputf):
    tasks = []
    subfolders = get_folder_list(inputf)
    for sf in subfolders:
        grfiles = get_file_list(inputf + '/' + sf, 'gr')
        for gr in grfiles:
            print(gr, get_radius_from_grfile(gr))
            tasks.append((inputf + '/' + sf + '/' + gr, get_radius_from_grfile(gr)))
    sorted_tasks = sorted(tasks, key=lambda tuple: tuple[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input folder", required=True)
    parser.add_argument("--output", help="output folder", required=True)
    parser.add_argument("--solver", help="the solver program", required=True)
    parser.add_argument("--timeout", help="timeout ", required=True)
    args = parser.parse_args()
    do_task4(args.input, args.output)


if __name__ == '__main__':
    main()

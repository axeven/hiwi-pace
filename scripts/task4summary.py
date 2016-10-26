#!/usr/bin/env python3.5
import argparse
import csv
import glob
import os
import re


def get_file_list(folder, ext=None):
    """
    Get the file list recursively with a certain extension of the folder
    """
    files = []
    if ext is None:
        dir_ = folder + '/**/*'
    else:
        dir_ = folder + '/**/*' + ext
    for sub in glob.glob(dir_, recursive=True):
        if os.path.isfile(sub):
            files.append(str(sub)[len(folder):])
    return files


def create_summary(input_folder, output_folder, output_file):
    pattern = re.compile(r'c width = (\d+), time = (\d+\.*\d*)')
    summary = []
    for file in get_file_list(output_folder, ext='gr'):
        width = -1
        time = -1
        with open(output_folder + file, 'r') as f:
            for line in f:
                if time == -1:
                    match = pattern.match(line)
                    if match:
                        time = float(match.group(2))
                        if width != -1:
                            break
                if width == -1 and line.startswith('s td'):
                    width = int(line.split()[3]) - 1
                    if time != -1:
                        break
        with open(input_folder + file, 'r') as inp:
            basename = os.path.basename(file)
            for inp_line in inp:
                if inp_line.startswith('p'):
                    temp = inp_line.split(' ')
                    vertice = int(temp[2])
                    edge = int(temp[3])
                    row = {
                        'instance': basename,
                        '#vertices': vertice,
                        '#edges': edge,
                        'tree width': width,
                        'computation time': time
                    }
                    summary.append(row)
                    break

    if len(summary) == 0:
        print("Output folder is empty")
        return
    header = ['instance', '#vertices', '#edges', 'tree width', 'computation time']
    with open(output_file, 'w') as outfile:
        writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n', fieldnames=header)
        writer.writeheader()
        writer.writerows(summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", '-if', help="input folder of the output folder", required=True)
    parser.add_argument("--output-folder", '-of', help="the output folder to be summarized", required=True)
    parser.add_argument("--output", '-o', help="output file", required=True)
    args = parser.parse_args()
    create_summary(args.input_folder, args.output_folder, args.output)

if __name__ == '__main__':
    main()

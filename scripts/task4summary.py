#!/usr/bin/env python3.5
import argparse
import csv
import os
import re
import shutil

from common import get_file_list, find_matching_file, create_tmp_dir, get_extracted_name, \
    extract_file_if_necessary, get_stem_name
from multiprocessing.pool import Pool


def run(param):
    """
    Create a summary file for each input file.
    """
    (out_file, inp_file, tmp_dir_inp, tmp_dir_out) = param

    tmp_inp = extract_file_if_necessary(inp_file, tmp_dir_inp)
    tmp_out = extract_file_if_necessary(out_file, tmp_dir_out)

    # reading width
    width = -1
    with open(tmp_out, 'r') as f:
        for line in f:
            if line.startswith('s td '):
                width = int(line.split()[3]) - 1
                break
    if tmp_out != out_file:
        os.remove(tmp_out)

    # reading time
    log_file = get_stem_name(out_file) + '.log'
    time = -1
    if os.path.isfile(log_file):
        with open(log_file, 'r') as f:
            for line in f:
                tmp = line.split(' ')
                time = float(tmp[1])
                break
    else:
        pattern = re.compile(r'c width = (\d+), time = (\d+\.*\d*)')
        with open(tmp_out, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    time = float(match.group(2))
                    break

    # reading vertice and edge count
    vertice = -1
    edge = -1
    with open(tmp_inp, 'r') as f:
        for line in f:
            if line.startswith('p'):
                tmp = line.split(' ')
                vertice = int(tmp[2])
                edge = int(tmp[3])
                break
    if tmp_inp != inp_file:
        os.remove(tmp_inp)

    stem_name = get_stem_name(os.path.basename(out_file))
    sum_file = os.path.dirname(out_file) + '/' + stem_name + '.summary'
    with open(sum_file, 'w') as f:
        f.write(stem_name + ',' + vertice + ',' + edge + ',' + width + ',' + time)


def create_summary(input_folder, output_folder, output_ext, debug, jobs):
    tmp_dir_inp = create_tmp_dir(__file__)
    tmp_dir_out = create_tmp_dir(__file__)
    tasks = []
    for file in get_file_list(output_folder, ext=output_ext):
        out_file = output_folder + file
        inp_file = find_matching_file(file, output_folder, input_folder)
        if inp_file is not None:
            tasks.append((out_file, inp_file, tmp_dir_inp, tmp_dir_out))
        else:
            print('No input file found for ' + out_file)

    if not debug:
        if jobs == 1:
            for t in tasks:
                run(t)
        else:
            with Pool(processes=jobs) as p:
                p.map(run, tasks, chunksize=1)

    shutil.rmtree(tmp_dir_inp)
    shutil.rmtree(tmp_dir_out)

    summary = []
    for file in get_file_list(output_folder, ext='.summary'):
        with open(file, 'r') as f:
            for line in f:
                summary.append(line)
                break
    summary = sorted(summary)

    if len(summary) == 0:
        print('output folder does not contain ' + output_ext + ' files')
    else:
        print('instance,#vertices,#edges,tree width,computation time')
        for line in summary:
            print(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", '-if', help="input folder of the output folder", required=True)
    parser.add_argument("--output-folder", '-of', help="the output folder to be summarized", required=True)
    parser.add_argument("--output-ext", '-ox', help="the extension of the output files to be scanned", default='.xz')
    parser.add_argument('--jobs', '-j', help='number of parallel job. default=4', default=4, type=int)
    parser.add_argument("--debug", '-d', help="debugging purpose", dest='debug', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    create_summary(args.input_folder, args.output_folder, args.output_ext, args.debug, args.jobs)


if __name__ == '__main__':
    main()

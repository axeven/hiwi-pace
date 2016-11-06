#!/usr/bin/env python3
import argparse
import os
import subprocess
import re

import shutil
from common import get_folder_list, get_file_list, find_matching_file, extract_file_if_necessary, \
    get_extracted_name, archive_file, create_tmp_dir

from multiprocessing.pool import Pool


def get_radius_from_grfile(grfile, default=0):
    """
    Extract the radius/number from a gr file name
    """
    match = re.findall('(\d+)', grfile)
    if len(match) > 0 and str(grfile).endswith(str(match[-1]) + '.gr'):
        return int(match[-1])
    return default


def run(run_param):
    """

    """
    (tool, input_file, output_file, archive_input, archive_output_ext, tmp_dir_input, tmp_dir_output) = run_param
    tmp_input = input_file
    if archive_input:
        print('Extracting ' + input_file)
        tmp_input = extract_file_if_necessary(input_file, tmp_dir_input)
    tmp_output = output_file
    if archive_output_ext is not None:
        tmp_output = tmp_dir_output + '/' + get_extracted_name(os.path.basename(output_file))
    print("Running {:s} on {:s} ".format(os.path.basename(tool), os.path.basename(tmp_input)))
    with open(tmp_output, 'w') as f:
        ret = subprocess.call(['python3', tool, tmp_input],
                              stdout=f,
                              stderr=f)
    if archive_input:
        print('Removing ' + tmp_input)
        os.remove(tmp_input)
    if archive_output_ext is not None:
        print('Archiving into '
              '' + output_file)
        archive_file(tmp_output, output_file, archive_output_ext)
    if archive_output_ext is not None:
        print('Removing ' + tmp_output)
        os.remove(tmp_output)
    print("Job {:s} on {:s} is done.".format(os.path.basename(tool), os.path.basename(input_file)))


def is_failed(file, validate=None, tmp_dir=None):
    """
    A task is failed if the output is small and/or it does not validate
    Small ~ less than 68 bytes xz file
    """
    stats = os.stat(file)
    if stats.st_size <= 68:
        if validate is None:
            return True
        try:
            if get_extracted_name(os.path.basename(file)) != os.path.basename(file):
                file = extract_file_if_necessary(file, tmp_dir)
            output = subprocess.check_output([validate, file])
        except subprocess.CalledProcessError:
            output = 'invalid'
        if output == 'invalid':
            return True
    return False


def do_task(inputf, input_ext, failed_outputf, outputf, output_ext, tool, jobs, validate):
    """
    Run solver in parallel sub processes on the files inside inputf folder.
    """
    print('Checking failed tasks')
    failed = []
    files = get_file_list(inputf, input_ext)
    tmp_dir = create_tmp_dir(tool)
    for f in files:
        match = find_matching_file(inputf + f, inputf, failed_outputf)
        if match is None or is_failed(match, validate, tmp_dir):
            failed.append(inputf + f)
    print('Found {:d} failed tasks.'.format(len(failed)))
    if len(failed) == 0:
        return
    failed = sorted(failed)
    for f in failed:
        print(f)
    print('Creating tasks ...')
    # assumes all input has same extension
    archive_input = (get_extracted_name(os.path.basename(failed[0])) != os.path.basename(failed[0]))
    tmp_dir_input = None
    if archive_input:
        tmp_dir_input = create_tmp_dir(tool)
    tmp_dir_output = None
    if output_ext is not None:
        tmp_dir_output = create_tmp_dir(tool)
    tasks = []
    for f in failed:
        basename = os.path.basename(f)
        output_file = outputf + get_extracted_name(f[len(inputf):]) + output_ext
        tasks.append((tool, f, output_file, archive_input,
                      output_ext, tmp_dir_input, tmp_dir_output))
    print('{:d} tasks created.'.format(len(tasks)))

    print('Checking for write permission ...')
    permitted_task = []
    not_permitted = []
    for t in tasks:
        if os.access(t[2], os.W_OK):
            permitted_task.append(t)
        else:
            not_permitted.append(t)
    tasks = permitted_task
    print('{:d} tasks not permitted.'.format(len(not_permitted)))
    print('{:d} tasks left.'.format(len(tasks)))
    print('Running tasks in {:d} jobs ...'.format(jobs))
    if jobs == 1:
        for t in tasks:
            run(t)
    else:
        with Pool(processes=jobs) as p:
            p.map(run, tasks, chunksize=1)
    shutil.rmtree(tmp_dir)
    if tmp_dir_input is not None:
        shutil.rmtree(tmp_dir_input)
    if tmp_dir_output is not None:
        shutil.rmtree(tmp_dir_output)
    print('Tasks finished.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", '-i', help="input folder", required=True)
    parser.add_argument("--input-ext", '-ix', help="input extension", required=True)
    parser.add_argument("--output-failed", '-of', help="output folder of the failed tasks", required=True)
    parser.add_argument("--output", '-o', help="output folder", required=True)
    parser.add_argument("--output-ext", '-ox', help="output extension", required=True)
    parser.add_argument("--tool", '-t', help="the tool program", required=True)
    parser.add_argument('--jobs', '-j', help='number of parallel job. default=4', default=4, type=int)
    parser.add_argument('--validate', '-v', help='path to td-validate', required=True)
    args = parser.parse_args()
    do_task(args.input, args.input_ext, args.output_failed, args.output, args.output_ext, args.tool, args.jobs, args.validate)


if __name__ == '__main__':
    main()

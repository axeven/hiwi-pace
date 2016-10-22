#!/usr/bin/env python3.5
import argparse
import glob
import os
import subprocess
import re

from multiprocessing.pool import Pool


def get_folder_list(folder):
    """
    Get the sub folder list (non recursively) of the folder
    """
    dirs = []
    for sub in os.listdir(folder):
        if os.path.isdir(folder + '/' + sub):
            dirs.append(sub)
    return dirs


def get_file_list(folder, ext=None):
    """
    Get the file list recursively with a certain extension of the folder
    """
    files = []
    if ext is None:
        dir = folder + '/**/*'
    else:
        dir = folder + '/**/*' + ext
    for sub in glob.glob(dir, recursive=True):
        if os.path.isfile(sub):
            files.append(str(sub)[len(folder):])
    return files


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
    Create a subprocess to run solver for timeout seconds on the input_file.
    The output is stored in the output_file.
    """
    (solver, input_file, output_file, timeout) = run_param
    basename = os.path.basename(input_file)
    print("Running {:s} for {:d} on {:s} "
          "logfile: {:s}".format(os.path.basename(solver), timeout, basename, output_file))
    with open(output_file, 'w') as f:
        with open(input_file, 'r') as inp:
            success = False
            try:
                run_output = subprocess.check_output([solver],
                                                     stdin=inp,
                                                     stderr=f,
                                                     timeout=timeout)
                print("Job on {:s} finished".format(basename))
                success = True
            except subprocess.CalledProcessError as e:
                print("Error on {:s}".format(basename))
                print(e)
            except subprocess.TimeoutExpired as e:
                print("Timeout error on {:s}".format(basename))
            if success:
                with open(output_file, 'wb') as o:
                    o.write(run_output)
            else:
                if os.path.isfile(output_file):
                    os.remove(output_file)


def do_task4(inputf, outputf, solver, timeout, jobs):
    """
    Run solver in parallel sub processes on the files inside inputf folder.
    """
    tasks = []
    subfolders = get_folder_list(inputf)
    for sf in subfolders:
        grfiles = get_file_list(inputf + '/' + sf, '.gr')
        for gr in grfiles:
            tasks.append(
                (
                    get_radius_from_grfile(gr),
                    inputf + '/' + sf + gr,
                    outputf + '/' + sf + gr
                ))
            outputfolder = os.path.dirname(outputf + '/' + sf + gr)
            if not os.path.exists(outputfolder):
                os.makedirs(outputfolder)
    sorted_tasks = sorted(tasks, key=lambda tuple: tuple[0])
    desc_tasks = []
    for radius, input, output in sorted_tasks:
        print((radius, solver, input, output, timeout))
        desc_tasks.append((solver, input, output, timeout))
    if jobs == 1:
        for t in desc_tasks:
            run(t)
    else:
        with Pool(processes=jobs) as p:
            p.map(run, desc_tasks, chunksize=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input folder", required=True)
    parser.add_argument("--output", help="output folder", required=True)
    parser.add_argument("--solver", help="the solver program", required=True)
    parser.add_argument("--timeout", help="timeout in seconds", required=True, type=int)
    parser.add_argument('--jobs', help='number of parallel job. default=4', default=4, type=int)
    args = parser.parse_args()
    do_task4(args.input, args.output, args.solver, args.timeout, args.jobs)


if __name__ == '__main__':
    main()

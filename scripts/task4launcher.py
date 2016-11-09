#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import subprocess
import time

from common import get_folder_list, get_file_list, extract_file_if_necessary, create_tmp_dir,\
    archive_file, get_extracted_name

from multiprocessing.pool import Pool


def get_radius_from_grfile(grfile, default=0):
    """
    Extract the radius/number from a gr file name
    """
    match = re.findall('(\d+)', grfile)
    ext = ['.gr', '.gr.xz', '.gr.bz2']
    for e in ext:
        if len(match) > 0 and str(grfile).endswith(str(match[-1]) + e):
            return int(match[-1])
    return default


def run(run_param):
    """
    Create a subprocess to run solver for timeout seconds on the input_file.
    The output is stored in the output_file.
    """
    (solver, input_file, output_file, timeout, tmp_dir_input, tmp_dir_output, output_ext) = run_param
    extracted_name = get_extracted_name(input_file)
    if extracted_name != input_file:
        print('Extracting ' + input_file)
    tmp_input = extract_file_if_necessary(input_file, tmp_dir_input)
    basename = os.path.basename(tmp_input)
    tmp_output = output_file
    # for now only support .xz
    if output_ext == '.xz':
        tmp_output = tmp_dir_output + '/' + basename
    print("Running {:s} for {:d} on {:s} "
          "logfile: {:s}".format(os.path.basename(solver), timeout, basename, tmp_output))
    success = False
    with open(tmp_output, 'w') as f:
        with open(tmp_input, 'r') as inp:
            try:
                start = time.time()
                run_output = subprocess.check_output([solver],
                                                     stdin=inp,
                                                     stderr=f,
                                                     timeout=timeout)
                print("Time: " + '{:.2f} s'.format(time.time() - start) + ' for ' + input_file)
                success = True
            except subprocess.CalledProcessError as e:
                print("Error on {:s}".format(basename))
                print(e)
            except subprocess.TimeoutExpired as e:
                print("Timeout error on {:s}".format(basename))
            if success:
                with open(output_file, 'wb') as o:
                    o.write(run_output)

    if tmp_output != output_file and success:
        print('Compressing into ' + output_file)
        archive_file(tmp_output, output_file, output_ext)
    if tmp_output != output_file or not success:
        os.remove(tmp_output)
    if tmp_input != input_file:
        os.remove(tmp_input)
    if success:
        print("Job on {:s} finished".format(basename))

def do_task4(inputf, input_ext, outputf, output_ext, solver, timeout, jobs, debug):
    """
    Run solver in parallel sub processes on the files inside inputf folder.
    """
    tmp_dir_input = create_tmp_dir(solver)
    tmp_dir_output = create_tmp_dir(solver)
    tasks = []
    print('Creating tasks ...')
    subfolders = get_folder_list(inputf)
    for sf in subfolders:
        grfiles = get_file_list(inputf + '/' + sf, input_ext)
        for gr in grfiles:
            tasks.append(
                (
                    get_radius_from_grfile(gr),
                    inputf + '/' + sf + gr,
                    get_extracted_name(outputf + '/' + sf + gr) + output_ext
                ))
            outputfolder = os.path.dirname(get_extracted_name(outputf + '/' + sf + gr) + output_ext)
            if not os.path.exists(outputfolder):
                os.makedirs(outputfolder)
    print('{:d} tasks created.'.format(len(tasks)))
    sorted_tasks = sorted(tasks, key=lambda tuple: tuple[0])
    desc_tasks = []
    for radius, input, output in sorted_tasks:
        desc_tasks.append((solver, input, output, timeout, tmp_dir_input, tmp_dir_output, output_ext))

    if not debug:
        if jobs == 1:
            for t in desc_tasks:
                run(t)
        else:
            with Pool(processes=jobs) as p:
                p.map(run, desc_tasks, chunksize=1)
    shutil.rmtree(tmp_dir_input)
    shutil.rmtree(tmp_dir_output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input folder", required=True)
    parser.add_argument("--input-ext", help="extension of input files", default='.gr')
    parser.add_argument("--output", help="output folder", required=True)
    parser.add_argument("--output-ext", help="extension of input files", default='.gr')
    parser.add_argument("--solver", help="the solver program", required=True)
    parser.add_argument("--timeout", help="timeout in seconds", required=True, type=int)
    parser.add_argument('--jobs', help='number of parallel job. default=4', default=4, type=int)
    parser.add_argument("--debug", help="debugging purpose", dest='debug', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    do_task4(args.input, args.input_ext, args.output, args.output_ext, args.solver, args.timeout, args.jobs, args.debug)


if __name__ == '__main__':
    main()

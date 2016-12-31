#!/usr/bin/env python3
import argparse
import datetime
import getpass
import os
import re
import shutil
import subprocess
import time

from common import get_folder_list, get_file_list, extract_file_if_necessary, create_tmp_dir, \
    archive_file, get_extracted_name, get_file_size, get_stem_name, get_sha1_checksum, \
    get_line_count

from multiprocessing.pool import Pool
import random


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
    (solver, input_file, output_file, timeout,
     tmp_dir_input, tmp_dir_output, output_ext, seed, validate) = run_param
    extracted_name = get_extracted_name(input_file)
    if extracted_name != input_file:
        print('Extracting ' + input_file)
    tmp_input = extract_file_if_necessary(input_file, tmp_dir_input)
    basename = os.path.basename(tmp_input)
    stemname = get_stem_name(basename)
    time_log_file = os.path.dirname(output_file) + '/' + stemname + '.log'
    tmp_output = output_file
    tmp_err = tmp_dir_output + "/" + stemname + '.err'
    # for now only support .xz
    if output_ext.endswith('.xz'):
        tmp_output = tmp_dir_output + '/' + stemname
    print("Running {:s} for {:d} on {:s} "
          "logfile: {:s}".format(os.path.basename(solver), timeout, stemname, tmp_output))
    status = "success"
    with open(tmp_output, 'wb') as f:
        with open(tmp_input, 'r') as inp:
            with open(time_log_file, 'w') as tlf:
                tlf.write("==================run=info=================\n")
                tlf.write("program: " + solver + "\n")
                tlf.write("input graph: " + input_file + "\n")
                tlf.write("timeout: " + str(timeout) + "\n")
                tlf.write("random seed: " + str(seed) + "\n")
                tlf.write("output td: " + output_file + "\n")
            start = time.time()
            try:
                with open(tmp_err, 'w') as t_e:
                    run_output = subprocess.check_output([solver, "-s", str(seed)],
                                                         stdin=inp,
                                                         stderr=t_e,
                                                         timeout=timeout)
                end = time.time() - start
                run_exit_status = 0
            except subprocess.CalledProcessError as e:
                status = "error"
                run_exit_status = e.returncode
            except subprocess.TimeoutExpired as e:
                status = "timeout"
                run_exit_status = 124
            with open(time_log_file, 'a') as tlf:
                with open(tmp_err, 'r') as t_e:
                    err_lines = t_e.readlines()
                tlf.write("=======stderr output from program=========\n")
                tlf.writelines(err_lines)
                tlf.write("=======validation=========================\n")
                if status == "success":
                    tlf.write("program exited successfully\n")
                elif status == "timeout":
                    tlf.write("program timed out\n")
                else:
                    tlf.write("program error\n")
                    tlf.write(e.output)
            # writing td
            dbs = -1 # max bag size
            if status == "success":
                f.write(run_output)
                decoded = run_output.decode()
                lines = decoded.split("\n")
                for line in lines:
                    if line.startswith('s'):
                        dbs = int(line.split(' ')[3])
                        break
            else:
                end = -1
    # running validate
    try:
        val_output = subprocess.check_output([validate, tmp_input, tmp_output],
                                             stderr=subprocess.STDOUT)
        val_exit_code = 0
    except subprocess.CalledProcessError as e:
        val_output = e.output
        val_exit_code = e.returncode
    with open(time_log_file, 'a') as tlf:
        tlf.write("tree decomposition: " + val_output.decode())
        tlf.write("=======run time===========================\n")
        tlf.write("real: {:.8f} s\n".format(end))
        tlf.write("=======misc===============================\n")
        tlf.write("user: " + getpass.getuser() + "\n")
        tlf.write("cwd: " + os.getcwd() + "\n")
        tlf.write("timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        tlf.write("input sha1: " + get_sha1_checksum(input_file) + "\n")
        if os.path.isfile(output_file):
            tlf.write("treedec sha1: " + get_sha1_checksum(output_file) + "\n")
        if val_exit_code == 0:
            tlf.write("valid tree decomposition: yes\n")
        else:
            tlf.write("valid tree decomposition: no\n")
        tlf.write("number of lines in  .td file: " + str(get_line_count(output_file)) + "\n")
        tlf.write("=======csv================================\n")
        tlf.write("{:s};{:d};{:d};{:d};{:d};{:.8f}\n".format(basename, timeout, dbs, val_exit_code, run_exit_status, end))

    if tmp_output != output_file and status == "success":
        print('Compressing into ' + output_file)
        archive_file(tmp_output, output_file, output_ext)
    if tmp_output != output_file or status != "success":
        # print('Removing', tmp_output)
        os.remove(tmp_output)
    if tmp_input != input_file:
        # print('Removing', tmp_input)
        os.remove(tmp_input)
    if status == "success":
        print("Job on {:s} finished".format(basename))


def do_tw_eval(inputf, input_ext, outputf, output_ext, solver, validate, timeout, jobs, debug):
    """
    Run solver in parallel sub processes on the files inside inputf folder.
    """
    tmp_dir_input = create_tmp_dir(solver)
    tmp_dir_output = create_tmp_dir(solver)
    tasks = []
    print('Creating tasks ...')
    grfiles = get_file_list(inputf, input_ext)
    for gr in grfiles:
        output_file = get_stem_name(outputf + gr) + output_ext
        tasks.append(
            (
                get_file_size(inputf + gr),
                inputf + gr,
                output_file
            ))
        outputfolder = os.path.dirname(output_file)
        if not os.path.exists(outputfolder):
            os.makedirs(outputfolder)
    print('{:d} tasks created.'.format(len(tasks)))
    sorted_tasks = sorted(tasks, key=lambda tuple: tuple[0])
    desc_tasks = []
    max_int = 2 ** 32
    for radius, input, output in sorted_tasks:
        if debug:
            print(radius, input, output)
        seed = random.randint(0, max_int)
        desc_tasks.append((solver, input, output, timeout,
                           tmp_dir_input, tmp_dir_output, output_ext, seed, validate))

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
    parser.add_argument("--input", "-i", help="input folder", required=True)
    parser.add_argument("--input-ext", "-ix", help="extension of input files", default='.gr')
    parser.add_argument("--output", "-o", help="output folder", required=True)
    parser.add_argument("--output-ext", "-ox", help="extension of input files", default='.td')
    parser.add_argument("--program", "-p", help="the tw program to run", required=True)
    parser.add_argument("--validate", "-v", help="the td validate program", required=True)
    parser.add_argument("--timeout", "-t", help="timeout in seconds", required=True, type=int)
    parser.add_argument('--jobs', "-j", help='number of parallel job. default=4', default=4, type=int)
    parser.add_argument("--debug", "-d", help="debugging purpose", dest='debug', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    random.seed(0)
    print(args)
    validate = args.validate
    if not os.path.isfile(validate):
        print("invalid td-validate path")
        return
    if not validate.startswith("/"):
        validate = "./" + validate
    do_tw_eval(args.input, args.input_ext, args.output, args.output_ext, args.program,
               validate, args.timeout, args.jobs, args.debug)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import glob
import os
import subprocess
import sys


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


def find_matching_file(file, input_folder, target_folder, same_folder=False):
    """
    Find a matching of a file, possibly archived, in the target_folder.
    """
    base_name = os.path.basename(file)
    path_name = file[len(input_folder):len(file) - len(base_name)]
    exts = ['.bz2', '.xz', '.tar.gz', '.tgz', '.gr', '.gr.bz2', '.gr.xz']
    if not same_folder:
        if os.path.isfile(target_folder + path_name + base_name):
            return target_folder + path_name + base_name
        for ext in exts:
            if os.path.isfile(target_folder + path_name + base_name + ext):
                return target_folder + path_name + base_name + ext
    for i in reversed(range(-len(base_name), -1)):
        for ext in exts:
            if os.path.isfile(target_folder + path_name + base_name[:i] + ext):
                return target_folder + path_name + base_name[:i] + ext
    return None


def extract_file_if_necessary(file, tmpdir):
    tmp_file = tmpdir + '/' + os.path.basename(file)
    while os.path.exists(tmp_file):
        tmp_file += '_'
    if file.endswith('.bz2'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['bzcat', file],
                            stdout=f,
                            stderr=f, )
        return tmp_file
    if file.endswith('.xz'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['xzcat', file],
                            stdout=f,
                            stderr=f, )
        return tmp_file
    if file.endswith('.tar.gz'):
        with open(tmp_file, 'w') as f:
            subprocess.call(['tar', '-xOf', tmp_file, os.path.basename(file)[:-len('.tar.gz')]],
                            stdout=f,
                            stderr=f, )
        return tmp_file
    return file


def archive_file(input_file, output_file, ext):
    if ext == '.xz':
        with open(output_file, 'w') as f:
            subprocess.call(['xz', '-c', input_file], stdout=f, stderr=f)
    return


def get_extracted_name(filename):
    arcv = ['.xz', '.bz2', '.zip', '.tgz', '.tar.gz']
    for ext in arcv:
        if filename.endswith(ext):
            return filename[:len(filename) - len(ext)]
    return filename


def create_tmp_dir(tool):
    cmd = 'mktemp --directory --tmpdir=/dev/shm ' + os.path.basename(tool) + '-XXXXXXXX'
    tmp_dir = subprocess.check_output(cmd.split(' '), stderr=sys.stdout)
    return tmp_dir.decode().strip()

#!/usr/bin/env python3
import glob
import os


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


def find_matching_file(file, target_folder, same_folder=False):
    """
    Find a matching of a file, possibly archived, in the target_folder.
    """
    base_name = os.path.basename(file)
    exts = ['.bz2', '.xv', '.tar.gz', '.tgz', '.gr']
    if not same_folder and os.path.isfile(target_folder + '/' + base_name):
        return target_folder + '/' + base_name
    for i in reversed(range(-len(base_name), -1)):
        for ext in exts:
            if os.path.isfile(target_folder + '/' + base_name[:i] + ext):
                return target_folder + '/' + base_name[:i] + ext
    return None

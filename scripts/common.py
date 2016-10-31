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

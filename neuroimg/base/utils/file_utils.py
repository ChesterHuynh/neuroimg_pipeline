# -*- coding: utf-8 -*-

# File writing/reading and manipulations

import glob
import os
from datetime import datetime


def ensure_unique_file(parent_folder, filename):
    final_path = os.path.join(parent_folder, filename)
    while os.path.exists(final_path):
        filename = raw_input(
            "\n\nFile %s already exists. Enter a different name: " %
            final_path)
        final_path = os.path.join(parent_folder, filename)
    return final_path


def change_filename_or_overwrite(path, overwrite=True):
    if overwrite:
        if os.path.exists(path):
            os.remove(path)
        return path

    parent_folder = os.path.dirname(path)
    while os.path.exists(path):
        filename = raw_input("\n\nFile %s already exists. Enter a different name or press enter to overwrite file: "
                             % path)
        if filename == "":
            overwrite = True
            break

        path = os.path.join(parent_folder, filename)

    if overwrite:
        os.remove(path)

    return path


def change_filename_or_overwrite_with_wildcard(path, overwrite=True):
    wild_path = path + "*"
    existing_files = glob.glob(path + "*")
    if len(existing_files) > 0:
        if overwrite:
            for file in existing_files:
                if os.path.exists(file):
                    os.remove(file)
            return path
        else:
            print(
                "The following files already exist for base paths " +
                wild_path +
                " !: ")
            for file in existing_files:
                print(file)
            filename = raw_input(
                "\n\nEnter a different name or press enter to overwrite files: ")
            if filename == "":
                return change_filename_or_overwrite_with_wildcard(
                    path, overwrite=True)
            else:
                parent_folder = os.path.dirname(path)
                path = os.path.join(parent_folder, filename)
                return change_filename_or_overwrite_with_wildcard(
                    path, overwrite)
    else:
        return path


def write_metadata(meta_dict, h5_file, key_date, key_version, path="/"):
    root = h5_file[path].attrs
    root[key_date] = str(datetime.now())
    root[key_version] = 2
    for key, val in meta_dict.iteritems():
        root[key] = val

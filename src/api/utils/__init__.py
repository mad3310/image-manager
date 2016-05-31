__author__ = 'xsank'

import os
import json
import subprocess


def run_cmd(cmdStr):
    if cmdStr == "":
        return ("", 0)
    p = subprocess.Popen(cmdStr, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ret_str = p.stdout.read()
    retval = p.wait()
    return (ret_str, retval)


def is_dir_exists(path):
    return os.path.exists(path)


def object_to_json(obj):
    return json.dumps(obj.__dict__)

def get_file_data(file_path, mode='r'):
    with open(file_path, mode) as f:
        data = f.read()
        f.close()
    return data

def set_file_data(file_path, data, mode='w'):
    with open(file_path, mode) as f:
        f.write(data)
        f.close()
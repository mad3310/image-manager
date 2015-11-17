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

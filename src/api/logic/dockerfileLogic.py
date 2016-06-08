#coding=utf-8

import os, shutil
from tornado.options import options
from utils import get_file_data, set_file_data

def dockerfile_get(owner, app_type, 
                   app_name, app_version='0.0.1'):
    template_path = ('%s/%s/%s/%s/template'
                     %(options.dockerfile_dir,
                       app_type, owner, app_name))
    target_path = ('%s/%s/%s/%s/%s'
                     %(options.dockerfile_dir,
                       app_type, owner, 
                       app_name, app_version)) 
    shutil.copytree(template_path,target_path)
    target_file = '%s/Dockerfile' % target_path 
    dockerfile_old = get_file_data(target_file)
    set_file_data(target_file, 
                  dockerfile_old.format(
                              APP_NAME=app_name,
                              APP_VERSION=app_version)
                 )
    return target_file


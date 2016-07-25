#coding=utf-8

import os, shutil
import logging
from tornado.options import options
from image_manager.utils import get_file_data, set_file_data

def _get_root_path(owner, app_type, app_name):
    path0 = os.path.join(options.dockerfile_dir,
                       app_type)
    path1 = os.path.join(path0, owner)
    path2 = os.path.join(path1, app_name)
    for path in [path2, path1, path0]:
        if os.path.exists(path):
            return path
    logging.error('No dockerfile path can found')

def dockerfile_get(repository, owner, app_type, 
                   app_name, appfile_name, app_version='0.0.1'):
    root_path = _get_root_path(owner, app_type, 
                   app_name)
    template_path = os.path.join(root_path, 'template')
    target_path = os.path.join(root_path, app_version)
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.copytree(template_path, target_path)
    target_file = os.path.join(target_path,'Dockerfile')
    dockerfile_old = get_file_data(target_file)
    set_file_data(target_file, 
                  dockerfile_old.format(
                              REPOSITORY_ADDR = repository,
                              APP_NAME = app_name,
                              APPFILE_NAME = appfile_name,
                              APP_VERSION = app_version)
                 )
    return target_path


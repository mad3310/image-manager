#coding=utf-8

import os, shutil
from tornado.options import options
from image_manager.utils import get_file_data, set_file_data

def dockerfile_get(repository, owner, app_type, 
                   app_name, appfile_name, app_version='0.0.1'):
    template_path = os.path.join(options.dockerfile_dir,
                       app_type, owner, app_name,
                       'template')
    target_path = os.path.join(options.dockerfile_dir,
                       app_type, owner, 
                       app_name, app_version)
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


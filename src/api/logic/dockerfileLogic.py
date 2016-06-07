#coding=utf-8
from tornado.options import options

def dockerfile_get(owner, app_type, app_name):
    target_path = ('%s/%s/%s/%s'
                     %(options.dockerfile_dir,
                       app_type, owner, app_name))
    return target_path


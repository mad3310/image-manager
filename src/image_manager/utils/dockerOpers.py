__author__ = 'xsank'

import logging

from tornado.options import options
from docker import Client

from image_manager.utils.utilOpers import UtilOpers
from image_manager.utils import run_cmd


class DockerOpers(UtilOpers):

    def __init__(self):
        self.client = Client(base_url = 'unix://var/run/docker.sock',
                             version = '1.12')

    @staticmethod
    def get_path_by__type(tp):
        return options.dockerfile_dir + "/%s" % tp

    def build(self, path, tag='', noCache=False):
        streams = self.client.build(tag = tag, path = path,
                nocache = noCache, rm = True)
        res = [line for line in streams]
        return res

    def push(self, repository, tag = ''):
        res = self.client.push(repository, tag)
        return res

    def remove(self, repository, tag = ''):
        image = '%s:%s' %(repository, 
               'latest' if tag == '' else tag)
        res = self.client.remove_image(image)
        return res

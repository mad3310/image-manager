__author__ = 'xsank'

import logging

from tornado.options import options
from docker import Client

from utilOpers import UtilOpers
from utils import run_cmd


class DockerOpers(UtilOpers):

    dockerfile = "Dockerfile"
    registry = "10.160.140.32:5000"

    def __init__(self):
        self.client = Client(base_url='unix://var/run/docker.sock')

    @staticmethod
    def get_path_by__type(tp):
        return options.dockerfile_dir + "/%s" % tp

    def build(self, _type='', tag='', noCache=False):
        _file = open(self.get_path_by__type(_type) + "/%s" % self.dockerfile)
        streams = self.client.build(tag=tag, fileobj=_file, nocache=noCache)
        res = [line for line in streams]
        return res

    def push(self, repository="10.160.140.32:5000", tag=''):
        res = self.client.push(repository, tag)
        return res

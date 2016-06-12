__author__ = 'xsank'

import logging

from tornado.options import options
from docker import Client

from utilOpers import UtilOpers
from utils import run_cmd


class DockerOpers(UtilOpers):

    def __init__(self):
        self.client = Client(base_url='unix://var/run/docker.sock')

    @staticmethod
    def get_path_by__type(tp):
        return options.dockerfile_dir + "/%s" % tp

    def build(self, dockerfile, tag='', noCache=False):
        _file = open(dockerfile)
        streams = self.client.build(tag=tag, fileobj=_file, nocache=noCache)
        res = [line for line in streams]
        return res

    def push(self, image):
        cmd = 'docker push %s' % image
        logging.info('pushing image: %s' % cmd)
        res = run_cmd(cmd)
        #now the current api cannot push tag
        #res = self.client.push(image)
        return res

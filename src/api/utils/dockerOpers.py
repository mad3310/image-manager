__author__ = 'xsank'

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
    def get_path_by_type(tp):
        return options.image_dir + "/%s" % tp

    def build(self, type='', tag='', noCache=False):
        file = open(self.get_path_by_type(type) + "/%s" % self.dockerfile)
        streams = self.client.build(tag=tag, fileobj=file, nocache=noCache)
        res = [line for line in streams]
        return res

    def build2(self, type='', tag=''):
        path = self.get_path_by_type(type)
        total = self.registry + '/' + tag
        cmd = 'cd %s && docker build -t="%s" .' % (path, total)
        res = run_cmd(cmd)
        return res

    def push(self, repository="10.160.140.32:5000", tag=''):
        res = self.client.push(repository, tag)
        return res

    def push2(self, tag=''):
        total = self.registry + '/' + tag
        cmd = "docker push %s" % total
        res = run_cmd(cmd)
        return res

    def pull(self, repository="10.160.140.32:5000", tag=''):
        res = self.client.pull(repository, tag)
        return res

    def pull2(self, tag=''):
        total = self.registry + '/' + tag
        cmd = 'docker pull "%s"' % total
        res = run_cmd(cmd)
        return res

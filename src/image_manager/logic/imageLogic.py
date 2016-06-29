__author__ = 'xsank'

from image_manager.utils.dockerOpers import DockerOpers
from image_manager.logic.result import Results
import logging
from image_manager.utils.zkOpers import zk_handler

def ImageOperRecord(object):
    REV_WORK, BUILDING, PUSHING, FINISHED = \
            '0', '1', '2', '3'

    def __init__(self, repo_name, tag):
        self.node = '%s/%s' %(repo_name, tag)
        
    def set_rev_work(self):
        zk_handler.node_create(self.node)
        zk_handler.value_set(self.node, self.REV_WORK)

    def set_building(self):
        zk_handler.value_set(self.node, self.BUILDING)

    def set_pushing(self):
        zk_handler.value_set(self.node, self.PUSHING)

    def set_finished(self):
        zk_handler.value_set(self.node, self.FINISHED)

    def get_finish(self):
        val = zk_handler.value_get(self.node)
        return val == self.FINISHED

class ImageLogic(object):

    docker_op = DockerOpers.instance()

    def push(self, repository, tag=''):
        res = self.docker_op.push(repository, tag)
        result = Result(not res[1], res[0])
        return str(result)

    def build(self, path, tag = ''):
        res = self.docker_op.build(path, tag)
        result = Result(not res[1], res[0])
        return str(result)

    def remove(self, repository, tag=''):
        self.docker_op.remove(repository, tag)


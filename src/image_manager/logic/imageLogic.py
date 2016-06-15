__author__ = 'xsank'

from image_manager.utils.dockerOpers import DockerOpers
from image_manager.logic.result import Result
import logging

class ImageLogic(object):

    #image_tag = "image_manager/letv_%s_image:%s"

    docker_op = DockerOpers.instance()

    def push(self, repository, tag=''):
        res = self.docker_op.push(repository, tag)
        result = Result(not res[1], res[0])
        return str(result)

    def build(self, path, tag = ''):
        res = self.docker_op.build(path, tag)
        result = Result(not res[1], res[0])
        return str(result)

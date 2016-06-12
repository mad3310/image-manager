__author__ = 'xsank'

from utils.dockerOpers import DockerOpers
from result import Result
import logging

class ImageLogic(object):

    #image_tag = "image_manager/letv_%s_image:%s"

    docker_op = DockerOpers.instance()

    def push(self, image):
        res = self.docker_op.push(image)
        result = Result(not res[1], res[0])
        return str(result)

    def build(self, dockerfile, tag = ''):
        res = self.docker_op.build(dockerfile, tag)
        result = Result(not res[1], res[0])
        return str(result)

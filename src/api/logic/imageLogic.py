__author__ = 'xsank'

from utils.dockerOpers import DockerOpers
from result import Result

class ImageLogic(object):

    image_tag = "image_manager/letv_%s_image:%s"

    docker_op = DockerOpers.instance()

    def push(self, image):
        res = self.docker_op.push2(image)
        result = Result(not res[1], res[0])
        return str(result)

    def build(self, image, _path):
        res = self.docker_op.build2(image, _path)
        result = Result(not res[1], res[0])
        return str(result)

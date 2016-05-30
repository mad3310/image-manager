__author__ = 'xsank'

from utils.gitOpers import GitOpers
from utils.dockerOpers import DockerOpers
from result import Result


image__types = ["zookeeper", "mcluster", "jetty"]


def is_image__type_valid(_type):
    return _type in image__types


def check__type(func):
    def decorate(self, _type, *args):
        if is_image__type_valid(_type):
            res = func(self, _type, *args)
        else:
            res = Result(value="invalid _type")
        return res
    return decorate


class ImageLogic(object):

    image_tag = "image_manager/letv_%s_image:%s"

    git_op = GitOpers.instance()
    docker_op = DockerOpers.instance()

    def get_tag_by__type(self, _type):
        return self.image_tag % (_type, self.git_op.commit_id(_type))

    def pull(self, _type):
        tag = self.get_tag_by__type(_type)
        res = self.docker_op.pull2(tag=tag)
        result = Result(not res[1], res[0])
        return str(result)

    def push(self, image):
        res = self.docker_op.push2(image)
        result = Result(not res[1], res[0])
        return str(result)

    def build(self, image, _path):
        res = self.docker_op.build2(image, _path)
        result = Result(not res[1], res[0])
        return str(result)

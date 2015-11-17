__author__ = 'xsank'

from utils.gitOpers import GitOpers
from utils.dockerOpers import DockerOpers
from result import Result


image_types = ["zookeeper", "mcluster"]


def is_image_type_valid(type):
    return type in image_types


def check_type(func):
    def decorate(self, type, *args):
        if is_image_type_valid(type):
            res = func(self, type, *args)
        else:
            res = Result(value="invalid type")
        return res
    return decorate


class ImageLogic(object):

    image_tag = "image_manager/letv_%s_image:%s"

    git_op = GitOpers.instance()
    docker_op = DockerOpers.instance()

    def get_tag_by_type(self, type):
        return self.image_tag % (type, self.git_op.commit_id(type))

    def pull(self, type):
        tag = self.get_tag_by_type(type)
        res = self.docker_op.pull2(tag=tag)
        result = Result(not res[1], res[0])
        return str(result)

    def push(self, type):
        tag = self.get_tag_by_type(type)
        res = self.docker_op.push2(tag=tag)
        result = Result(not res[1], res[0])
        return str(result)

    def build(self, type):
        if not self.git_op.exists(type):
            self.git_op.clone(type)
        else:
            self.git_op.update(type)
        tag = self.get_tag_by_type(type)
        res = self.docker_op.build2(type=type, tag=tag)
        result = Result(not res[1], res[0])
        return str(result)

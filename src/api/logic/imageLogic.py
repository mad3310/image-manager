__author__ = 'xsank'

from utils.dockerOpers import DockerOpers
from result import Result
import logging

class ImageLogic(object):

    #image_tag = "image_manager/letv_%s_image:%s"

    docker_op = DockerOpers.instance()

    def push(self, repository, tag = ''):
        res = self.docker_op.push(repository, tag)
        result = Result(not res[1], res[0])
        return str(result)

    def build(self, dockerfile, tag = ''):
        logging.info('<<<<<Image Logic, image:%s, path:%s' 
                    %(tag, dockerfile))
        res = self.docker_op.build(dockerfile, tag)
        logging.info('>>>>Image Logic end, image:%s, path:%s' 
                    %(tag, dockerfile))
        result = Result(not res[1], res[0])
        return str(result)

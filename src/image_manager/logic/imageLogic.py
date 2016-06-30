__author__ = 'xsank'

from image_manager.utils.dockerOpers import DockerOpers
from image_manager.logic.result import Result
import logging
import json
from image_manager.utils.zkOpers import zk_handler

class ImageOperRecord(object):
    REV_WORK = dict(code=1, msg='work accept')
    BUILDING = dict(code=2, msg='image building')
    PUSHING = dict(code=3, msg='image pushing')
    REMOVING = dict(code=4, msg='image removing')
    FINISHED = dict(code=0, msg='work finish')

    ERR_BEGIN = 100 

    def __init__(self, repo_name, tag):
        self.node = '%s/%s' %(repo_name, tag)
        
    def set_rev_work(self):
        zk_handler.node_create(self.node)
        zk_handler.value_set(self.node, self.REV_WORK)

    def set_building(self):
        zk_handler.value_set(self.node, self.BUILDING)

    def set_pushing(self):
        zk_handler.value_set(self.node, self.PUSHING)

    def set_error(self, err_code, msg):
        zk_handler.value_set(self.node,
             dict(code=self.ERR_BEGIN+err_code, msg=msg))

    def set_finished(self):
        zk_handler.value_set(self.node, self.FINISHED)

    def get_status(self):
        val = zk_handler.value_get(self.node)
        val['is_finish'] = False
        val['is_err'] = False
        if val['code'] == self.FINISHED['code']:
            val['is_finish'] = True
        if val['code'] > self.ERR_BEGIN:
            val['is_err'] = True
        return val

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


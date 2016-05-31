__author__ = 'xsank'

import logging

from tornado.web import asynchronous
from tornado.gen import engine
from tornado.options import options

from utils.decorators import run_on_executor, run_callback
from handlers.baseHandler import BaseHandler
from logic.imageLogic import is_image__type_valid
from logic.imageLogic import ImageLogic


class ImageHandler(BaseHandler):

    image_logic = ImageLogic()

    @staticmethod
    def check_image(_type):
        if not is_image__type_valid(_type):
            raise Exception("image is invalid")


class ImageBuildHandler(ImageHandler):

    @asynchronous
    @engine
    def post(self,):
        """curl -d "jdk_version=jdk1.7&web_server=resin&app=tethys_1.0.0.1" http://10.154.156.129:9999/image/build
        """
        
        args = self.get_params()
        deploy_env = self.validate_parms('deploy_env', args)
        location = self.validate_parms('location', args)
        jdk_version = self.validate_parms('jdk_version', args)
        web_server = self.validate_parms('web_server', args)
        app = self.validate_parms('app', args)
        
        tag = 'dianshang/%s_%s_%s_%s:%s' % (location, deploy_env, jdk_version, web_server, app)
        image = self.registry + '/' + tag
        dockerfile_path = options.dockerfile_dir + '/%s/%s_%s' % (web_server, jdk_version, app)
        logging.info('build image  : %s' % image)
        res = yield self.block(image, dockerfile_path)
        print res
        self.finish({'image': image})

    @run_on_executor()
    @run_callback
    def block(self, image, dockerfile_path):
        res = self.image_logic.build(image, dockerfile_path)
        return res


class ImagePushHandler(ImageHandler):

    @asynchronous
    @engine
    def post(self,):
        """curl -d "image=10.160.140.32:5000/dianshang/dlyl_jdk1.7_resin:tethys_1.0.0.1" http://10.154.156.129:9999/image/push
        """
        
        args = self.get_params()
        image = args.get('image')
        logging.info('image to be pushed to image store : %s' % image)
        res = yield self.block(image)
        self.finish(res)

    @run_on_executor()
    @run_callback
    def block(self, image):
        res = self.image_logic.push(image)
        return res


class ImagePullHandler(ImageHandler):

    @run_on_executor()
    @run_callback
    def block(self, _type):
        res = self.image_logic.pull(_type)
        return res

    @asynchronous
    @engine
    def post(self, *args, **kwargs):
        args = self.get_params()
        _type = args["_type"]
        self.check_image(_type)
        _type = "letv_zookeeper_image"
        res = yield self.block(_type)
        self.finish(res)

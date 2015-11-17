__author__ = 'xsank'

from tornado.web import asynchronous
from tornado.gen import engine
from async.core import run_on_executor, run_callback

from handlers.baseHandler import BaseHandler
from logic.imageLogic import is_image_type_valid
from logic.imageLogic import ImageLogic


class ImageHandler(BaseHandler):

    image_logic = ImageLogic()

    @staticmethod
    def check_image(type):
        if not is_image_type_valid(type):
            raise Exception("image is invalid")


class ImageBuildHandler(ImageHandler):

    @run_on_executor()
    @run_callback
    def block(self, type):
        res = self.image_logic.build(type)
        return res

    @asynchronous
    @engine
    def post(self, *args, **kwargs):
        args = self.get_params()
        type = args["type"]
        self.check_image(type)
        type = "letv_zookeeper_image"
        res = yield self.block(type)
        self.finish(res)


class ImagePushHandler(ImageHandler):

    @run_on_executor()
    @run_callback
    def block(self, type):
        res = self.image_logic.push(type)
        return res

    @asynchronous
    @engine
    def post(self, *args, **kwargs):
        args = self.get_params()
        type = args["type"]
        self.check_image(type)
        type = "letv_zookeeper_image"
        res = yield self.block(type)
        self.finish(res)


class ImagePullHandler(ImageHandler):

    @run_on_executor()
    @run_callback
    def block(self, type):
        res = self.image_logic.pull(type)
        return res

    @asynchronous
    @engine
    def post(self, *args, **kwargs):
        args = self.get_params()
        type = args["type"]
        self.check_image(type)
        type = "letv_zookeeper_image"
        res = yield self.block(type)
        self.finish(res)

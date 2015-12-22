__author__ = 'xsank'

from tornado.web import asynchronous
from tornado.gen import engine
from async.core import run_on_executor, run_callback

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

    @run_on_executor()
    @run_callback
    def block(self, _type):
        res = self.image_logic.build(_type)
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


class ImagePushHandler(ImageHandler):


    @asynchronous
    @engine
    def post(self, *args, **kwargs):
        args = self.get_params()
        _type = args["_type"]
        self.check_image(_type)
        res = yield self.block(_type)
        self.finish(res)

    @run_on_executor()
    @run_callback
    def block(self, _type):
        res = self.image_logic.push(_type)
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

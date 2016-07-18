__author__ = 'xsank'

import os
import logging
import logging.config
import tornado.options
from image_manager.appdefine import appDefine
tornado.options.parse_command_line()

from tornado.options import options
config_path = os.path.join(options.base_dir, "config")
logging.config.fileConfig(config_path + '/logging.conf')

import tornado.web
import tornado.ioloop
import tornado.httpserver
from image_manager.routes import handlers
from image_manager.utils import zkOpers

class Application(tornado.web.Application):

    def __init__(self):
        super(Application, self).__init__(handlers=handlers)


def main():
    tornado.options.parse_command_line()
    zkOpers.zk_handler.conn()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

__author__ = 'xsank'

import os
import logging
import logging.config

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options

from appdefine import appDefine
from routes import handlers


class Application(tornado.web.Application):

    def __init__(self):
        super(Application, self).__init__(handlers=handlers)


def main():
    tornado.options.parse_command_line()
    config_path = os.path.join(options.base_dir, "config")
    logging.config.fileConfig(config_path + '/logging.conf')
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

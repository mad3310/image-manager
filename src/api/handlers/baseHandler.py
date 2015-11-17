__author__ = 'xsank'

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def get_params(self):
        params = {}
        args = self.request.arguments
        for k in args:
            params[k] = args[k][0]
        return params

    def block(self, *args):
        raise Exception("this method should be implemented")

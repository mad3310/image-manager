__author__ = 'xsank'

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    registry = "192.168.211.131:5000"

    def get_params(self):
        params = {}
        args = self.request.arguments
        for k in args:
            params[k] = args[k][0]
        return params

    @staticmethod
    def validate_parms(param, params):
        assert param in params
        return params.get(param)

    def block(self, *args):
        raise Exception("this method should be implemented")

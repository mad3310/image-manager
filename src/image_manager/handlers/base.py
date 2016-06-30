#coding = utf-8
from tornado.web import RequestHandler
import logging

class UserDefineExcept(Exception):
    def __init__(self, err_code, err_msg = 'unknown'):
        self.code = err_code
        self.msg = msg 

def catch_error(err_code, err_msg):
    def _catch_error(func):
        def wrapper(self, *args):
            try:
                func(self, *args)
                return 0
            except Exception as e:
                logging.error(e, exc_info=True)
                raise UserDefineExcep(err_code, err_msg)
        return wrapper
    return _catch_error

class BaseHandler(RequestHandler):
    
    def finish(self, chunk = None):
        if chunk is None:
            chunk = {}
        if isinstance(chunk, dict):
            if 'error_code' not in chunk.keys():
                chunk = {"meta": {"code": 200}, "response": chunk}
            else:
                chunk = {"meta": {"code ": 401}, "response": chunk}

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(BaseHandler, self).finish(chunk)
 

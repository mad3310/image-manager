#coding = utf-8
from tornado.web import RequestHandler

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
 

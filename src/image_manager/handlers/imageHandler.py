#coding = utf-8

import logging
from concurrent.futures import ThreadPoolExecutor

from tornado.web import asynchronous, RequestHandler
from tornado.gen import coroutine, Return
from tornado.options import options

from image_manager.logic.imageLogic import ImageLogic
from image_manager.logic.dockerfileLogic import dockerfile_get 

thread_pool = ThreadPoolExecutor(4)

class ImageBuildHandler(RequestHandler): 
    registry_addr = "192.168.211.131:5000"
    image_logic = ImageLogic()

    @asynchronous
    @coroutine
    def post(self):
        """
        curl -d "owner=dianshang&app_type=jdk1.7_resin&app_name=tethys_1.0.0.1" 
        http://10.154.156.129:9999/image/build
        """
        owner = self.get_argument('owner', None)
        app_type = self.get_argument('app_type', None)
        app_name = self.get_argument('app_name', None) 
        app_version = self.get_argument('app_version', '0.0.1')
        if not (owner and app_type and app_name):
            self.set_status(500)
            self.finish({'msg':'invalid para'})
            Return
        self.finish({'msg':'building image, please wait....'})
        yield thread_pool.submit(self._image_build,
            owner, app_type, app_name, app_version)

    def _image_build(self, owner, app_type, 
                     app_name, app_version='0.0.1'):
        self.registry = '%s/%s/%s_%s' % (
                              self.registry_addr, 
                              owner, app_type, 
                              app_name)
        self.tag = app_version
        self.image = '%s:%s'  %(self.registry, self.tag)
        dockerfile_path = dockerfile_get(owner, app_type, 
                                   app_name, app_version)
        logging.info('build image:%s' % self.image)
        try:
            self.__image_build(self.registry, self.tag, 
                               dockerfile_path)
        except Exception as e:
            logging.error(e, exc_info=True)

    def __image_build(self, registry, tag, dockerfile_path):
        res = None
        try:
            logging.info('building image begin: %s, dockerfile:%s' 
                         % (self.image, dockerfile_path))
            res = self.image_logic.build(dockerfile_path,
                                        self.image)
            logging.info('building image end, begin push: %s' 
                         % self.image)
            res = self.image_logic.push(registry, tag)
            logging.info('push image end: %s' % self.image)
        except Exception as e:
            logging.error(e, exc_info=True)
        return res


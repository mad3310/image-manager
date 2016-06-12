__author__ = 'xsank'

import logging

from tornado.web import asynchronous
from tornado.gen import engine
from tornado.options import options

from utils.decorators import run_on_executor, run_callback
from handlers.baseHandler import BaseHandler
from logic.imageLogic import ImageLogic
from logic.dockerfileLogic import dockerfile_get 

class ImageHandler(BaseHandler):

    image_logic = ImageLogic()

class ImageBuildHandler(ImageHandler): 

    @asynchronous 
    @engine
    def post(self):
        """
        curl -d "owner=dianshang&app_type=jdk1.7_resin&app_name=tethys_1.0.0.1" 
        http://10.154.156.129:9999/image/build
        """
        args = self.get_params()
        owner = self.validate_parms('owner', args)
        app_type = self.validate_parms('app_type', args)
        app_name = self.validate_parms('app_name', args) 
        
        self._image_build(owner, app_type, app_name, '0.0.2')
        self.finish({'msg':'building image, please wait....'})

    @engine
    def _image_build(self, owner, app_type, 
                     app_name, app_version='0.0.1'):
        tag = '%s/%s/%s_%s:%s' % (self.registry, owner, app_type, 
                               app_name, app_version)
        dockerfile_path = dockerfile_get(owner, app_type, 
                                   app_name, app_version)
        logging.info('build image:%s' % tag)
        try:
            yield self.__image_build(tag, dockerfile_path)
        except Exception as e:
            logging.error(e, exc_info=True)
            self.set_status(500)
            self.write({'detail':('image %s build fail'
                        % tag)})

    @run_on_executor()
    @run_callback
    def __image_build(self, tag, dockerfile_path):
        res = None
        try:
            logging.info('building image begin: %s, dockerfile:%s' 
                         % (tag, dockerfile_path))
            res = self.image_logic.build(dockerfile_path,
                                        tag)
            logging.info('building image end, begin push: %s' 
                         % tag)
            res = self.image_logic.push(tag)
            logging.info('building push end: %s' % tag)
        except Exception as e:
            logging.error(e, exc_info=True)
            self.set_status(500)
            self.write({'detail':('image %s build or push fail'
                        % tag)})
        return res

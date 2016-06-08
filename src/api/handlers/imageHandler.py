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
        
        self._image_build(owner, app_type, app_name)
        if self.tag:
            self._image_push()
        self.finish()


    @engine
    def _image_build(self, owner, app_type, 
                     app_name, app_version='0.0.1'):
        tag = '/%s/%s:%s-%s' % (owner, app_type, 
                               app_name, app_version)
        dockerfile_path = dockerfile_get(owner, app_type, 
                                   app_name, app_version)
        logging.info('build image:%s, tag:%s' 
                   % (self.registry, tag))
        self.tag = None
        try:
            yield self.__image_build(tag, dockerfile_path)
            self.tag = tag
        except Exception as e:
            logging.error(e, exc_info=True)
            self.set_status(500)
            self.write({'detail':('image %s%s build fail'
                        % (image, tag))})

    @engine
    def _image_push(self):
        logging.info('image to be pushed : %s%s'
                     % (self.image, self.tag))
        try:
            yield self.__image_push()
            self.write({'image': self.image, 
                        'tag': self.tag})
        except Exception as e:
            logging.error(e, exc_info=True)
            self.set_status(500)
            self.write({'detail':('image %s%s push fail' 
                                  % (self.image, self.tag))})

    @run_on_executor()
    @run_callback
    def __image_build(self, tag, dockerfile_path):
        logging.info('build image  : %s%s, dockerfile:%s' 
                     % (self.registry, tag, dockerfile_path))
        res = self.image_logic.build(dockerfile_path,
                                    tag)
        return res

    @run_on_executor()
    @run_callback
    def __image_push(self):
        res = self.image_logic.push(self.registry, 
                                    self.tag)
        return res


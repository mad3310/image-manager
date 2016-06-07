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
        
        yield self._image_build(owner, app_type, app_name)
        if self.image:
            yield self._image_push(self.image) 
        self.finish()

    @engine
    def _image_build(self, owner, app_type, 
                     app_name)
        tag = '%s/%s:%s' % (owner, app_type, app_name)
        image = self.registry + '/' + tag
        dockerfile_path = dockerfile_get(owner, app_type, 
                                         app_name)
        logging.info('build image  : %s' % image)
        self.image = None
        try:
            yield self.__image_build(image, dockerfile_path)
            self.image = image
        except Exception as e:
            logging.error(e, exc_info=True)
            self.set_status(500)
            self.write({'detail':('image %s build fail'
                        % image)})

    @engine
    def _image_push(self, image):
        logging.info('image to be pushed : %s'
                     % image)
        try:
            yield self.__image_push(self.image)
            self.write({'image': self.image})
        except Exception as e:
            logging.error(e, exc_info=True)
            self.set_status(500)
            self.write({'detail':('image %s push fail' 
                                  % self.image)})

    @run_on_executor()
    @run_callback
    def __image_build(self, image, dockerfile_path):
        res = self.image_logic.build(image, dockerfile_path)
        return res

    @run_on_executor()
    @run_callback
    def __image_push(self, image):
        res = self.image_logic.push(image)
        return res


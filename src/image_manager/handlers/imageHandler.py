#coding = utf-8

import logging
import os.path
from concurrent.futures import ThreadPoolExecutor

from tornado.web import asynchronous, RequestHandler
from tornado.gen import coroutine, Return
from tornado.options import options

from image_manager.logic.imageLogic import ImageLogic
from image_manager.logic.dockerfileLogic import dockerfile_get 
from image_manager.logic.app_load import s3Oper
thread_pool = ThreadPoolExecutor(10)

class ImageBuildHandler(RequestHandler): 

    image_logic = ImageLogic()

    @asynchronous
    @coroutine
    def post(self):
        """
        curl -d "owner=dianshang&app_type=jdk1.7_resin&app_name=tethys_1.0.0.1" 
        http://10.154.156.129:9999/image/build
        """
        self.registry_addr = options.registry_addr
        owner = self.get_argument('owner', None)
        app_type = self.get_argument('app_type', None)
        app_name = self.get_argument('app_name', None) 
        self.tag = self.get_argument('app_version', '0.0.1')
        appfile_name = self.get_argument(
                                'appfile_name', None)
        self.appfile_s3_bucket = self.get_argument(
                                'appfile_s3_bucket', None)
        self.appfile_s3_key    = self.get_argument(
                                'appfile_s3_key', None)
        #TODO input para check

        self.registry = '%s/%s/%s_%s' % (
                              self.registry_addr, 
                              owner, app_type,
                              app_name)
        self.image = '%s:%s'  %(self.registry, self.tag)
        self.dockerfile_path = dockerfile_get(self.registry_addr,
                               owner, app_type, app_name, 
                               appfile_name, self.tag)
        self.appfile_fullpath  = os.path.join(self.dockerfile_path,
                             'files', appfile_name)
        self.finish({'msg':'building image, please wait....'})
        yield thread_pool.submit(self._image_build)

    def _image_build(self):
        dockerfile_path = self.dockerfile_path 
        logging.info('build image:%s' % self.image)
        try:
            #down load app file
            s3 = s3Oper(options.s3_host, options.s3_access_key,
                        options.s3_secret_key)
            logging.info('download appfile %s begin......' 
                         % self.appfile_fullpath)
            s3.file_download(self.appfile_s3_bucket,
                          self.appfile_s3_key,
                          self.appfile_fullpath)
            logging.info('download appfile %s end' 
                         % self.appfile_fullpath)
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


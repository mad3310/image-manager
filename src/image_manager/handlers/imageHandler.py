#coding = utf-8

import logging
import os.path
from concurrent.futures import ThreadPoolExecutor

from tornado.web import asynchronous, RequestHandler
from tornado.gen import coroutine, Return
from tornado.options import options

from image_manager.logic.imageLogic import ImageLogic, ImageOperRecord
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
        owner = str(self.get_argument('owner', None))
        app_type = self.get_argument('app_type', None)
        app_name = self.get_argument('app_name', None) 
        self.tag = self.get_argument('app_version', '0.0.1')
        self.registry = self.get_argument('repo_name')
        appfile_name = self.get_argument(
                                'appfile_name', None)
        self.s3_host = self.get_argument(
                                'awss3endpoint', options.s3_host)
        self.s3_access_key = self.get_argument(
                                'accessKey', options.s3_access_key)
        self.s3_secret_key = self.get_argument(
                                'secretKey', options.s3_secret_key)
        self.appfile_s3_bucket = self.get_argument(
                                'appfile_s3_bucket', None)
        self.appfile_s3_key    = self.get_argument(
                                'appfile_s3_key', None)
        #TODO input para check
        
        self.image = '%s:%s'  %(self.registry, self.tag)
        self.image_oper_rec = ImageOperRecord(self.registry, self.tag)
        yield thread_pool.submit(self.image_oper_rec.set_rev_work)
        self.dockerfile_path = dockerfile_get(options.registry_addr,
                               owner, app_type, app_name, 
                               appfile_name, self.tag)
        self.appfile_fullpath  = os.path.join(self.dockerfile_path,
                             'files', appfile_name)
        self.finish({'msg':'building image, please wait....'})
        yield thread_pool.submit(self._image_build)
        yield thread_pool.submit(self.image_oper_rec.set_finished)

    def _image_build(self):
        dockerfile_path = self.dockerfile_path 
        logging.info('build image:%s' % self.image)
        try:
            #down load app file
            s3 = s3Oper(self.s3_host, self.s3_access_key,
                        self.s3_secret_key)
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
            self.image_oper_rec.set_building()
            res = self.image_logic.build(dockerfile_path,
                                        self.image)
            logging.info('building image end, begin push: %s' 
                         % self.image)
            self.image_oper_rec.set_pushing()
            res = self.image_logic.push(registry, tag)
            logging.info('push image end: %s' % self.image)
            logging.info('delete image %s from local, begin' 
                         % self.image)
            self.image_logic.remove(registry, tag)
            logging.info('delete image %s from local, end' 
                         % self.image)
        except Exception as e:
            logging.error(e, exc_info=True)
        return res


class ImageQueryHandler(RequestHandler):

    STATUS_UNKOWN = 0
    STATUS_SUCC = 1
    @coroutine
    def post(self, repo_name, tag):
        self.registry, self.tag = repo_name, tag
        self.image_oper_rec = ImageOperRecord(self.registry, self.tag)
        ret = yield thread_pool.submit(self.image_oper_rec.set_finish)
        msg = 'success' if ret else 'unkown'
        code = self.STATUS_SUCC if ret else self.STATE_UNKOWN
        self.write(dict(code=code,
             message='build %s %s' % (self.image, msg)))



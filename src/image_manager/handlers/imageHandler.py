#coding = utf-8

import logging
import os.path
from concurrent.futures import ThreadPoolExecutor
import urllib
from tornado.web import asynchronous, RequestHandler
from tornado.gen import coroutine, Return
from tornado.options import options
from base import BaseHandler, catch_error, UserDefineExcept
from image_manager.logic.imageLogic import ImageLogic, ImageOperRecord
from image_manager.logic.dockerfileLogic import dockerfile_get 
from image_manager.logic.app_load import s3Oper
thread_pool = ThreadPoolExecutor(10)

ERR_PARA_UNVALID, ERR_DOWNLOAD, ERR_DOCKERFILE, \
   ERR_BUILD, ERR_PUSH, ERR_IMG_RM = 1, 2, 3, 4, 5, 6

class ImageBuildHandler(BaseHandler): 

    image_logic = ImageLogic()

    @catch_error(ERR_PARA_UNVALID, 'please check input para')
    def _para_get(self):
        self.owner = str(self.get_argument('owner', None))
        self.app_type = self.get_argument('app_type', None)
        self.app_name = self.get_argument('app_name', None) 
        self.tag = self.get_argument('app_version', '0.0.1')
        self.registry = self.get_argument('repo_name')
        self.appfile_name = self.get_argument(
                                'appfile_name', None)
        s3_host = self.get_argument('awss3endpoint', options.s3_host)
        if s3_host.startswith('http'):
            _, rest = urllib.splittype(s3_host)
            s3_host, _ = urllib.splithost(rest)
        self.s3_host = s3_host
        self.s3_access_key = self.get_argument(
                                'accessKey', options.s3_access_key)
        self.s3_secret_key = self.get_argument(
                                'secretKey', options.s3_secret_key)
        self.appfile_s3_bucket = self.get_argument(
                                'appfile_s3_bucket', None)
        self.appfile_s3_key    = self.get_argument(
                                'appfile_s3_key', None)
        self.image = '%s:%s'  %(self.registry, self.tag)
        self.image_oper_rec = ImageOperRecord(self.registry, self.tag)

    @catch_error(ERR_DOCKERFILE, 'dockerfile cannot found')
    def _dockerfile_get(self):
        self.dockerfile_path = dockerfile_get(options.registry_addr,
                               self.owner, self.app_type, self.app_name, 
                               self.appfile_name, self.tag)
        self.appfile_fullpath  = os.path.join(self.dockerfile_path,
                             'files', self.appfile_name)

    @catch_error(ERR_DOWNLOAD, 'appfile download err')
    def _appfile_load(self):
        s3 = s3Oper(self.s3_host, self.s3_access_key,
                    self.s3_secret_key)
        logging.info('download appfile %s begin......' 
                     % self.appfile_fullpath)
        s3.file_download(self.appfile_s3_bucket,
                      self.appfile_s3_key,
                      self.appfile_fullpath)
        logging.info('download appfile %s end' 
                     % self.appfile_fullpath)

    @catch_error(ERR_BUILD, 'image build fail')
    def _image_build(self):
        logging.info('building image begin: %s, dockerfile:%s' 
                     % (self.image, self.dockerfile_path))
        self.image_oper_rec.set_building()
        res = self.image_logic.build(self.dockerfile_path,
                                    self.image)
        logging.info('building image end: %s' 
                     % self.image)

    @catch_error(ERR_PUSH, 'image push fail')
    def _image_push(self):
        logging.info('push image begin: %s' % self.image)
        self.image_oper_rec.set_pushing()
        res = self.image_logic.push(self.registry, self.tag)
        logging.info('push image end: %s' % self.image)

    @catch_error(ERR_IMG_RM, 'image remove fail')
    def _image_remove(self):
        self.image_logic.remove(self.registry, self.tag)

    @asynchronous
    @coroutine
    def post(self):
        """
        curl -d "owner=dianshang&app_type=jdk1.7_resin&app_name=tethys_1.0.0.1" 
        http://10.154.156.129:9999/image/build
        """
        try:
            self._para_get() 
            yield thread_pool.submit(self.image_oper_rec.set_rev_work)
            self._dockerfile_get()
            self.finish(dict(msg='building image, please wait....'))
            #yield thread_pool.submit(self._appfile_load)
            #yield thread_pool.submit(self._image_build)
            #yield thread_pool.submit(self._image_push)
            yield thread_pool.submit(self._image_remove)
            yield thread_pool.submit(self.image_oper_rec.set_finished)
        except UserDefineExcept, e:
            yield thread_pool.submit(self.image_oper_rec.set_error, e.code, e.msg)

class ImageQueryHandler(BaseHandler):

    @coroutine
    def post(self):
        self.registry = self.get_argument('repo_name')
        self.tag = self.get_argument('app_version', '0.0.1')
        self.image_oper_rec = ImageOperRecord(self.registry, self.tag)
        retval = yield thread_pool.submit(self.image_oper_rec.get_status)
        msg = retval['msg'] 
        if retval['is_finish']:
            msg = 'success'
        ret = dict(message='build %s:%s %s' % (self.registry, self.tag, msg))
        if retval['is_err']: 
            ret['error_code'] = retval['code']
        self.finish(ret)


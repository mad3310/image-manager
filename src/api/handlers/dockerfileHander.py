
import re
import logging
import os

from tornado.web import asynchronous
from tornado.options import options


from handlers.baseHandler import BaseHandler
from utils import get_file_data, set_file_data


class DockerfileBuildHandler(BaseHandler):

    @asynchronous
    def post(self,):
        """curl -d "jdk_version=jdk1.7&web_server=tomcat&app=tethys-1.0.0.1" http://10.154.156.129:9999/dockerfile/build
        
        """

        args = self.get_params()
        
        deploy_env = self.validate_parms('deploy_env', args)
        location = self.validate_parms('location', args)
        jdk_version = self.validate_parms('jdk_version', args)
        web_server = self.validate_parms('web_server', args)
        app = self.validate_parms('app', args)
        
        _web_server_path = os.path.join(options.dockerfile_dir, web_server)
        template_path = os.path.join(_web_server_path, 'template')
        app_dir_path = os.path.join(_web_server_path, '%s_%s' % (jdk_version, app) )
        
        if not os.path.exists(app_dir_path):
            cp_cmd = 'cp -r %s %s' % (template_path, app_dir_path)
            os.system(cp_cmd)
        
        father_tag = 'dianshang/%s_%s_%s_%s:0.0.1' % (location, deploy_env, jdk_version, web_server)
        father_image = self.registry + '/' + father_tag
        
        app_dockerfile = os.path.join(app_dir_path, 'Dockerfile')
        dockerfile_old = get_file_data(app_dockerfile)
        
        replaced_father_image = re.findall('FROM (.*)', dockerfile_old)[0]
        replaced_app = re.findall('ENV APP_NAME (.*)', dockerfile_old)[0]
        
        dockerfile_new = dockerfile_old.replace(replaced_father_image, father_image)
        
        dockerfile_new = dockerfile_new.replace(replaced_app, app)
        set_file_data(app_dockerfile, dockerfile_new)
        logging.info('dockerfile content : \n%s' % dockerfile_new)
        
        self.finish({'data' : dockerfile_new})

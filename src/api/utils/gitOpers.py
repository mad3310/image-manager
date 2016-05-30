__author__ = 'xsank'

from tornado.options import options

from utilOpers import UtilOpers
from configOpers import ConfigOpers
from utils import run_cmd, is_dir_exists


class GitOpers(UtilOpers):

    def __init__(self):
        self.username = ConfigOpers.instance().get_value(options.git_property, "username")
        self.password = ConfigOpers.instance().get_value(options.git_property, "password")
        self.valid_url = "http://" + self.username + ":" + \
            self.password + "@git.letv.cn/letv_image/%s.git"

    def get_url_by_type(self, tp):
        return self.valid_url % tp

    @staticmethod
    def get_path_by_type(tp):
        return options.dockerfile_dir + "/%s" % tp

    def exists(self, tp):
        path = self.get_path_by_type(tp)
        return is_dir_exists(path)

    def clone(self, tp=""):
        url = self.get_url_by_type(tp)
        #url = "http://mazheng:admin!12@git.letv.cn/mazheng/letv_zookeeper_image.git"
        cmd = "cd %s && git clone %s" % (options.dockerfile_dir, url)
        run_cmd(cmd)

    def update(self, tp):
        path = self.get_path_by_type(tp)
        run_cmd("cd %s && git pull origin master" % path)

    def commit_id(self, tp):
        path = self.get_path_by_type(tp)
        cmd = 'cd ' + path + ' && git log -1 --pretty=format:"%h"'
        res = run_cmd(cmd)
        if not res[1]:
            return res[0].strip()
        return "badval"

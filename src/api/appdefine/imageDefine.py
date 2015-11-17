__author__ = 'xsank'

import os

from tornado.options import define


dirname = os.path.dirname
join = os.path.join
base_dir = os.path.abspath(dirname(dirname(__file__)))

define('port', default=3721, type=int, help='app listen port')
define("base_dir", default=base_dir, help="project base dir")
define("image_dir", default=join(base_dir, "images"), help="image dir")

define("git_property", default=join(
    base_dir, "config", "git.property"), help="git property")

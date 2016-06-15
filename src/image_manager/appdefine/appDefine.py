__author__ = 'xsank'

import os

from tornado.options import define


dirname = os.path.dirname
join = os.path.join
base_dir = os.path.abspath(dirname(dirname(__file__)))

define('port', default=9999, type=int, help='app listen port')
define("base_dir", default=base_dir, help="project base dir")
define("dockerfile_dir", default=join(base_dir, "dockerfile"), help="dockerfile dir")

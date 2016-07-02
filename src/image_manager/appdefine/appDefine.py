__author__ = 'xsank'

import os

from tornado.options import define


dirname = os.path.dirname
join = os.path.join
base_dir = os.path.abspath(dirname(dirname(__file__)))

define('port', default=9999, type=int, help='app listen port')
define('base_dir', default=base_dir, help='project base dir')
define('dockerfile_dir', default=join(base_dir, 'dockerfile'), 
        help='dockerfile dir')
define('registry_addr', default='192.168.211.131:5000', 
        help='registry_addr')
define('s3_host', default='s3.lecloud.com', help='s3 host')
define('s3_access_key', default='EH18VA68TUPMOF4L5MK3',
        help='s3 access key')
define('s3_secret_key', 
        default='Y3KW8LAyVcTNS1cAnPEv847lUmtFXILVg+8gXaIo',
        help='s3 secret key')
define('zkrootPath', default='/letv/imagemanager', help='zookeeper root path')
define('zkaddress', default='127.0.0.1', help='zookeeper host')
define('zkport', default='2181', help='zookeeper port')

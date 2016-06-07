__author__ = 'xsank'

from handlers.imageHandler import *

handlers = [
    (r"/image/build", ImageBuildHandler),
]

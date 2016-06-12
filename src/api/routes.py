__author__ = 'xsank'

from handlers.imageHandler import *

handlers = [
    (r"/image/BuildPush", ImageBuildHandler),
]

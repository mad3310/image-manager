__author__ = 'xsank'

from image_manager.handlers.imageHandler import *

handlers = [
    (r"/image/BuildPush", ImageBuildHandler),
]

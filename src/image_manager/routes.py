__author__ = 'xsank'

from image_manager.handlers.imageHandler import *
from image_manager.handlers.base import HealthCheckHandler
handlers = [
    (r"/image/BuildPush", ImageBuildHandler),
    (r"/image/BuildQuery", ImageQueryHandler),
    (r"/", HealthCheckHandler),
]

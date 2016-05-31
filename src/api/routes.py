__author__ = 'xsank'

from handlers.imageHandler import *
from handlers.dockerfileHander import DockerfileBuildHandler


handlers = [
    (r"/dockerfile/build", DockerfileBuildHandler),
    (r"/image/build", ImageBuildHandler),
    (r"/image/push", ImagePushHandler),
    (r"/image/pull", ImagePullHandler),
]

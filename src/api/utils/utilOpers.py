__author__ = 'xsank'


class UtilOpers(object):

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

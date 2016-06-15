#coding=utf-8

class Result(object):

    def __init__(self, success=False, value=''):
        self.result = 'success' if success else 'failed'
        self.value = value

    def __repr__(self):
        return str(self.__dict__)

#coding=utf-8

from image_manager.utils.utilOpers import UtilOpers


class ConfigOpers(UtilOpers):

    @staticmethod
    def get_value(filename, key, separator="="):
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if line.find(separator) > 0 and line.find(key) >= 0:
                    return line.split(separator)[1].strip()
        return ''

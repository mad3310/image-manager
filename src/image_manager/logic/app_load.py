#coding=utf-8
import boto
import boto.s3.connection
from boto.s3.key import Key

class s3Oper(object):
    def __init__(self, host, access_key, secret_key):
        self.conn = boto.connect_s3(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            host = host, is_secure = False,
            calling_format = boto.s3.connection.OrdinaryCallingFormat())

    def file_download(self, bucket, key, filename):
        bucket = self.conn.create_bucket(
                      bucket)
        self.key = bucket.get_key(key)
        fp = open(filename, 'wb')
        self.key.get_contents_to_file(fp)

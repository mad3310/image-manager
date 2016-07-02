#coding=utf-8

import logging
import json
from kazoo.client import KazooClient, KazooState
from kazoo.retry import KazooRetry
from tornado.options import options

class ZkOpers(object):

    '''
    classdocs
    '''
    def __init__(self):
        self.rootPath = options.zkrootPath
        self.zkaddress = options.zkaddress
        self.zkport = options.zkport
        if "" != self.zkaddress and "" != self.zkport:
            self.host = '%s:%s' % (self.zkaddress, self.zkport)
            self.DEFAULT_RETRY_POLICY = KazooRetry(
                max_tries=None,
                max_delay=10000,
            )

    def conn(self):
        try:
            self.zk = KazooClient(
                    hosts = self.host,
                    connection_retry = self.DEFAULT_RETRY_POLICY,
                    timeout = 20)
            self.zk.add_listener(self.listener)
            self.zk.start()
            logging.info("instance zk client (%s:%s)" 
                    % (self.zkaddress, self.zkport))
        except Exception as e:
            logging.error("connect to zk (%s) failed" % self.host)
            raise

    def close(self):
        try:
            self.zk.stop()
            self.zk.close()
        except Exception, e:
            logging.error(e)

    def stop(self):
        try:
            self.zk.stop()
        except Exception as e:
            logging.error(e, exc_info = True)
            raise

    def listener(self, state):
        if state == KazooState.LOST:
            logging.info("zk connect lost, stop this "
                         "connection and then start new one!")
        elif state == KazooState.SUSPENDED:
            logging.info("zk connect suspended, stop this "
                         "connection and then start new one!")
        else:
            pass

    def is_connected(self):
        return self.zk.state == KazooState.CONNECTED

    def re_connect(self):
        zk = KazooClient(
             hosts=self.host, connection_retry=self.DEFAULT_RETRY_POLICY)
        zk.start()
        self.zk = zk
        return self.zk

    def node_create(self, node):
        path = ('%s/%s') %(self.rootPath, node) 
        self.DEFAULT_RETRY_POLICY(self.zk.ensure_path, path)

    def value_set(self, node, value):
        path = ('%s/%s') %(self.rootPath, node) 
        self.DEFAULT_RETRY_POLICY(self.zk.set,
                               path, json.dumps(value))

    def value_get(self, node):
        path = ('%s/%s') %(self.rootPath, node) 
        ret, _ = self.DEFAULT_RETRY_POLICY(self.zk.get, path)
        return json.loads(ret)

zk_handler = ZkOpers()

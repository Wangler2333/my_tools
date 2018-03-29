#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/10/26上午11:16
# @Author   : Saseny Zhou
# @Site     : 
# @File     : collect_log_module.py
# @Software : PyCharm Community Edition


import os
import logging.config


class log_collection(object):
    def __init__(self, log_path=None, debug_log=None):
        self.log_path = log_path
        self.debug_log = debug_log
        self.define_message()
        self.check_log_path()
        self.define_dic()

    def define_message(self):
        self.debug_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                            ' [%(levelname)s][%(message)s]'
        self.log_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        self.display_format = '[%(levelname)s][%(asctime)s] %(message)s'

    def check_log_path(self):
        try:
            for i in [self.log_path, self.debug_log]:
                dict = os.path.dirname(i)
                if not os.path.isdir(dict):
                    os.makedirs(dict)
        except:
            print('create log path folder fail')

    def define_dic(self):
        self.config_info = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': self.debug_format
                },
                'simple': {
                    'format': self.log_format
                },
                'id_simple': {
                    'format': self.display_format
                },
            },
            'filters': {},
            'handlers': {
                # 打印到终端的日志
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',  # 打印到屏幕
                    'formatter': 'id_simple'
                },
                # 打印到文件的日志,收集info及以上的日志
                'default': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                    'formatter': 'standard',
                    'filename': self.debug_log,  # 日志文件
                    'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
                    'backupCount': 5,
                    'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                },
                'boss': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                    'formatter': 'simple',
                    'filename': self.log_path,  # 日志文件
                    'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
                    'backupCount': 5,
                    'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                },
            },
            'loggers': {
                # logger1=logging.getLogger(__name__)拿到的logger配置
                '': {
                    'handlers': ['default', 'console', 'boss'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                    'level': 'DEBUG',
                    'propagate': True,  # 向上（更高level的logger）传递
                },
                # logger1=logging.getLogger('collect')拿到的logger配置
                # 'collect': {
                #    'handlers': ['boss', ],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                #    'level': 'DEBUG',
                #    'propagate': True,  # 向上（更高level的logger）传递
                # },
            },
        }

    def run(self):
        logging.config.dictConfig(self.config_info)
        self.logger = logging.getLogger(__name__)

    def add_mesaage(self, message):
        self.logger.info(message)


if __name__ == '__main__':
    pass

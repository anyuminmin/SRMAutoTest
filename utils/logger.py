#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import os.path
from utils.config import Config
import logging
import time


def singleton(cls):
	cls.instance = None

	def get_instance(*args, **kwargs):
		if not cls.instance:
			cls.instance = cls(*args, **kwargs)
		return cls.instance

	return get_instance


@singleton
class Logger:

	def __init__(self, logger):
		"""指定保存日志的文件路径，日志级别，以及调用文件将日志存入到指定的文件中"""
		# 读取配置文件中的日志设置
		cf = Config()
		self.log_dir = cf.get_value("log.conf", "basiclog", "log_dir")
		self.format = cf.get_value("log.conf", "basiclog", "format")

		#创建一个logger
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)

		cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		# print('root path--->', root_path)
		logfile_path = os.path.join(root_path, self.log_dir)
		# print('file path --->', file_path)

		# 输出日志到文件的nandler
		file_name = cur_date + ".log"
		log_file = os.path.join(logfile_path, file_name)
		fh = logging.FileHandler(log_file, encoding = 'UTF-8')
		fh.setLevel(logging.DEBUG)

		# 再创建一个handler,用于输出到控制台
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# 定义nandler的输出格式
		formatter = logging.Formatter(self.format)
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		# 给logger添加nandler
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)


if __name__ == '__main__':
	log = Logger(logger='logger').logger
	package_path = os.path.dirname(os.path.dirname(__file__))
	print('package_path:', package_path)
	# file_path = os.path.join(package_path, 'log dir')
	# print(file_path)
	# print(os.path.dirname(os.path.dirname(__file__)))


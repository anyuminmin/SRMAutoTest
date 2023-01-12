#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import configparser
import os
from utils.read_config import ReadConfig


class Config:

	def __init__(self):
		self.config_folder = "config"

	@property
	def get_all_config(self):
		return ReadConfig()

	def get_value(self, file_name, section, key):
		"""
		读取配置文件
		:param file name:配置文件名称
		param section:配置文件中的section
		:param key:配置文件中的key
		"""
		try:
			config = self.read_config_file(file_name)
			value = config.get(section, key)
			return value
		except Exception as e:
			print("获取value失败："+str(e))

	def set_value(self, file_name, section, key, value):
		"""
		写入配置文件
		:param file name:记置文件名称
		:param section: 配置文件中的section
		:param key:配置文件中的key
		:param value:配置文件中的key对应的value
		"""
		try:
			config = self.read_config_file(file_name)
			config.add_section(section)
			config.set(section,key,value)
			config.write(open(self.get_file_path(file_name),"w+"))
		except Exception as e:
			print("设置value失败："+str(e))

	def update_value(self, file_name, section, key, value):
		"""
		修改配置文件
		:param file name:配置文件名称
		:param section:配置文件中的section
		:param key:配置文件中的key
		:param value:配置文件中的key对应的value
		"""
		try:
			config = self.read_config_file(file_name)
			config.set(section,key,value)
			config.write(open(self.get_file_path(file_name),"r+"))
		except Exception as e:
			print("更新value失败："+str(e))

	def remove_option(self, file_name, section, key):
		"""
		移除配置文件中某个key
		:param file name:配置文件名称
		:param section:配置文件中的section
		:param key:配置文件中的key
		"""
		try:
			config = self.read_config_file(file_name)
			config.remove_option(section, key)
			config.write(open(self.get_file_path(file_name), "r+"))
		except Exception as e:
			print("移除key失败：" + str(e))

	def remove_section(self, file_name, section):
		"""
		移除配置文件中某个section
		:param file_name: 配置文件名称
		:param section: 配置文件中的section
		"""
		try:
			config = self.read_config_file(file_name)
			config.remove_section(section)
			config.write(open(self.get_file_path(file_name), "r+"))
		except Exception as e:
			print("移除section失败："+str(e))

	def read_config_file(self, file_name):
		"""
		读取配置文件
		:param file_name: 配置文件名称
		"""
		try:
			config = configparser.ConfigParser()
			file_path = self.get_file_path(file_name)
			config.read(file_path, encoding='UTF-8')
			return config
		except Exception as e:
			print("读取config.文件失败：" + str(e))

	def get_file_path(self, file_name):
		"""
		读取文件所在路径，默认读取Config.文件夹的文件，如需修改，实例化类时，传文件夹名称
		注意：只能读取com.note包及子包下的文件
		:param file_name: 文件名称
		"""
		root_path = os.path.dirname(os.path.dirname(__file__))
		config_dir_path = os.path.join(root_path, self.config_folder)
		# print('配置文件目录地址--->'，config.yaml dir path)
		file_path = os.path.join(config_dir_path, file_name)
		return file_path


if __name__ == '__main__':
	config = Config()
	f = config.get_file_path('config.yaml')
	print(f)
	# print(config.get_value("log.conf", "filehandlerlog", "level"))




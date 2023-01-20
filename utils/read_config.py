#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import os
import yaml


class ReadConfig(object):
	base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + os.sep
	config_path = base_path + "config" + os.sep

	def __init__(self, *args):
		if len(args) == 0:
			self.env = self.__get_envyaml()["env"]
		else:
			self.env = args[0]

	def get_env(self):
		return self.__get_envyaml()['env']

	def get_branch(self):
		return self.__get_envyaml()['branch']

	def __get_envyaml(self):
		"""
		解析yaml
		:return:s字典
		"""
		path = self.config_path + 'config.yaml'
		try: # 兼容2和3版本
			with open(path, encoding="utf-8")as f:
				s = yaml.safe_load(f)
		except:
			with open(path)as f:
				s = yaml.safe_load(f)
		return s.decode() if isinstance(s, bytes) else s

	def __get_yaml(self):
		"""
		解析yaml
		:return:s字典
		"""
		path = self.config_path + 'config_' + self.env + '.yaml'
		try:  # 兼容2和3版本
			with open(path, encoding="utf-8")as f:
				s = yaml.safe_load(f)
		except Exception:
			with open(path)as f:
				s = yaml.safe_load(f)
		return s.decode() if isinstance(s, bytes) else s


	@property
	def user(self):
		return self.__get_yaml()["user"]

	@property
	def user2(self):
		return self.__get_yaml()["user2"]

	# @property
	def url(self):
		return self.__get_yaml()["url"]

	@property
	def shopId(self):
		return self.__get_yaml()["shopId"]

	@property
	def shopId2 (self):
		return self.__get_yaml()["shopId2"]

	@property
	def shopId3(self):
		return self.__get_yaml()["shopId3"]

	@property
	def shopName (self):
		return self.__get_yaml()["shopName"]

	@property
	def shopName2 (self):
		return self.__get_yaml()["shopName2"]

	@property
	def shopName3(self):
		return self.__get_yaml()["shopName3"]


	@property
	def mysql(self):
		return self.__get_yaml()["mysql"]

	def get_yaml_uri_path(self):
		root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		yaml_uri_path = os.path.join(root_path, 'resource/uriYaml')
		return yaml_uri_path

	def get_yaml_param_path(self):
		root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		yaml_param_path = os.path.join(root_path, 'resource/paramsYaml')
		return yaml_param_path

	# @property
	def get_url(self, FileName, param, domain="srm_buyer_url"):
		"""
		默认加载srm_buyer_url的url
		FileName:文件路径
		:param: yaml文件中uri的key
		url: 登录域名
		"""
		domain = self.url()[domain]
		with open(f'{self.get_yaml_uri_path()}/{FileName}', 'r', encoding='utf-8')as f:
			ele_info = f.read()
			yaml_dict = yaml.safe_load(ele_info)
		uri = yaml_dict[param]
		return domain + '/api' + uri

	# @property
	def get_param(self, FileName, param):
		"""
		默认加载srm_buyer_url的url
		FileName:文件路径
		:param: yaml文件中param的key
		url: 登录域名
		"""
		with open(f'{self.get_yaml_param_path()}/{FileName}', 'r', encoding='utf-8')as f:
			ele_info = f.read()
			yaml_dict = yaml.safe_load(ele_info)
		return yaml_dict[param]


if __name__ == '__main__':
	read = ReadConfig()
	# print(read.get_url("SRM/public/uri.yaml", "SRM_LOGIN"))
	print(read.get_param("SRM/public/base.yaml", "HEADERS"))
	# print(read.srm_uri_path)



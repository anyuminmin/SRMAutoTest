#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import configparser
import os
import yaml


class readConfig(object):

	def base_dir(self, filename='config.yaml'):
		return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml', filename)

	def getMysql(self,environment='test_srm'):
		' ''获取环境的配置'''
		_dict = {}
		config = configparser.ConfigParser()
		config.read(self.base_dir('mysqlConfig.ini'))
		_dict["IP"] = config.get(environment, 'IP')
		_dict["PORT"] = int(config.get(environment, 'PORT'))
		_dict["DB"] = config.get(environment, 'DB')
		_dict["username"] = config.get(environment, 'username')
		_dict["password"] = config.get(environment, 'password')
		return _dict

	def filePath(self, fileDir, fileName):
		return os.path.join(os.path.dirname(os.path.dirname(__file__)), fileDir, fileName)

	def readYaml(self, fileDir, fileName):
		' ''获取列的具体值dictConfig（）'''
		with open(self.filePath(fileDir=fileDir, fileName=fileName), 'r', encoding="utf-8") as f:
			return yaml.safe_load(f)

	def readConfigYaml(self):
		with open(self.filePath('config.yaml', 'config.yaml'), 'r', encoding="utf-8") as f:
			_envParams = yaml.safe_load(f)['env']
		return self.readYaml('config.yaml', 'config_'+_envParams+'.paramsYaml')

	def writeYaml(self, content, fileDir='writeData', fileName='address.paramsYaml'):
		with open(self.filePath(fileDir, fileName), 'w', encoding="utf-8") as f:
			f.writelines(content)


if __name__ == '__main__':
	read = readConfig()
	print(read.base_dir())


#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from utils.readConfig import readConfig


class requestBody(readConfig):
	def getUrl(self, uri, uriFileName="uri.paramsYaml"):
		"""默认获取uri.yaml文件中的uri，以后有多个文件时，可自定义文件"""
		url = self.readConfigYaml()['servers']['testSrm']
		uri = self.readYaml('data', uriFileName)[uri]  # 从ymal文件读取uri
		return url+'/api'+uri

	def getParamsBody(self, paramsKey, parmsFileName="params.paramsYaml"):
		"""默认获取params.yaml文件中的params，以后有多个文件时，可自定义文件"""
		"""获取请求参数"""
		return self.readYaml("data", parmsFileName)[paramsKey]

	def getLoginUser(self, product="SRM"):
		"""获取登录账号、默认SRM产品"""
		return self.readConfigYaml()[product]['user']

	def getLoginPsd(self, product="SRM"):
		"""获取登录账号密码"""
		return self.readConfigYaml()[product]['password']

	def getLoginShopId(self, product="SRM"):
		"""获取配置中的shopId"""
		return self.readConfigYaml()[product]['shopId']

	def getCompanyName(self, product="SRM"):
		"""获取配置中的name，公司名称"""
		return self.readConfigYaml()[product]['name']

	def getLoginShopId2(self, product="SRM"):
		"""获取配置中的shopId"""
		return self.readConfigYaml()[product]['shopId2']

	def getCompanyName2(self, product="SRM"):
		"""获取配置中的name，公司名称"""
		return self.readConfigYaml()[product]['name2']

	def getMes(self, product="SRM"):
		"""获取配置中的name，公司名称"""
		return self.readConfigYaml()[product]

	def getHeaders(self):
		"""获取当前登录的shopId"""
		return self.readConfigYaml()['JsonHeader']

	def getConfigSupplierFile(self):
		return self.readConfigYaml()['supplierFile']

	def getPublicParams(self):
		return self.readConfigYaml()['publicParams']

# if __name__ == '__main__':
# 	hea=requestBody()
# 	print(hea.getConfigSupplierFile())






#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import os
import requests
import yaml
import json
from utils.logger import Logger
import urllib3
from utils.read_config import ReadConfig

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log = Logger("BaseService").logger
read = ReadConfig()
token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'token.yaml')
headers = read.get_param("SRM/public/base.yaml", "HEADERS")
with open(token_path, 'r', encoding='utf-8')as f:
	token = yaml.safe_load(f)


class BaseService(object):

	def post_json(self, url, data, shop="'采购方西子清洁能源装备制造有限公司'"):
		headers["X-PH-TOKEN"] = token[shop]
		rsp = requests.post(
			url=url,
			headers=headers,
			json=data
		)
		return rsp

	def get_json(self, url, data, shop='采购方西子清洁能源装备制造有限公司'):
		headers["X-PH-TOKEN"] = token[shop]
		return requests.get(
			url=url,
			data=data,
			headers=headers
		)

	def return_and_assert(self, response, interfaceName, isSuccess):
		if isSuccess and not response.json()['success']:
			response = response.content.decode("utf-8")
			raise BaseException(interfaceName + "接口失败，响应为：" + response)
		else:
			return response


if __name__ == '__main__':
	h = BaseService()

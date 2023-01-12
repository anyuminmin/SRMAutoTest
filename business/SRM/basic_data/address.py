#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from services.httpService import HttpService
from utils.read_config import ReadConfig
read_config = ReadConfig()
http = HttpService()


class Address:

	def add_new_address(self, paramDict):
		url = read_config.get_url("SRM/basic_data/address.yaml", "SAVE_ADDRESS")
		param = read_config.get_param("SRM/basic_data/address.yaml", "SAVE_ADDRESS")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp

	def select_address(self, paramDict):
		url = read_config.get_url("SRM/basic_data/address.yaml", "SELECT_ADDRESS")
		param = read_config.get_param("SRM/basic_data/address.yaml", "SELECT_ADDRESS")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp

	def delete_address(self, paramDict):
		url = read_config.get_url("SRM/basic_data/address.yaml", "DELETE_ADDRESS")
		param = read_config.get_param("SRM/basic_data/address.yaml", "DELETE_ADDRESS")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp

	def update_address(self, paramDict):
		url = read_config.get_url("SRM/basic_data/address.yaml", "UPDATE_ADDRESS")
		param = read_config.get_param("SRM/basic_data/address.yaml", "UPDATE_ADDRESS")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp
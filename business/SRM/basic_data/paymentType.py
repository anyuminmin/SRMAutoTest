#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from services.httpService import HttpService
from utils.read_config import ReadConfig
read_config = ReadConfig()
http = HttpService()


def get_paymentType(paramDict):
	"""获取结算方式"""
	url = read_config.get_url("SRM/basic_data/payment_type.yaml", "GET_PAYMENT_TYPE")
	param = read_config.get_param("SRM/basic_data/payment_type.yaml", "GET_PAYMENT_TYPE")
	for i in paramDict:
		param[i] = paramDict.get(i)
	rsp = http.post_json(
		url=url,
		data=param
	)
	return rsp.json()
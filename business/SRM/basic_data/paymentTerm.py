#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from services.httpService import HttpService
from utils.read_config import ReadConfig
read_config = ReadConfig()
http = HttpService()


def get_paymentTerm(paramDict):
	"""获取付款条件"""
	url = read_config.get_url("SRM/basic_data/payment_term.yaml", "GET_PAYMENT_TERM")
	param = read_config.get_param("SRM/basic_data/payment_term.yaml", "GET_PAYMENT_TERM")
	for i in paramDict:
		param[i] = paramDict.get(i)
	rsp = http.post_json(
		url=url,
		data=param
	)
	return rsp.json()
#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import json

from utils.operationMysql import mysqlUtils
from utils.requestBody import requestBody
from testcases.SRM.sourcing.template import test_template
import requests
import random
import pytest

requestBody = requestBody()


# 获取报价明细模板信息
def getQuotationCode(json_headers):
	response = requests.post(
		url=requestBody.getUrl("SRM_QUOTATION_FUZZY_QUERY"),
		headers=json_headers,
		json=requestBody.getParamsBody("SRM_QUOTATION_FUZZY_QUERY")
	)
	return response.json()['data']['list']


# 获取报价明细detail
def getQuotationDetail(json_headers, num):#num:0、1、、
	_body = requestBody.getParamsBody("SRM_QUOTATION_DETAIL")
	assert getQuotationCode(json_headers)[num] != [], "无报价模板相关信息，请查看"
	_body['id'] = getQuotationCode(json_headers)[num]['id']
	response = requests.post(
		url=requestBody.getUrl("SRM_QUOTATION_DETAIL"),
		headers=json_headers,
		json=_body
	)
	return response.json()['data']


# 报价明细传参，格式："inquiryQuotationTemplate": {
# 				"quotationTemplateId": "69",
# 				"quotationData": "[{\"id\":1,\"sds\":23}]"
# 			}
def setParams(json_headers, num=0):
	_data = getQuotationDetail(json_headers, num)
	list = []
	quotationData = {}
	quotationData['id'] = 1
	for i in range(1, len(_data['detailList'])):
		quotationData[_data['detailList'][i]['columnCode']] = 20
	list.append(quotationData)
	return _data['id'], list


# def test(json_headers):
# 	print(setParams(json_headers))

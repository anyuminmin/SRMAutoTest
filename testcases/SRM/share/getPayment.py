#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.operationMysql import mysqlUtils
from utils.requestBody import requestBody
from testcases.SRM.sourcing.template import test_template
import requests
import random
import pytest
requestBody = requestBody()


# 获取币种
def getCurrencyId(json_headers):
	response = requests.post(
			url=requestBody.getUrl("SRM_SHARE_CURRENCY"),
			headers=json_headers,
			json=requestBody.getParamsBody("SRM_SHARE_CURRENCY")
		)
	return response.json()['data']['list'][0]


# 获取付款条款 businessId: "539223256875155456"
# creatorId: "539223256862572544"
# defaultType: 0
# gmtCreate: "2021-05-18 14:26:25"
# gmtModified: "2021-05-18 14:26:25"
# id: "844219378463442945"
# lastModifierId: "539223256862572544"
# list: null
# shopId: "539223256875155457"
# status: 1
# tenantId: "539223256875155458"
# termCode: "A"
# termName: "A"
def getPaymentTerm(json_headers):
	response = requests.post(
			url=requestBody.getUrl("SRM_PAYMENT_TERM"),
			headers=json_headers,
			json=requestBody.getParamsBody("SRM_PAYMENT_TERM")
		)
	return response.json()['data']['list'][0]


# 获取付款方式 businessId: "539223256875155456"
# creatorId: "539223256862572544"
# defaultType: 0
# gmtCreate: "2021-04-20 17:13:47"
# gmtModified: "2021-04-20 17:13:47"
# id: "834114638979303424"
# lastModifierId: "539223256862572544"
# payTypeCode: "0"
# payTypeName: "0"
# shopId: "539223256875155457"
# status: 1
# tenantId: "539223256875155458"
def getPaymentType(json_headers):
	response = requests.post(
			url=requestBody.getUrl("SRM_PAYMENT_TYPE"),
			headers=json_headers,
			json=requestBody.getParamsBody("SRM_PAYMENT_TYPE")
		)
	return response.json()['data']['list'][0]

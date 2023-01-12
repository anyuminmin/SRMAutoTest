#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from utils.requestBody import requestBody
import requests
import pytest
import json
import random

requestBody = requestBody()
shopId = requestBody.getLoginShopId()


def save_supplier_pool(json_headers):
	_body = requestBody.getParamsBody("MES_SAVE_SUPPLIER_POOL")
	_body['supplierPoolCode'] = "supplierPoolCode" + str(random.randint(0, 1000))
	_body['supplierPoolName'] = "supplierPoolName" + str(random.randint(0, 1000))
	response = requests.post(
		url=requestBody.getUrl("MES_SAVE_SUPPLIER_POOL"),
		headers=json_headers,
		json=_body
	)
	assert response.json()['status'] == 0
	assert response.json()['success'] is True
	return response.json()['data']


def test_select_supplier_pool(json_headers):
	' ''默认查询列表，且将第一行数据写到文件中'''
	_body = requestBody.getParamsBody("MES_SELECT_SUPPLIER_POOL")
	_body['supplierPoolCode'] = ""
	response = requests.post(
		url=requestBody.getUrl("MES_SELECT_SUPPLIER_POOL"),
		headers=json_headers,
		json=_body
	)
	assert response.json()['status'] == 0
	assert response.json()['success'] is True
	if not response.json()['data']['list']:
		requestBody.writeYaml(json.dumps(save_supplier_pool(json_headers)), 'writeData', 'supplierPool.paramsYaml')
	else:
		requestBody.writeYaml(json.dumps(response.json()['data']['list'][0]), 'writeData', 'supplierPool.paramsYaml')


# 从配置中获取刚写进去的数据
def get_data():
	return requestBody.readYaml('writeData', 'supplierPool.paramsYaml')


_supplierPoolCode = get_data()['supplierPoolCode']
_supplierPoolName = get_data()['addressName']
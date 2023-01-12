#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import requests
from utils.requestBody import requestBody

'''提供供应商档案查询列表接口'''
_requestBody = requestBody()
_supplierPhone = _requestBody.getConfigSupplierFile()['phone1']


def test_supplierProfile(json_headers, telePhone, supplierName):
	'' '根据电话号码或名称查询，供应商档案列表'''
	body = _requestBody.getParamsBody("MES_SELECT_SUPPLIER_PROFILE")
	body['telePhone'] = telePhone
	body['supplierName'] = supplierName
	response = requests.post(
		url=_requestBody.getUrl("MES_SELECT_SUPPLIER_PROFILE"),
		headers=json_headers,
		json=body
	)
	print("-------------")
	print(response.json())
	assert response.json()['success']is True, response.json()
	assert response.json()['messages'][0]['message'] != '', response.json()
	return response.json()


def test_getSupplierCode(json_headers, telePhone=_supplierPhone, supplierName=None):
	'''根据供应商名称查询后，获取供应商code
	默认从配置拿填报人手机，默认不根据名称查询'''
	suppliers = test_supplierProfile(json_headers, telePhone, supplierName)['data']['list']
	assert suppliers != [], "该供应商不存在"  # 判断获取不到供应商时，抛异常，获取到继续往下走
	supplierCode = []
	for i in range(0, len(suppliers)):
		supplierCode.append(suppliers[i]['supplierCode'])
	return supplierCode


def test_getSupplierType(json_headers, telePhone=_supplierPhone, supplierName=None):
	'''根据供应商名称查询后，获取供应商type
	默认从配置拿填报人手机，默认不根据名称查询'''
	suppliers = test_supplierProfile(json_headers, telePhone, supplierName)['data']['list']
	assert suppliers != [], "该供应商不存在"  # 判断获取不到供应商时，抛异常，获取到继续往下走
	supplierType = []
	for i in range(0, len(suppliers)):
		supplierType.append(suppliers[i]['supplierTypeName'])
	return supplierType


def test_getShopId(json_headers, telePhone=_supplierPhone, supplierName=None):
	'''获取供应商的shopid
	默认从配置拿填报人手机，默认不根据名称查询'''
	suppliers = test_supplierProfile(json_headers, telePhone, supplierName)['data']['list']
	assert suppliers != [], "该供应商不存在"  # 判断获取不到供应商时，抛异常，获取到继续往下走
	_shopId = []
	for i in range(0, len(suppliers)):
		_shopId.append(suppliers[i]['shopId'])
	return _shopId


def test_getRelationId(json_headers, telePhone=_supplierPhone, supplierName=None):
	'''获取供应商档案id
	默认从配置拿填报人手机，默认不根据名称查询'''
	suppliers = test_supplierProfile(json_headers,telePhone,supplierName)['data']['list']
	assert suppliers != [], "该供应商不存在"  # 判断获取不到供应商时，抛异常，获取到继续往下走
	_releationId = []
	for i in range(0, len(suppliers)):
		_releationId.append(suppliers[i]['id'])
	return _releationId


def test_getSupplierName(json_headers, telePhone=_supplierPhone, supplierName=None):
	'''获取供应商档案名称
	默认从配置拿填报人手机，默认不根据名称查询'''
	suppliers = test_supplierProfile(json_headers,telePhone,supplierName)['data']['list']
	assert suppliers != [], "该供应商不存在"  # 判断获取不到供应商时，抛异常，获取到继续往下走
	_supplierName = []
	for i in range(0, len(suppliers)):
		_supplierName.append(suppliers[i]['supplierName'])
	return _supplierName


def test(json_headers):
	print(test_supplierProfile(json_headers))

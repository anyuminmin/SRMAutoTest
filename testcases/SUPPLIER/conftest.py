#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import pytest
import requests
from utils.requestBody import requestBody
import urllib3
from utils.readConfig import readConfig
from testcases.SRM.supplierCertification.supplierFile.test_supplierProfile import test_getShopId
from testcases.SRM.supplierCertification.supplierFile.test_supplierProfile import test_getRelationId
from testcases.SRM.supplierCertification.supplierFile.test_supplierProfile import test_getSupplierName
urllib3.disable_warnings()

# supplier方登录
# 获取登录相关配置
_requestBody = requestBody()
_readConfig = readConfig()
user = _requestBody.getLoginUser('SUPPLIER')
psw = _requestBody.getLoginPsd('SUPPLIER')
JsonHeaders = _requestBody.getHeaders()
# _supplierName="5.11号邀约注册13：42修改名称"
_supplierName = _requestBody.getConfigSupplierFile()['supplierName']
# _supplierName="2021"


def supplier_login():
	' ''supplier方登录'''
	'''从prams.yaml文件中获取参数，并替换其用户名密码'''
	parms = _requestBody.getParamsBody("SUPPLIER_LOGIN", "SUPPLIER_params.paramsYaml")
	parms['accountNo'] = user
	parms['password'] = psw
	response = requests.post(
		url=_requestBody.getUrl("SUPPLIER_LOGIN", "SUPPLIER_uri.paramsYaml"),
		headers=JsonHeaders,
		json=parms,
		verify=False
	)
	assert response.json()['data'] is not None, response.json()
	return response.json()['data']['securityToken']  # 返回securityToken


def supplier_choose_shop(json_headers):
	' ''通过login返回的shopId的list和securityToken，作为入参，然后该接口获取到token'''
	'''从prams.yaml文件中获取参数，并替换其用户名密码'''
	_dict = _requestBody.getParamsBody("SUPPLIER_CHOOSE_SHOP", "SUPPLIER_params.paramsYaml")
	_dict['securityToken'] = str(supplier_login())
	_dict['shopId'] = test_getShopId(json_headers, supplierName=_supplierName)[0]
	_dict['relationName'] = test_getSupplierName(json_headers, supplierName=_supplierName)[0]
	_dict['relationId'] = test_getRelationId(json_headers, supplierName=_supplierName)[0]
	response = requests.post(
		url=_requestBody.getUrl("SUPPLIER_CHOOSE_SHOP", "SUPPLIER_uri.paramsYaml"),
		headers=JsonHeaders,
		json=_dict
	)
	assert response.json()['success'] is True, response.json()
	return response.json()['data']['token']


@pytest.fixture(scope="session")
def supplier_headers(json_headers):
	' ''application/json;charset=UTF-8'''
	token = supplier_choose_shop(json_headers)
	JsonHeaders['cookie'] = "x-ph-token=" + token
	JsonHeaders['x-ph-token'] = token
	assert token is not None, "token为null"
	return JsonHeaders

#
# if __name__ == '__main__':
# 	print("test------>")

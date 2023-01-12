#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.requestBody import requestBody
import requests
import random
import pytest
requestBody = requestBody()


def test_select_template(json_headers):
	response = requests.post(
		url=requestBody.getUrl("SRM_SELECT_TEMPLATE"),
		headers=json_headers,
		json=requestBody.getParamsBody("SRM_SELECT_TEMPLATE")
	)
	return response.json()['data']['list'][0]  # 返回该list响应参数


def test_update_template(json_headers):
	_selectBody = test_select_template(json_headers)
	_body = requestBody.getParamsBody("SRM_UPDATE_TEMPLATE")
	_body['id'] = _selectBody['id']
	_body['businessId'] = _selectBody['businessId']
	_body['creatorId'] = _selectBody['creatorId']
	_body['creatorName'] = _selectBody['creatorName']
	_body['lastModifierId'] = _selectBody['lastModifierId']
	_body['templateNo'] = _selectBody['templateNo']
	response = requests.post(
		url=requestBody.getUrl("SRM_UPDATE_TEMPLATE"),
		headers=json_headers,
		json=_body
	)
	assert response.json()['success'] is True, response.json()


def test_template(json_headers):
	test_update_template(json_headers)
	return test_select_template(json_headers)

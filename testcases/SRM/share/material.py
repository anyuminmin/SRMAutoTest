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


def getMaterial(json_headers):
	_body = requestBody.getParamsBody("SRM_MATERIAL")
	_body['targetShopId'] = requestBody.getLoginShopId()
	response = requests.post(
			url=requestBody.getUrl("SRM_MATERIAL"),
			headers=json_headers,
			json=_body
		)
	return response.json()['data']['list']



def test(json_headers):
	print(getMaterial(json_headers))
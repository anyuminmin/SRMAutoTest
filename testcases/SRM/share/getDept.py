#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.requestBody import requestBody
from conftest import choose_shop
import requests

requestBody = requestBody()


# 获取当前用户部门
def getDept(json_headers):
	_body = requestBody.getParamsBody("SRM_SHOP_DEPT")
	_body['ids'] = [choose_shop()[1]]
	_body['directShopId'] = requestBody.getLoginShopId()
	response = requests.post(
			url=requestBody.getUrl("SRM_SHOP_DEPT"),
			headers=json_headers,
			json=_body
		)
	return response.json()['data'][0]

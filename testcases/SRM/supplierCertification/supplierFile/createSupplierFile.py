#!/user/bin/env python
# -*-  -*-
# author:yumin An

import requests
from utils.requestBody import requestBody

_requestBody = requestBody()


def saveCustomizeForm(json_headers, phone):
	parms = _requestBody.getParamsBody("MES_SAVE_SUPPLIER_CUSTOMIZEFORM")
	parms['components'][1]['children'][6]['data']['value'] = phone
	response = requests.post(
		url=_requestBody.getUrl("MES_SAVE_SUPPLIER_CUSTOMIZEFORM"),
		headers=json_headers,
		json=parms
	)
	return response.json()


def saveSupplier(json_headers, supplierName, phone, taxNo):
	' ''说明：自定义供应商名称、手机号、统一信用代码'''
	prams = _requestBody.getParamsBody("MES_SAVE_SUPPLIER")  # 从配置中获取初始参数
	prams['supplierName'] = supplierName
	prams['telephone'] = phone
	prams['taxNo'] = taxNo
	prams['formDataCode'] = saveCustomizeForm(json_headers, phone)['data']
	response = requests.post(
		url=_requestBody.getUrl("MES_SAVE_SUPPLIER"),
		headers=json_headers,
		json=prams
	)
	return response  # 返回供应商id

# if __name__ == '__main__':
# 	saveSupplier(jsonHeaders)


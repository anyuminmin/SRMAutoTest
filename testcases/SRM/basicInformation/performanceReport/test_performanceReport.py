#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import requests
from utils.requestBody import requestBody
import pytest
from testcases.SRM.supplierCertification.supplierFile.test_supplierProfile import test_getSupplierCode
from utils.readConfig import readConfig
import urllib3
import json
urllib3.disable_warnings()
requestBody = requestBody()
readConfig = readConfig()


# 新增绩效报告
@pytest.fixture()
def test_1insert(json_headers):
	_saveParams = requestBody.getParamsBody("MES_SAVE_PERFORMANCE_REPORT")  # 获取初始参数
	_saveParams['supplierCode'] = test_getSupplierCode(json_headers)[0]
	response = requests.post(
		url=requestBody.getUrl("MES_SAVE_PERFORMANCE_REPORT"),
		headers=json_headers,
		json=_saveParams
	)
	assert response.status_code == 200
	assert response.json()['success'] is True
	print(response.json())
	return _saveParams


# @pytest.fixture()
def test_2select(json_headers, test_1insert):
	' ''根据入参查询指定数据，方便删除'''
	_data = requestBody.getParamsBody("MES_SELECT_PERFORMANCE_REPORT")
	_data['supplierCode'] = test_1insert['supplierCode']
	response = requests.post(
		url=requestBody.getUrl('MES_SELECT_PERFORMANCE_REPORT'),
		headers=json_headers,
		json=_data,
		verify=False
	)
	assert response.status_code == 200
	assert response.json()['success'] is True
	if response.json()['data']['list'] is []:
		requestBody.writeYaml(json.dumps(test_1insert), 'writeData', 'performanceReport.paramsYaml')
	else:
		requestBody.writeYaml(json.dumps(response.json()['data']['list'][0]), 'writeData', 'performanceReport.paramsYaml')


# 从配置中获取刚写进去的数据
def get_data():
	return requestBody.readYaml('writeData', 'performanceReport.paramsYaml')


_id = get_data()['id']
_supplierCode = get_data()['supplierCode']
_examDate = get_data()['examDate']
_supplierType = get_data()['supplierType']


# 新增异常测试
@pytest.mark.parametrize('supplierCode,examDate,supplierType,isSuccess,message', [
	pytest.param(_supplierCode, _examDate, _supplierType, False, "不允许同供应商同考核期数据存在"),
	pytest.param("", '2021/04', '类型随意', False, "供应商不存在")
], ids=[
	"数据唯一性校验",
	"供应商有效性校验"
])
def test_insert_api(json_headers, supplierCode, examDate, supplierType, isSuccess, message):
	_data = {"supplierCode": supplierCode, "examDate": examDate, "supplierType": supplierType,
	"sumScore": 1234.56789111, "sumOrder": "1", "deliveredScore": 100, "deliveredPromptness": 78.12345678}
	response = requests.post(
		url=requestBody.getUrl("MES_SAVE_PERFORMANCE_REPORT"),
		headers=json_headers,
		json=_data
	)
	assert response.json()['success'] == isSuccess, "接口返回与预期不一致"
	assert response.json()['messages'][0]['message'] == message, "接口校验与预期不一致"


def test_export(json_headers):
	' ''导出测试'''
	param = requestBody.getParamsBody("MES_EXPORT_PERFORMANCE_REPORT")
	param['list'] = [_id]
	response = requests.post(
		url=requestBody.getUrl("MES_EXPORT_PERFORMANCE_REPORT"),
		headers=json_headers,
		json=param,
		verify=False
	)
	print(response.json()['data'])
	assert response.status_code == 200
	assert response.json()['success'] is True


# 更新操作
def test_update(json_headers, test_1insert):
	_body = requestBody.getParamsBody("MES_UPDATE_PERFORMANCE_REPORT")  # 获取初始参数
	_body['supplierCode'] = test_1insert['supplierCode']  # 该参数需与新增保持一致
	_body['examDate'] = test_1insert['examDate']
	_body['qualityOrder'] = "修改为B"
	_body['id'] = _id
	response = requests.post(
		url=requestBody.getUrl("MES_UPDATE_PERFORMANCE_REPORT"),
		headers=json_headers,
		json=_body,
		verify=False
	)
	assert response.json()['success'] is True


# 更新之后查询校验
def test_select_for_update(json_headers, test_1insert):
	_data = requestBody.getParamsBody("MES_SELECT_PERFORMANCE_REPORT")
	_data['supplierCode'] = test_1insert['supplierCode']
	response = requests.post(
		url=requestBody.getUrl('MES_SELECT_PERFORMANCE_REPORT'),
		headers=json_headers,
		json=_data,
		verify=False
	)
	assert response.status_code == 200
	assert response.json()['success'] is True
	assert response.json()['data']['list'][0]['qualityOrder'] == "修改为B"


def test_3del(json_headers):
	body = requestBody.getParamsBody("MES_DELETE_PERFORMANCE_REPORT")
	body['list'] = [_id]
	response = requests.post(
		url=requestBody.getUrl("MES_DELETE_PERFORMANCE_REPORT"),
		headers=json_headers,
		json=body,
		verify=False
	)
	assert response.status_code == 200
	assert response.json()['success'] is True


if __name__ == '__main__':
	pytest.main("-s,-v,test_performanceReport.py")

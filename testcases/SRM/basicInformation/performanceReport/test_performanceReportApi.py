#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import requests
from utils.requestBody import requestBody
import pytest


requestBody = requestBody()


# 列表查询api测试
@pytest.mark.parametrize('pageNum,pageSize,supplierCode,supplierName,examDate,isSuccess,sCode,sName, sexamDate', [
	pytest.param(1, 20, "", "", "", True, None, None, None),
	pytest.param(1, 20, "1", "", "", True, '1', None, None),
	pytest.param(1, 20, "", "公司", "", True, None, "公司", None),
	pytest.param(1, 20, "", "", "2021-04-24T03:13:41.453Z", True, None, None, "2021/04")
], ids=[
	"列表默认查询",
	"根据供应商编码模糊查询",
	"根据供应商名称模糊查询",
	"根据考核期查询"])
def test_select(json_headers, pageNum, pageSize, supplierCode, supplierName, examDate, isSuccess, sCode, sName, sexamDate):
	' '' 单接口测试-查询 ' ''
	data = {"pageNum": pageNum, "pageSize": pageSize, "supplierCode": supplierCode,"supplierName": supplierName,"examDate":examDate}
	response = requests.post(
		url=requestBody.getUrl("MES_SELECT_PERFORMANCE_REPORT"),
		headers=json_headers,
		json=data
	)
	assert response.json()['success'] == isSuccess, "接口查询失败"
	if response.json()['data']['list']:
		if sCode:
			for i in range(0, len(response.json()['data']['list'])):
				assert sCode in response.json()['data']['list'][i]['supplierCode'], "根据供应商编码查询有误"
		if sName:
			for i in range(0, len(response.json()['data']['list'])):
				assert sName in response.json()['data']['list'][i]['supplierName'], "根据供应商名称查询有误"
		if sexamDate:
			for i in range(0, len(response.json()['data']['list'])):
				assert sexamDate in response.json()['data']['list'][i]['examDate'], "根据考核期查询有误"


if __name__ == '__main__':
	pytest.main("-s,-v,test_performanceReportApi.py")

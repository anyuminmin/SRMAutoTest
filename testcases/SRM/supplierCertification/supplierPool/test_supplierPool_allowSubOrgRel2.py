#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import requests
from utils.requestBody import requestBody
import pytest
import random

requestBody = requestBody()
# 从config_demopre配置获取参数shopid、name
_shopId = str(requestBody.getLoginShopId())
_shopId2 = str(requestBody.getLoginShopId2())
_companyName = str(requestBody.getCompanyName())
_companyName2 = str(requestBody.getCompanyName2())


# 从parmas配置中获取参数，并替换其参数shopid、name
def replaceParams(key):
	_data = requestBody.getParamsBody(key)
	_data['maintainShopList'][0]['shopId'] = _shopId
	_data['maintainShopList'][0]['name'] =_companyName
	_data['relOrganizationList'][0]['shopId'] = _shopId
	_data['relOrganizationList'][0]['name'] = _companyName
	_data['relOrganizationList'][1]['shopId'] = _shopId2
	_data['relOrganizationList'][1]['name'] = _companyName2
	return _data


# 新增供应商库,允许下级引用：2指定公司，且维护或引用部分公司
def test_save_supplier_pool(json_headers):
	_data = replaceParams("MES_SAVE_SUPPLIER_POOL")
	response = requests.post(
		url=requestBody.getUrl("MES_SAVE_SUPPLIER_POOL"),
		headers=json_headers,
		json=_data
		# json=requestBody.getParamsBody("MES_SAVE_SUPPLIER_POOL")
	)
	print(response.json())
	assert response.json()['success']is True, response.json()['message']


_paramsdata = replaceParams("MES_SAVE_SUPPLIER_POOL")
_num = random.randint(1, 10)


# 重复新增报错
@pytest.mark.parametrize('supplier_pool_code,supplier_pool_name,message', [
	pytest.param(_paramsdata['supplierPoolCode'], "供应商库随意"+str(_num), "已存在相同的供应商库编码"),
	pytest.param("scode"+str(_num), _paramsdata['supplierPoolName'], "已存在相同的供应商库名称")
], ids=[
	"供应商库编码，唯一性校验",
	"供应商库名称，唯一性校验"
])
def test_save_fail_supplier_pool(json_headers, supplier_pool_code, supplier_pool_name, message):
	_paramsdata['supplierPoolCode'] = supplier_pool_code
	_paramsdata['supplierPoolName'] = supplier_pool_name
	response=requests.post(
		url=requestBody.getUrl("MES_SAVE_SUPPLIER_POOL"),
		headers=json_headers,
		json=_paramsdata
	)
	assert response.json()['success']is False
	assert message in str(response.json())

# 查询供应商库(新增后校验列表；且获取id)
@pytest.fixture(scope='module')
def test_select_for_save(json_headers):
	response=requests.post(
		url=requestBody.getUrl("MES_SELECT_SUPPLIER_POOL"),
		headers=json_headers,
		json=requestBody.getParamsBody("MES_SELECT_SUPPLIER_POOL")
	)
	assert response.json()['success']is True, response.json()['message']
	assert response.json()['data']['list'][0]['allowSubOrgRel'] == 2, "列表允许公司下级引用方式与请求不一致"
	assert response.json()['data']['list'][0]['maintainShopList'][0]['name'] == _companyName, "列表维护公司与请求不一致"
	assert response.json()['data']['list'][0]['relOrganizationList'][0]['name'] == _companyName, "列表引用公司与请求不一致"
	assert response.json()['data']['list'][0]['relOrganizationList'][1]['name'] == _companyName2, "列表引用公司与请求不一致"
	return response.json()


# 修改供应商库，修改为允许下级引用：所有
def test_update_supplier_pool(json_headers, test_select_for_save):
	_data = requestBody.getParamsBody("MES_UPDATE_SUPPLIER_POOL")
	_data['relOrganizationList'] = []
	_id = test_select_for_save['data']['list'][0]['id']
	_data['id'] = _id
	response = requests.post(
		url=requestBody.getUrl("MES_UPDATE_SUPPLIER_POOL"),
		headers=json_headers,
		json=_data
	)
	assert response.json()['success'] is True, response.json()['message']
	assert response.status_code == 200


# 校验更新后，列表数据
def test_select_for_update(json_headers):
	response = requests.post(
		url=requestBody.getUrl("MES_SELECT_SUPPLIER_POOL"),
		headers=json_headers,
		json=requestBody.getParamsBody("MES_SELECT_SUPPLIER_POOL")
	)
	assert response.json()['success']is True, response.json()['message']
	assert response.json()['data']['list'][0]['allowSubOrgRel'] == requestBody.getParamsBody("MES_UPDATE_SUPPLIER_POOL")['allowSubOrgRel'], "列表允许公司下级引用方式与请求不一致"
	assert response.json()['data']['list'][0]['maintainShopList'][0]['name'] == _companyName , "列表维护公司与请求不一致"
	assert response.json()['data']['list'][0]['relOrganizationList'] == [], "列表引用公司与请求不一致"
	return response.json()


# 删除数据
def test_delete_supplier_pool(json_headers, test_select_for_save):
	_data = requestBody.getParamsBody("MES_DELETE_SUPPLIER_POOL")
	_data['list'] = [test_select_for_save['data']['list'][0]['id']]
	response = requests.post(
		url=requestBody.getUrl("MES_DELETE_SUPPLIER_POOL"),
		headers=json_headers,
		json=_data
	)
	assert response.json()['success']is True, response.json()['message']


if __name__ == '__main__':
	pytest.main("-s,-v,test_supplierPool_allowSubOrgRel2.py")

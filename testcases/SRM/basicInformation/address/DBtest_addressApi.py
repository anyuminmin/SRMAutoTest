#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.operationMysql import mysqlUtils
from utils.requestBody import requestBody
import requests
import random
import pytest

requestBody = requestBody()
shopId = requestBody.getLoginShopId()
sql = mysqlUtils()

def test_getAddressForDB(num=20):
	'''默认查询20条数据'''
	mysql = "select * from scm_address where del_flag=%s and shop_id=%s order by address_code limit %s"
	params = (0, shopId,num)
	data = sql.readSql(mysql, params, DB='scm_master')
	codeList = [] #地址编码
	typeList = [] #地址类型
	nameList = [] #地址名称
	remarkList = [] #备注
	[codeList.append(data[i][1]) for i in  range(0, len(data))] #获取列表all编码
	[typeList.append(data[i][2]) for i in  range(0, len(data))] #获取列表all类型
	[nameList.append(data[i][3]) for i in  range(0, len(data))] #获取列表all名称
	[remarkList.append(data[i][4]) for i in  range(0, len(data))] #获取列表all备注
	return codeList,typeList,nameList,remarkList


# 新增test
@pytest.mark.parametrize('addressCode,addressType,addressName,remark,isSuccess,message',[
	pytest.param("",1,"浙江省杭州市余杭区佳源未来府","家",False,"地址编码必填"),
	pytest.param("code",None,"浙江省杭州市余杭区佳源未来府","家",False,"地址类型必填"),
	pytest.param("code",1,"","家",False,"地址名称不能为空"),
	pytest.param(test_getAddressForDB()[0][0],1,"浙江省杭州市余杭区佳源未来府","家",False,"地址编码"+ test_getAddressForDB()[0][0]+"已存在")
],
ids=[
	"地址编码必填校验",
	"地址类型必填校验",
	"地址名称必填校验",
	"地址编码已存在校验（该地址编码从db获取）"
])
def test_saveAddress(json_headers,addressCode,addressType,addressName,remark,isSuccess,message):
	data={"addressCode":addressCode,"addressType":addressType,"addressName":addressName,"remark":remark}

	response=requests.post(
		url=requestBody.getUrl("MES_SAVE_ADDRESS"),
		headers=json_headers,
		json=data
	)
	assert response.json()['messages'][0]['message'] == message
	assert response.json()['success'] == isSuccess


# # 列表查询
@pytest.mark.parametrize('pageNum,pageSize,fuzzyAddressCode,fuzzyAddressName,count,addressCode,addressName',[
	# pytest.param(1,20,None,None,20,codeList,None),#查询20条数据，并按照code升序排序
	pytest.param(1,20,test_getAddressForDB()[0][0],None,1,None,None),
	# pytest.param(1,20,None,None,1,None,test_getAddressForDB()[2][0])
],
ids=[
	# "默认列表查询"
	# "根据地址编码查询"
	"根据地址名称查询"
])
def test_selectAddress(json_headers,pageNum,pageSize,fuzzyAddressCode,fuzzyAddressName,count,addressCode,addressName):
	#全量数据校验，无查询条件
	data={"pageNum":pageNum,"pageSize":pageSize,"fuzzyAddressCode":fuzzyAddressCode,"fuzzyAddressName":fuzzyAddressName}
	response=requests.post(
		url=requestBody.getUrl("MES_SELECT_ADDRESS"),
		headers=json_headers,
		json=data
	)
	list=[]
	for i in range(0,len(response.json()['data']['list'])):
		list.append(response.json()['data']['list'][i]['addressCode'])
	if addressCode:
		assert list==addressCode,"列表返回地址编码与db不一致"
	assert len(response.json()['data']['list'])==count,"列表数量返回值与db不一致"
	if addressName!=None:
		assert response.json()['data']['list'][0]['addressName']==addressName,"列表返回名称与db不一致"

	# def test_1updateAddress(self,jsonHeaders,test_selectAddress):
	# 	更新addressName、remark，然后再跟查询出来之前的值比较
	# 	body=self.requestBody.getParamsBody("MES_UPDATE_ADDRESS")
	# 	body['addressName']=body['addressName']+str(random.randint(1,10))
	# 	body['remark']=body['remark']+str(random.randint(1,10))
	# 	body['id']=[test_selectAddress[0]['id']]
	# 	requests.post(
	# 		url=self.requestBody.getUrl("MES_UPDATE_ADDRESS"),
	# 		headers=jsonHeaders,
	# 		json=body
	# 	)
	# 	assert test_selectAddress[0]['addressName']!=body['addressName'] #此时查询出来的值，还是更新之前的
	# 	assert test_selectAddress[0]['remark']!=body['remark']

	# def test_2deleteAddress(self,jsonHeaders,test_selectAddress):
	# 	body=self.requestBody.getParamsBody("MES_DELETE_ADDRESS")
	# 	body['list']=[test_selectAddress[0]['id']]
	# 	response=requests.post(
	# 		url=self.requestBody.getUrl("MES_DELETE_ADDRESS"),
	# 		headers=jsonHeaders,
	# 		json=body
	# 	)
	# 	assert response.json()['status'] == 0
	# 	assert response.json()['success'] == True

	# def test_3dbDEL(self,test_selectAddress):
	# 	#数据清洗
	# 	assert test_selectAddress != [],"获取列表为空"
	# 	mysql = "delete from scm_address where id=%s"
	# 	params=(test_selectAddress[0]['id'],)
	# 	self.sql.writSql(mysql,params,DB='scm_master')#执行sql
#
# if __name__ == '__main__':
# # 	# print(test_getDBCount())
# # 	print(type(test_getDBCount()))
#     pytest.main("-s,-v,test_address.py")






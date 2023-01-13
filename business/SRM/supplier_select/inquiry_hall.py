#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from business.SRM.public.public import publicBusiness
from business.SRM.supplier_select import sourcing_template
from business.SRM.basic_data import currency
from business.SRM.basic_data import paymentType
from business.SRM.basic_data import paymentTerm
from utils.read_config import ReadConfig
from services.httpService import HttpService
import random
from utils.logger import Logger
from utils import time_helper

publicBusiness = publicBusiness()
read_config = ReadConfig()
shopId = read_config.shopId
http = HttpService()
log = Logger("InquiryHallBusiness").logger


def get_generate_code_for_inquiry_hall():
	"""获取寻源大厅编码"""
	paramDict = {"ruleCode": "INQUIRY_HALL_CODE_RULE"}
	rsp = publicBusiness.get_generate_code(paramDict)
	log.info("寻源大厅编码:" + rsp)
	return rsp


def get_sourcing_template():
	"""获取寻源模板"""
	paramDict = {"queryShopId": shopId}
	rsp = sourcing_template.get_sourcing_template(paramDict)
	log.info("寻源模板:" + str(rsp['data']['list'][0]))
	return rsp['data']['list'][0]


def get_currency():
	"""获取币种"""
	paramDict = {"fuzzyName": ""}
	rsp = currency.get_currency(paramDict)
	log.info("币种:" + str(rsp))
	return rsp['data']['list'][0]


def get_paymentType():
	"""获取结算方式"""
	paramDict = {"fuzzyName": ""}
	rsp = paymentType.get_paymentType(paramDict)
	log.info("结算方式:" + str(rsp['data']['list'][0]))
	return rsp['data']['list'][0]


def get_paymentTerm():
	"""获取付款条件"""
	paramDict = {"fuzzyName": ""}
	rsp = paymentTerm.get_paymentTerm(paramDict)
	log.info("付款条件:" + str(rsp['data']['list'][0]))
	return rsp['data']['list'][0]


def query_dept_and_person():
	"""获取部门id：personId编码"""
	return publicBusiness.query_dept_and_person()['list'][0]


class InquiryHallBusiness:

	def create_new_inquiry_hall(self, paramDict):
		"""新增寻源单"""
		paramList = ['寻源大厅']
		publicBusiness.shop_com_sysFactory_updateSys_to_close(paramList)
		publicBusiness.shop_com_sysRole_update(paramList)
		url = read_config.get_url("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_SAVE")
		param = read_config.get_param("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_SAVE")
		param['billNo'] = get_generate_code_for_inquiry_hall()
		param['inquiryTopic'] = "autoTest" + str(random.randint(1000, 9999))
		param['gmtCreate'] = time_helper.getTimesTZ()
		param['applyDeptId'] = query_dept_and_person()['deptId']
		param['applyPersonId'] = query_dept_and_person()['parentId']
		param['companyId'] = shopId
		param['currencyId'] = get_currency()['id']
		param['paymentTermId'] = get_paymentTerm()['id']
		param['paymentTypeId'] = get_paymentType()['id']
		param['templateId'] = get_sourcing_template()['id']
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp

	def update_inquiry_hall(self):
		"""修改寻源单，明细等"""
		url = read_config.get_url("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_UPDATE")
		param = read_config.get_param("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_UPDATE")
		insertParam = self.create_new_inquiry_hall({}).json()['data']
		param['billNo'] = insertParam['billNo']
		param['inquiryTopic'] = insertParam['inquiryTopic']
		param['gmtCreate'] = insertParam['gmtCreate']
		param['applyDeptId'] = insertParam['applyDeptId']
		param['applyPersonId'] = insertParam['applyPersonId']
		param['companyId'] = shopId
		param['currencyId'] = insertParam['currencyId']
		param['paymentTermId'] = insertParam['paymentTermId']
		param['paymentTypeId'] = insertParam['paymentTypeId']
		param['templateId'] = insertParam['templateId']
		param['budgetAmount'] = 5000
		param['businessId'] = publicBusiness.shop_query_person_list()['groupConfig'][0]['dept']['businessId']
		param['id'] = insertParam['id']
		param['inquiryHallDetails']['materialId'] = insertParam['id']
		return param



	def delete_inquiry_hall(self, paramDict):
		"""删除寻源单"""
		url = read_config.get_url("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_DELETE")
		param = read_config.get_param("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_DELETE")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp


if __name__ == '__main__':
	inquiryHallBusiness = InquiryHallBusiness()
	# print(inquiryHallBusiness.update_inquiry_hall())
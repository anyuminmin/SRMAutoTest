#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import pytest

from services.SRM.supplier_select.inquiryHallService import InquiryHallService
from utils import time_helper
from utils.logger import Logger
from services.common.assertService import AssertService
from services.SRM.supplier_select.sourcingTemplateService import sourcingTemplateService
from services.SRM.basic_data.generateCodeService import GenerateCodeService
from services.SRM.basic_data.currencyService import currencyService
from services.SRM.basic_data.paymentTermService import paymentTermService
from services.SRM.basic_data.paymentTypeService import paymentTypeService
from services.SRM.basic_data.deptAndPersonService import DeptAndPersonService
from services.SRM.basic_data.supplierService import SupplierService
from services.SRM.basic_data.materialService import MaterialService
from services.SRM.basic_data.taxesService import TaxesService
from utils.read_config import ReadConfig
import random
import json

read_config = ReadConfig()
shopId = read_config.shopId
inquiryHallBusiness = InquiryHallService()
log = Logger("TestInquiryHallCases").logger
assertService = AssertService()
generateCodeService = GenerateCodeService()
sourcingTemplateService = sourcingTemplateService()
currencyService = currencyService()
paymentTypeService = paymentTypeService()
paymentTermService = paymentTermService()
deptAndPersonService = DeptAndPersonService()
supplierService = SupplierService()
materialService = MaterialService()
taxesService = TaxesService()
generate_code = generateCodeService.get_generate_code({"ruleCode": "INQUIRY_HALL_CODE_RULE"})  # 获取寻源大厅编码
template = sourcingTemplateService.get_sourcing_template({"queryShopId": shopId})['data']['list'][0]  # 获取寻源模板
currency = currencyService.get_currency({"fuzzyName": ""})['data']['list'][0]  # 获取币种
paymentType = paymentTypeService.get_paymentType({"fuzzyName": ""})['data']['list'][0]  # 获取结算方式
paymentTerm = paymentTermService.get_paymentTerm({"fuzzyName": ""})['data']['list'][0]  # 获取付款条件
person = deptAndPersonService.query_dept_and_person()['list'][0]  # 获取部门id：personId编码
taxes = taxesService.get_taxes() # 获取税码信息


class TestInquiryHallCases:

	@pytest.mark.P1
	@pytest.mark.parametrize(
		'isSuccess, message, billNo, inquiryTopic, applyDeptId, applyPersonId, companyId, currencyId, paymentTermId, paymentTypeId, templateId',
		[
			pytest.param(False, "寻源标题不能为空", generate_code, "", person['deptId'], person['parentId'], shopId,
			             currency['id'], paymentTerm['id'], paymentType['id'], template['id']),
			pytest.param(False, "币种不能为空", generate_code, "autoTest" + str(random.randint(1000, 9999)), person['deptId'],
			             person['parentId'], shopId, "", paymentTerm['id'], paymentType['id'], template['id']),
			pytest.param(True, "", generate_code, "autoTest" + str(random.randint(1000, 9999)), person['deptId'],
			             person['parentId'], shopId, currency['id'], paymentTerm['id'], paymentType['id'],
			             template['id'])
		],
		ids=['新增失败，寻源标题为空', '新增失败，币种为空', '新增成功']
	)
	def test_create_new_inquiry_hall(self, isSuccess, message, billNo, inquiryTopic, applyDeptId, applyPersonId,
	                                 companyId, currencyId, paymentTermId, paymentTypeId, templateId):
		resBody = {"billNo": billNo, "applyPersonId": applyPersonId, "companyId": companyId, "currencyId": currencyId,
		           "paymentTypeId": paymentTypeId,
		           "paymentTermId": paymentTermId, "applyDeptId": applyDeptId, "inquiryTopic": inquiryTopic,
		           "templateId": templateId}
		rsp = inquiryHallBusiness.create_new_inquiry_hall(resBody, isSuccess)
		if isSuccess:
			try:
				assertService.base_assert_for_success(rsp)
			finally:
				id_ = rsp.json()['data']['id']
				deleteParamDict = {"list": [id_]}
				rsp = inquiryHallBusiness.delete_inquiry_hall(deleteParamDict)
				assertService.base_assert_for_success(rsp)
		else:
			assertService.assert_message_fail(rsp, message)

	@pytest.mark.P1
	@pytest.mark.SRM
	@pytest.mark.parametrize(
		'isSuccess, message, supplier, taxId, taxRate, qty',
		[
			pytest.param(False, '寻源明细行未分配供应商', 0, taxes['id'], taxes['taxRate'], 2),
			pytest.param(False, '寻源单明细行中的数量不能为空', 1, taxes['id'], taxes['taxRate'], None),
			pytest.param(False, '寻源单明细行中的税码/税率不能为空', 1, None, None, 2),
		],
		ids=['新增失败,明细行未分配供应商', '新增失败，明细行数量为空', '新增失败，税码/税率为空']
	)
	def test_update_inquiry_hall(self, isSuccess, message, supplier, taxId, taxRate, qty):
		inquiryTopic = "autoTest" + str(random.randint(1000, 9999))
		generate_code_new = generateCodeService.get_generate_code({"ruleCode": "INQUIRY_HALL_CODE_RULE"})
		insertResBody = {"billNo": generate_code_new, "applyPersonId": person['parentId'], "companyId": shopId,
		                 "currencyId": currency['id'], "paymentTypeId": paymentType['id'],
		                 "paymentTermId": paymentTerm['id'], "applyDeptId": person['deptId'],
		                 "inquiryTopic": inquiryTopic, "templateId": template['id']}
		inquiryHallDetails = {"inquirySupplierAllocates": [], "rowNo": 1, "materialId": "", "materialTypeId": "",
		                      "qty": qty, "unitId": "", "taxId": taxId, "taxRate": taxRate, "remark": "", "materialCode": "",
		                      "materialTypeCode": "", "taxInclude": 1, "freightInclude": 2}
		resBody = {"applyDeptId": person['deptId'], "applyPersonId": person['parentId'], "billNo": generate_code,
		           "companyId": shopId, "creatorId": person['parentId'], "currencyId": currency['id'],
		           "gmtModified": time_helper.getTimesTZ(), "id": "", "inquiryHallDetails": [], "inquirySuppliers": [],
		           "inquiryTopic": inquiryTopic, "paymentTermId": paymentTerm['id'], "paymentTypeId": paymentType['id'],
		           "personId": person['parentId'], "shopId": shopId, "templateId": template['id'] }
		insertRsp = inquiryHallBusiness.create_new_inquiry_hall(insertResBody)
		if insertRsp.json()['success']:
			id_ = insertRsp.json()['data']['id']
			Suppliers = {"id": 3098584, "state": False, "supplierId": "", "supplierCode": "", "supplierName": "",
			             "telephone": "", "mail": "", "linkman": ""}
			supplierList = supplierService.get_supplier_list()[0]
			materialList = materialService.get_material_massages()[0]
			Suppliers["id"] = random.randint(1000000, 9999999)
			Suppliers["supplierId"] = supplierList['id']
			Suppliers["supplierCode"] = supplierList['supplierCode']
			Suppliers["telephone"] = supplierList['telephone']
			Suppliers["mail"] = supplierList['mail']
			Suppliers["linkman"] = supplierList['linkman']
			if supplier == 0:
				inquiryHallDetails['inquirySupplierAllocates'] = []
			else:
				inquiryHallDetails["inquirySupplierAllocates"].append(Suppliers)
			inquiryHallDetails['materialId'] = materialList['id']
			inquiryHallDetails['materialTypeId'] = materialList['materialTypeId']
			inquiryHallDetails['materialCode'] = materialList['materialCode']
			inquiryHallDetails['materialTypeCode'] = materialList['materialTypeCode']
			inquiryHallDetails['unitId'] = materialList['unitId']
			resBody['id'] = id_
			resBody['inquiryHallDetails'].append(inquiryHallDetails)
			resBody['inquirySuppliers'].append(Suppliers)
			rsp = inquiryHallBusiness.update_inquiry_hall(resBody, isSuccess)
			try:
				if isSuccess:
					assertService.base_assert_for_success(rsp)
				else:
					assertService.assert_message_fail(rsp, message)
			finally:
				deleDict = {"list": [id_]}
				rsp = inquiryHallBusiness.delete_inquiry_hall(deleDict)
				assertService.base_assert_for_success(rsp)

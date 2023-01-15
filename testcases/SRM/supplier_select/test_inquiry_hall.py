#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import pytest

from business.SRM.supplier_select.inquiry_hall import InquiryHallBusiness
from utils.logger import Logger
from services.assertService import AssertService
import json

inquiryHallBusiness = InquiryHallBusiness()
log = Logger("TestInquiryHallCases").logger
assertService = AssertService()


class TestInquiryHallCases:

	@pytest.mark.P1
	@pytest.mark.parametrize(
		'isSuccess, message, paramDict',
		[
			pytest.param(False, "寻源标题不能为空", {"inquiryTopic": ""}),
			pytest.param(False, "币种不能为空", {"currencyId": ""}),
			pytest.param(True, None, {})
		],
		ids=['新增失败，寻源标题为空', '新增失败，币种为空', '新增成功，必填字段都不为空']
	)
	def test_create_new_inquiry_hall(self, srm_buyer_login, paramDict, isSuccess, message):
		rsp = inquiryHallBusiness.create_new_inquiry_hall(paramDict)
		log.info(str(rsp.json()))
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
	@pytest.mark.parametrize(
		'isSuccess, message, paramDict',
		[
			pytest.param(False, '寻源单的供应商不能为空', {"inquiryHallDetails":[{"inquirySupplierAllocates":[{"supplierId":""}]}]}),
		],
		ids=['新增失败', ]
	)
	def test_update_inquiry_hall(self, paramDict, isSuccess, message):
		rsp = inquiryHallBusiness.update_inquiry_hall(paramDict)
		id_ = rsp[1]
		log.info(str(rsp[2]))
		try:
			if isSuccess:
				assertService.base_assert_for_success(rsp[0])
			else:
				# log.info(str(rsp))
				assertService.assert_message_fail(rsp, message)
		finally:
			deleDict = {"list": [id_]}
			rsp = inquiryHallBusiness.delete_inquiry_hall(deleDict)
			assertService.base_assert_for_success(rsp)

	def test_test(self):
		paramDict = {"inquiryHallDetails":[{"inquirySupplierAllocates":[{"supplierId":""}]}], "inquiry": "222"}
		# paramDict = {"inquiryHallDetails": "222"}
		param = {"inquiryHallDetails":[{"id":3049668,"parentId":"","inquiryLadderQuotations":None,"inquirySupplierAllocates":[{"id":3098584,"state":False,"supplierId":"852294463363514368","supplierCode":"F21523","supplierName":"autoTest__supplier626","telephone":"13136166390","mail":"23233@163.com","linkman":"abby"}],"rowNo":1,"materialId":"819364747807850496","materialSpec":"壁厚公差:11","bindedCharacter":"","materialTypeId":"819161160787984384","qty":11,"deferCount":"",}]}
		# for i in paramDict:
		# 	if "inquiryHallDetails" in paramDict:
		# 		paramNewKeys = paramDict.get(i)
		# 		print(paramNewKeys)
		# 	else:
		# 		param = paramDict.get(i)
		# 		print("2222222223" + param)
		for k in paramDict.keys():
			if "inquiryHallDetails" == k:
				paramNewKeys = paramDict.values()
				print(paramNewKeys)
				paramDict = str(paramNewKeys).split(":")
				print(paramDict)

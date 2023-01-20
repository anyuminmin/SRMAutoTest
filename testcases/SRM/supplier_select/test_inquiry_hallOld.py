#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import pytest

from services.SRM.supplier_select.inquiryHallServiceOld import InquiryHallService
from utils.logger import Logger
from services.common.assertService import AssertService

inquiryHallBusiness = InquiryHallService()
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


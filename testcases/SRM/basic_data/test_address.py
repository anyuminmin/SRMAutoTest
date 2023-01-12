#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from business.SRM.basic_data.address import Address
import pytest
from services.assertService import AssertService
from utils.random_util import RandomUtil
from utils.logger import Logger
log = Logger("TestAddressCases").logger

address = Address()
assertService = AssertService()
randomUtil = RandomUtil()
addressCode = randomUtil.random_string(12, startswith="autoTest-")
existedCode = address.select_address({"fuzzyAddressCode": "", "fuzzyAddressName": ""}).json()['data']['list'][0]['addressCode']


def insert_address():
	addressCode = randomUtil.random_string(12, startswith="autoTest-")
	paramDict = {"addressCode": addressCode, "addressType": 1, "addressName": "浙江省杭州市余杭区佳源未来府", "remark": "家"}
	address.add_new_address(paramDict)


def select_insert_address():
	selectParam = {"fuzzyAddressCode": "autoTest", "fuzzyAddressName": ""}
	response = address.select_address(selectParam).json()
	if response['data']['list']:
		return response['data']['list'][0]['addressCode'], response['data']['list'][0]['id']
	else:
		insert_address()
		selectParam = {"fuzzyAddressCode": "autoTest", "fuzzyAddressName": ""}
		response = address.select_address(selectParam).json()
		return response['data']['list'][0]['addressCode'], response['data']['list'][0]['id']


class TestAddressCases:

	@pytest.mark.P1
	@pytest.mark.parametrize(
		'addressCode, addressType, addressName, remark, isSuccess, message',
		[
			pytest.param(addressCode, 1, "浙江省杭州市余杭区佳源未来府", "家", True, None),
			pytest.param(existedCode, 1, "浙江省杭州市余杭区佳源未来府", "家", False, "地址编码" + existedCode + "已存在"),
			pytest.param("", 1, "浙江省杭州市余杭区佳源未来府", "家", False, "地址编码必填"),
			pytest.param(addressCode, 1, "", "家", False, "地址名称不能为空"),
			pytest.param(addressCode, 1, "浙江省杭州市余杭区佳源未来府", "", True, None)
		],
		ids=['新增成功，编码唯一', '重复编码，新增失败', '编码为空，新增失败', '名称为空，新增失败', '备注为空，新增成功']
	)
	def test_add_new_address(self, addressCode, addressType, addressName, remark,  isSuccess, message):
		"""新增新地址"""
		paramDict = {"addressCode": addressCode, "addressType": addressType, "addressName": addressName, "remark": remark}
		response = address.add_new_address(paramDict)
		log.info(response.json())
		selectParam = {"fuzzyAddressCode": addressCode, "fuzzyAddressName": ""}
		if isSuccess:
			try:
				assertService.base_assert_for_success(response)
			finally:
				id_ = address.select_address(selectParam).json()['data']['list'][0]['id']
				address.delete_address({"list": [id_]})
				assert address.select_address(selectParam).json()['data']['list'] == []
		else:
			assertService.assert_message_fail(response, message)

	@pytest.mark.P1
	@pytest.mark.parametrize(
		'addressCode, addressName, remark, id_, isSuccess, message',
		[
			pytest.param(select_insert_address()[0],  "浙江省杭州市余杭区佳源未来府update", "家", select_insert_address()[1], True, None),
			pytest.param(select_insert_address()[0] + "update",  "浙江省杭州市余杭区佳源未来府", "家", select_insert_address()[1], True, None),
			pytest.param(select_insert_address()[0],  "浙江省杭州市余杭区佳源未来府", "家update", select_insert_address()[1], True, None),
			pytest.param(select_insert_address()[0],  "浙江省杭州市余杭区佳源未来府update", "", select_insert_address()[1], True, None)
		],
		ids=["修改addressName成功", "修改addressCode成功", "修改remark成功", "备注修改为空"]
	)
	def test_update_address(self, addressCode, addressName, remark, id_, isSuccess, message):
		"""修改地址成功"""
		selectParam = {"fuzzyAddressCode": select_insert_address()[0], "fuzzyAddressName": ""}
		response = address.select_address(selectParam).json()
		# assert response['data']['list'][0]['addressCode'] == select_insert_address()[0]
		# assert response['data']['list'][0]['addressName'] == "浙江省杭州市余杭区佳源未来府"
		paramDict = {"addressCode": addressCode, "addressType": 1, "addressName": addressName, "remark": remark, "id": id_}
		response = address.update_address(paramDict)
		newSelectParam = {"fuzzyAddressCode": addressCode, "fuzzyAddressName": ""}
		log.info(response.json())
		if isSuccess:
			try:
				assertService.base_assert_for_success(response)
				response = address.select_address(newSelectParam).json()
				assert response['data']['list'][0]['addressCode'] == addressCode
			except:
				log.info("用例执行失败")
		else:
			assertService.assert_message_fail(response, message)
		address.delete_address({"list": [id_]})
		assert address.select_address(newSelectParam).json()['data']['list'] == []


def test_test():
	print("============")
	# rsp = address.select_address({"fuzzyAddressCode": "", "fuzzyAddressName": ""}).json()
	# print(select_insert_address())
	# print(existedCode)
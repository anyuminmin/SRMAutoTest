#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from services.common.BaseService import BaseService
from utils.read_config import ReadConfig
from utils.logger import Logger
log = Logger("SupplierService").logger


class SupplierService(BaseService):

	def get_supplier_list(self, paramDict={"fuzzyName": "auto"}, isSuccess = True):
		"""获取供应商，先根据期望供应商搜素，没有则获取默认列表"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "GET_SUPPLIER_LIST")
		param = ReadConfig().get_param("SRM/public/base.yaml", "GET_SUPPLIER_LIST")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			if len(rsp.json()['data']['list']) > 0:
				log.info("============供应商信息：" + str(rsp.json()['data']['list'][0]) + "============")
				return rsp.json()['data']['list']
			else:
				log.info("==========无此类型的供应商，请检查==========")
		else:
			return self.return_and_assert(rsp, "获取供应商", isSuccess)
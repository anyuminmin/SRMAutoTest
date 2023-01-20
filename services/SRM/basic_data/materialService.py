#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from services.common.BaseService import BaseService
from utils.read_config import ReadConfig
from utils.logger import Logger
log = Logger("SysRoleService").logger


class MaterialService(BaseService):

	def get_material_massages(self, paramDict={"fuzzyName": "10.101.000"}, isSuccess = True):
		"""获取物料信息"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "GET_MATERIAL_MESSAGES")
		param = ReadConfig().get_param("SRM/public/base.yaml", "GET_MATERIAL_MESSAGES")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			if len(rsp.json()['data']['list']) > 0:
				log.info("============物料信息：" + str(rsp.json()['data']['list'][0]) + "============")
				return rsp.json()['data']['list']
			else:
				log.info("======无此物料信息，请检查，或请求失败，请看异常" + str(rsp.json()) + "======")
		else:
			return self.return_and_assert(rsp, "获取物料信息", isSuccess)
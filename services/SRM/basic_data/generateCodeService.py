#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from services.common.BaseService import BaseService
from utils.read_config import ReadConfig


class GenerateCodeService(BaseService):

	def get_generate_code(self, paramDict, isSuccess = True):
		"""获取操作编码"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "GET_GENERATE_CODE")
		param = ReadConfig().get_param("SRM/public/base.yaml", "GET_GENERATE_CODE")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			return rsp.json()['data']
		else:
			return self.return_and_assert(rsp, "获取操作编码", isSuccess)


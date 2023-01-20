#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from services.common.BaseService import BaseService
from utils.read_config import ReadConfig
from utils.logger import Logger
log = Logger("TaxesService").logger


class TaxesService(BaseService):

	def get_taxes(self, isSuccess = True):
		"""获取税码信息，先查询是否有0.13的税码，没有则获取列表第一条数据"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "GET_TAXES")
		param = ReadConfig().get_param("SRM/public/base.yaml", "GET_TAXES")
		isHave = 0
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			for i in range(len(rsp.json()['data']['list'])):
				if rsp.json()['data']['list'][i]['taxRate'] == 0.13:
					self.isHave = 1
					log.info("税码信息：" + str(rsp.json()['data']['list'][i]))
					return rsp.json()['data']['list'][i]
					break
			if isHave == 0:
				log.info("============税码信息：" + str(rsp.json()['data']['list'][0]) + "============")
				return rsp.json()['data']['list'][0]
		else:
			return self.return_and_assert(rsp, "获取税码信息", isSuccess)
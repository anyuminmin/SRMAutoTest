#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.read_config import ReadConfig
from services.httpService import HttpService
from utils.logger import Logger
from business.SRM.public.public import publicBusiness

read_config = ReadConfig()
http = HttpService()
log = Logger("publicBusiness").logger
publicBusiness = publicBusiness()


class FactoryRuleBusiness:

	def __init__(self):
		self.change_factory_rule_sys()

	def change_factory_rule_sys(self):
		publicBusiness.shop_com_sysFactory_updateSys_to_open(['公司业务规则'])
		publicBusiness.shop_com_sysFactory_updateSys_to_close(['公司业务规则变更单'])
		publicBusiness.shop_com_sysRole_update(['公司业务规则'])

	def query_factory_rule(self):
		"""查询公司业务规则"""
		url = read_config.get_url("SRM/public/base.yaml", "QUERY_FACTORY_RULE")
		param = read_config.get_param("SRM/public/base.yaml", "QUERY_FACTORY_RULE")
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()['data']

	def update_factory_rule(self, paramDict):
		"""更新公司业务规则"""
		url = read_config.get_url("SRM/public/base.yaml", "UPDATE_FACTORY_RULE")
		param = self.query_factory_rule()
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()

	def update_factory_rule_for_inquiryOrderTransferStatus(self, status=1):
		"""
		更新公司业务规则: 询价单切寻源状态,
		status=1:手工切换；status=2，自动切换
		"""
		paramDict = {"inquiryOrderTransferStatus": status, "inquiryOrderTransferStatusStr": status}
		rsp = self.update_factory_rule(paramDict)
		if rsp['status'] == 0:
			log.info("=================" + "成功修改：询价单切寻源状态" + "=================")
		else:
			log.info("=================" + "修改业务规则失败，请检查!!!" + "=================")


if __name__ == '__main__':
	fa = FactoryRuleBusiness()
	fa.update_factory_rule_for_inquiryOrderTransferStatus()
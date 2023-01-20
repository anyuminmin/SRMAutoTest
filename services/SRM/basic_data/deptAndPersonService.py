#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from services.common.BaseService import BaseService
from utils.read_config import ReadConfig
read_config = ReadConfig()


class DeptAndPersonService(BaseService):

	def query_dept_and_person(self, isSuccess = True):
		"""获取部门和人员信息"""
		url = read_config.get_url("SRM/public/base.yaml", "QUERY_DEPT_AND_PERSON")
		param = read_config.get_param("SRM/public/base.yaml", "QUERY_DEPT_AND_PERSON")
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			return rsp.json()['data']
		else:
			return self.return_and_assert(rsp, "获取部门和人员信息", isSuccess)

	def shop_query_person_list(self, isSuccess = True):
		"""通讯录管理：获取人员角色、business等信息; roleCodeRemark:角色编码;;roleRemark:角色名称"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_DEPTOATXL_QUERY_PERSONLIST")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_DEPTOATXL_QUERY_PERSONLIST")
		param['personName'] = read_config.user["loginName"]
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			return rsp.json()['data']['list'][0]
		else:
			return self.return_and_assert(rsp, "讯录管理：获取人员角色、business等信息", isSuccess)

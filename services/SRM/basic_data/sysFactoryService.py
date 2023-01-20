#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from services.common.BaseService import BaseService
from utils.read_config import ReadConfig
from utils.logger import Logger
log = Logger("SysRoleService").logger


class SysFactoryService(BaseService):

	def shop_com_sysFactory_querySys(self, isSuccess = True):
		"""系统配置：查询菜单是否开启"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_QUERYSYS")
		param = ReadConfig().get_param("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_QUERYSYS")
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			return rsp.json()['data']
		else:
			return self.return_and_assert(rsp, "系统配置：查询菜单是否开启", isSuccess)

	def shop_com_sysFactory_updateSys_to_close(self, paramList):
		"""系统配置：将审批流关闭"，，paramList = ['寻源大厅', '询价单', '采购申请单']"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		param = ReadConfig().get_param("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		list = self.shop_com_sysFactory_querySys()
		if type(list) is dict:
			for i in range(len(list)):
				for j in range(len(paramList)):
					if list[i]['serviceName'] == paramList[j]:
						if list[i]['useApproval'] == 1:
							list[i]['useApproval'] = 0
							list[i]['enableApproval'] = 0
							list[i]['enableUse'] = 1
							log.info("=================" + str(paramList[j]) + "审批流关闭成功" + "=================")
						break
			param['list'] = list
			self.post_json(
				url=url,
				data=param
			)

	def shop_com_sysFactory_updateSys_to_open(self, paramList):
		"""系统配置：将审批流打开，，paramList = ['寻源大厅', '询价单', '采购申请单']"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		param = ReadConfig().get_param("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		list = self.shop_com_sysFactory_querySys()
		if type(list) is dict:
			for i in range(len(list)):
				for j in range(len(paramList)):
					if list[i]['serviceName'] == paramList[j]:
						if list[i]['useApproval'] == 0:
							list[i]['useApproval'] = 1
							list[i]['enableApproval'] = 1
							list[i]['enableUse'] = 1
							log.info("=================" + str(paramList[j]) + "审批流打开成功" + "=================")
						break
			param['list'] = list
			self.post_json(
				url=url,
				data=param
			)
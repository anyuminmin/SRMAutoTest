#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from services.SRM.basic_data.deptAndPersonService import DeptAndPersonService
from services.common.BaseService import BaseService
from utils.read_config import ReadConfig
from utils.logger import Logger
log = Logger("SysRoleService").logger


class SysRoleService(BaseService):

	def shop_com_sysRole_queryRole(self, isSuccess = True):
		"""角色：查询角色"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_ROLE")
		param = ReadConfig().get_param("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_ROLE")
		rawBody = DeptAndPersonService().shop_query_person_list()
		if type(rawBody) is dict:
			param['roleCode'] = rawBody['roleCodeRemark']
			param['roleName'] = rawBody['roleRemark']
			rsp = self.post_json(
				url=url,
				data=param
			)
			if rsp.json()['success']:
				return param['roleCode'], param['roleName'], rsp.json()['data'][0]['id']
			else:
				return self.return_and_assert(rsp, "角色：查询角色", isSuccess)


	def shop_com_sysRole_queryMultiRoleByUse(self, isSuccess = True):
		"""角色：查询角色权限管理"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_MULTIROLE_BYUSE")
		param = ReadConfig().get_param("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_MULTIROLE_BYUSE")
		rawBody = self.shop_com_sysRole_queryRole()
		if type(rawBody) is dict:
			log.info("=================" + "成功获取角色名称：" + str(rawBody[1]) + "=================")
			param['roleCode'] = rawBody[0]
			param['roleName'] = rawBody[1]
			param['id'] = rawBody[2]
			rsp = self.post_json(
				url=url,
				data=param
			)
			if rsp.json()['success']:
				return rsp.json()['data']
			else:
				return self.return_and_assert(rsp, "角色：查询角色权限管理", isSuccess)

	def shop_com_sysRole_update(self, paramList, productType=7):
		"""角色：更新角色权限:打开所有按钮"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "SHOP_COM_SYSROLE_UPDATE")
		param = ReadConfig().get_param("SRM/public/base.yaml", "SHOP_COM_SYSROLE_UPDATE")
		rawBody = self.shop_com_sysRole_queryRole()
		if type(rawBody) is dict:
			param['roleCode'] = rawBody[0]
			param['roleName'] = rawBody[1]
			param['id'] = rawBody[2]
			param['productType'] = productType
			roleList = self.shop_com_sysRole_queryMultiRoleByUse()
			if type(roleList) is dict:
				for i in range(len(roleList)):
					for j in range(len(paramList)):
						if roleList[i]['serviceName'] == paramList[j]:
							roleList[i]['enableService'] = 1  # 启用菜单
							for k in range(len(roleList[i]['list'])):
								roleList[i]['list'][k]['allowUse'] = 1
							log.info("=================" + "成功打开，角色中菜单：" + str(paramList[j]) + "的所有按钮=================")
							break
				param['list'] = roleList
				self.post_json(
					url=url,
					data=param
				)
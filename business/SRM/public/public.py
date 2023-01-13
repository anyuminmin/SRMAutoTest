#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.read_config import ReadConfig
from services.httpService import HttpService
from utils.logger import Logger

read_config = ReadConfig()
http = HttpService()
log = Logger("publicBusiness").logger


class publicBusiness:

	def get_generate_code(self, paramDict):
		"""获取操作编码"""
		url = read_config.get_url("SRM/public/base.yaml", "GET_GENERATE_CODE")
		param = read_config.get_param("SRM/public/base.yaml", "GET_GENERATE_CODE")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()['data']

	def query_dept_and_person(self):
		url = read_config.get_url("SRM/public/base.yaml", "QUERY_DEPT_AND_PERSON")
		param = read_config.get_param("SRM/public/base.yaml", "QUERY_DEPT_AND_PERSON")
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()['data']

	def shop_query_person_list(self):
		"""通讯录管理：获取人员角色、business等信息; roleCodeRemark:角色编码;;roleRemark:角色名称"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_DEPTOATXL_QUERY_PERSONLIST")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_DEPTOATXL_QUERY_PERSONLIST")
		param['personName'] = read_config.user["loginName"]
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()['data']['list'][0]

	def shop_com_sysRole_queryRole(self):
		"""角色：查询角色"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_ROLE")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_ROLE")
		rawBody = self.shop_query_person_list()
		param['roleCode'] = rawBody['roleCodeRemark']
		param['roleName'] = rawBody['roleRemark']
		rsp = http.post_json(
			url=url,
			data=param
		)
		return param['roleCode'], param['roleName'], rsp.json()['data'][0]['id']

	def shop_com_sysRole_queryMultiRoleByUse(self):
		"""角色：查询角色权限管理"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_MULTIROLE_BYUSE")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_SYSROLE_QUERY_MULTIROLE_BYUSE")
		rawBody = self.shop_com_sysRole_queryRole()
		log.info("=================" + "成功获取角色名称：" + str(rawBody[1]) + "=================")
		param['roleCode'] = rawBody[0]
		param['roleName'] = rawBody[1]
		param['id'] = rawBody[2]
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()['data']

	def shop_com_sysFactory_querySys(self):
		"""系统配置：查询菜单是否开启"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_QUERYSYS")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_QUERYSYS")
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()['data']

	def shop_com_sysFactory_updateSys_to_close(self, paramList):
		"""系统配置：将审批流关闭"，，paramList = ['寻源大厅', '询价单', '采购申请单']"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		list = self.shop_com_sysFactory_querySys()
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
		http.post_json(
			url=url,
			data=param
		)

	def shop_com_sysFactory_updateSys_to_open(self, paramList):
		"""系统配置：将审批流打开，，paramList = ['寻源大厅', '询价单', '采购申请单']"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_SYSFACTORY_UPDATESYS")
		list = self.shop_com_sysFactory_querySys()
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
		http.post_json(
			url=url,
			data=param
		)

	def shop_com_sysRole_update(self, paramList, productType=7):
		"""角色：更新角色权限:打开所有按钮"""
		url = read_config.get_url("SRM/public/base.yaml", "SHOP_COM_SYSROLE_UPDATE")
		param = read_config.get_param("SRM/public/base.yaml", "SHOP_COM_SYSROLE_UPDATE")
		rawBody = self.shop_com_sysRole_queryRole()
		param['roleCode'] = rawBody[0]
		param['roleName'] = rawBody[1]
		param['id'] = rawBody[2]
		param['productType'] = productType
		roleList = self.shop_com_sysRole_queryMultiRoleByUse()
		for i in range(len(roleList)):
			for j in range(len(paramList)):
				if roleList[i]['serviceName'] == paramList[j]:
					roleList[i]['enableService'] = 1  # 启用菜单
					for k in range(len(roleList[i]['list'])):
						roleList[i]['list'][k]['allowUse'] = 1
					log.info("=================" + "成功打开，角色中菜单：" + str(paramList[j]) + "的所有按钮=================")
					break
		param['list'] = roleList
		http.post_json(
			url=url,
			data=param
		)

	def query_extend_page_table(self):
		"""列表查询扩展字段"""
		url = read_config.get_url("SRM/public/base.yaml", "QUERY_EXTEND_PAGE_TABLE")
		param = read_config.get_param("SRM/public/base.yaml", "QUERY_EXTEND_PAGE_TABLE")
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()['data']['list']

	def update_extend_status(self, url, param):
		"""将指定扩展字段关闭"""
		http.post_json(
			url=url,
			data=param
		)

	def update_extend_status_to_close(self, paramList):
		"""将指定扩展字段关闭,,paramList = ['purchase_request_order', 'purchase_request_order_detail']"""
		url = read_config.get_url("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		param = read_config.get_param("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		extendList = self.query_extend_page_table()
		for i in range(len(extendList)):
			for j in range(len(paramList)):
				if extendList[i]['tableName'] == paramList[j]:
					param['id'] = extendList[i]['id']
					param['status'] = 0
					self.update_extend_status(url, param)
					log.info("=================" + "成功停用扩展字段：" + str(paramList[j]) + "=================")

	def update_extend_status_to_open(self, paramList):
		"""将指定扩展字段开启,,paramList = ['purchase_request_order', 'purchase_request_order_detail']"""
		url = read_config.get_url("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		param = read_config.get_param("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		extendList = self.query_extend_page_table()
		for i in range(len(extendList)):
			for j in range(len(paramList)):
				if extendList[i]['tableName'] == paramList[j]:
					param['id'] = extendList[i]['id']
					param['status'] = 1
					self.update_extend_status(url, param)
					log.info("=================" + "成功启用扩展字段：" + str(paramList[j]) + "=================")

	def get_material_massages(self, paramList):
		"""获取物料信息"""
		url = read_config.get_url("SRM/public/base.yaml", "GET_MATERIAL_MESSAGES")
		param = read_config.get_param("SRM/public/base.yaml", "GET_MATERIAL_MESSAGES")
		rsp = http.post_json(
			url=url,
			data=param
		)
		return rsp.json()


if __name__ == '__main__':
	p = publicBusiness()
	# paramList = ['采购申请单']
	# paramList = ['purchase_request_order', 'purchase_request_order_detail']
	# p.update_extend_status_to_open(paramList)
	paramList = {"fuzzyName":"10.101.000"}
	print(p.get_material_massages(paramList))

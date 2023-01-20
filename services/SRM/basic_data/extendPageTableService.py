#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from services.common.BaseService import BaseService
from utils.read_config import ReadConfig
from utils.logger import Logger
log = Logger("SysRoleService").logger


class QueryExtendPageService(BaseService):

	def query_extend_page_table(self, isSuccess = True):
		"""列表查询扩展字段"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "QUERY_EXTEND_PAGE_TABLE")
		param = ReadConfig().get_param("SRM/public/base.yaml", "QUERY_EXTEND_PAGE_TABLE")
		rsp = self.post_json(
			url=url,
			data=param
		)
		if rsp.json()['success']:
			return rsp.json()['data']['list']
		else:
			return self.return_and_assert(rsp, "列表查询扩展字段", isSuccess)

	def update_extend_status(self, url, param):
		"""将指定扩展字段关闭"""
		self.post_json(
			url=url,
			data=param
		)

	def update_extend_status_to_close(self, paramList):
		"""将指定扩展字段关闭,,paramList = ['purchase_request_order', 'purchase_request_order_detail']"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		param = ReadConfig().get_param("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		extendList = self.query_extend_page_table()
		if extendList:
			for i in range(len(extendList)):
				for j in range(len(paramList)):
					if extendList[i]['tableName'] == paramList[j]:
						param['id'] = extendList[i]['id']
						param['status'] = 0
						self.update_extend_status(url, param)
						log.info("=================" + "成功停用扩展字段：" + str(paramList[j]) + "=================")

	def update_extend_status_to_open(self, paramList):
		"""将指定扩展字段开启,,paramList = ['purchase_request_order', 'purchase_request_order_detail']"""
		url = ReadConfig().get_url("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		param = ReadConfig().get_param("SRM/public/base.yaml", "EXTEND_UPDATE_STATUS")
		extendList = self.query_extend_page_table()
		if extendList:
			for i in range(len(extendList)):
				for j in range(len(paramList)):
					if extendList[i]['tableName'] == paramList[j]:
						param['id'] = extendList[i]['id']
						param['status'] = 1
						self.update_extend_status(url, param)
						log.info("=================" + "成功启用扩展字段：" + str(paramList[j]) + "=================")

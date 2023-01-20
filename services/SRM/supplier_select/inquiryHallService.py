#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

from services.common.BaseService import BaseService
import random
from utils.logger import Logger
from utils import time_helper
from services.SRM.basic_data.materialService import MaterialService
from services.SRM.basic_data.taxesService import TaxesService
from services.SRM.basic_data.supplierService import SupplierService
from services.SRM.basic_data.sysFactoryService import SysFactoryService
from services.SRM.basic_data.sysRoleService import SysRoleService
from utils.read_config import ReadConfig


read_config = ReadConfig()
log = Logger("InquiryHallBusiness").logger
materials = MaterialService().get_material_massages()
taxes = TaxesService().get_taxes()
supplierList = SupplierService().get_supplier_list()


class InquiryHallService(BaseService):

	def setup_class(self):
		"""前置执行，执行类之前，将寻源大厅模块审批流关闭"""
	paramList = ['寻源大厅']
	SysFactoryService().shop_com_sysFactory_updateSys_to_close(paramList)
	SysRoleService().shop_com_sysRole_update(paramList)
	log.info("================寻源大厅审批流关闭================")

	def teardown_class(self):
		"""后置执行，执行类之前，将寻源大厅模块审批流开启"""
		paramList = ['寻源大厅']
		SysFactoryService().shop_com_sysFactory_updateSys_to_open(paramList)
		SysRoleService().shop_com_sysRole_update(paramList)
		log.info("================寻源大厅审批流打开================")

	def create_new_inquiry_hall(self, resBody, isSuccess=True):
		"""新增寻源单"""
		url = read_config.get_url("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_SAVE")
		param = read_config.get_param("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_SAVE")
		param['gmtCreate'] = time_helper.getTimesTZ()
		for i in resBody:
			param[i] = resBody.get(i)
		rsp = self.post_json(
			url=url,
			data=param
		)
		return self.return_and_assert(rsp, "新增寻源单", isSuccess)

	def update_inquiry_hall(self, resBody, isSuccess=True):
		"""修改寻源单，明细等"""
		url = read_config.get_url("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_UPDATE")
		param = read_config.get_param("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_UPDATE")
		for i in resBody:
			param[i] = resBody.get(i)
		rsp = self.post_json(
			url=url,
			data=param
		)
		return self.return_and_assert(rsp, "修改寻源单，明细等", isSuccess)

	def delete_inquiry_hall(self, paramDict, isSuccess=True):
		"""删除寻源单"""
		url = read_config.get_url("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_DELETE")
		param = read_config.get_param("SRM/supplier_select/inquiry_hall.yaml", "INQUIRY_HALL_DELETE")
		for i in paramDict:
			param[i] = paramDict.get(i)
		rsp = self.post_json(
			url=url,
			data=param
		)
		return self.return_and_assert(rsp, "删除寻源单", isSuccess)


# if __name__ == '__main__':
	# inquiryHallBusiness = InquiryHallBusiness()
	# print(inquiryHallBusiness.update_inquiry_hall({}))

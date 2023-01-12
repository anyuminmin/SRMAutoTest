#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.operationMysql import mysqlUtils

sql = mysqlUtils()


# # 协议类型时，批量插入数据
# def test_insertDB():
# 	# 表：pur_contract_type_attachment 参数：parentId、自定义编码
# 	mysql = "INSERT INTO `test_srm`.`pur_contract_type_attachment` (`parent_id`, `attachment_code`, `attachment_name`, `status`, `required`, `supplier_flag`, `remark`, `tenant_id`, `business_id`, `shop_id`, `creator_id`, `last_modifier_id`, `gmt_create`, `gmt_modified`, `del_flag`, `deleted_time`)  " \
# 	        "VALUES (%s, %s, 'sd', '1', '1', '0', 'sd', '539223256875155458', '539223256875155456', '539223256875155457', '852473181966573568', '852473181966573568', '2021-06-11 10:38:20', '2021-06-11 11:11:36', '0', '0')"
# 	for i in range(3, 48):
# 		params = [(15, i)]
# 		sql.writSql(mysql, params)


# 采购订单明细时，批量插入数据
def test_insertDB():
	# 表：pur_contract_type_attachment 参数：parentId、自定义编码
	mysql = "INSERT INTO `scm_master`.`pur_order_detail` (`id`,`parent_id`, `parent_path`, `row_no`, `material_id`, `material_spec`, `binded_character`, `attribute_item_id`, `qty`, `plan_receive_date`, `enable_quality`, `source_row_id`, `source_id`, `pp_order_row_id`, `pp_order_id`, `tax_price`, `tax_amount`, `tax_rate`, `notax_price`, `notax_amount`, `tax`, `receive_qty`, `inspect_qualify_qty`, `inspect_defect_qty`, `stock_qty`, `invoice_qty`, `return_qty`, `cancelled_qty`, `exceed_max_qty`, `unit_id_bus`, `bus_qty`, `remark`, `gmt_create`, `gmt_modified`, `del_flag`, `tenant_id`, `business_id`, `shop_id`, `current_state`, `last_close_id`, `gmt_close`, `close_type`, `source_price_library_detail_id`, `price_library_notax_price`, `source_from_shop_id`, `rcv_shop_id`, `material_type_id`, `conversion_rate`, `project_id`, `project_no`, `task_id`, `task_no`, `source_from_type`, `source_from_id`, `source_from_row_id`, `source_from_qty`, `delivery_qty`, `attribute1`, `attribute2`, `attribute3`, `attribute4`, `attribute5`, `attribute6`, `attribute7`, `attribute8`, `attribute9`, `attribute10`, `attribute11`, `attribute12`, `attribute13`, `attribute14`, `attribute15`, `attribute16`, `attribute17`, `attribute18`, `attribute19`, `attribute20`, `attribute21`, `attribute22`, `attribute23`, `attribute24`, `attribute25`, `attribute26`, `attribute27`, `attribute28`, `attribute29`, `attribute30`, `attribute31`, `attribute32`, `attribute33`, `attribute34`, `attribute35`, `attribute36`, `attribute37`, `attribute38`, `attribute39`, `attribute40`, `attribute41`, `attribute42`, `attribute43`, `attribute44`, `attribute45`, `attribute46`, `attribute47`, `attribute48`, `attribute49`, `attribute50`, `tax_id`, `exceed_max_ratio`, `attachment`) "\
           "VALUES ('%s','875020602269642752', '875020602269642752', '%s', '798552414516971520', '半径2:; 材质:; 半径2:; 材质:; ', '[{\"esCode\":\"S42\",\"id\":796411489970814976,\"name\":\"半径2\",\"type\":1,\"value\":\"\"},{\"esCode\":\"S52\",\"id\":803563086572158976,\"name\":\"材质\",\"type\":3,\"value\":\"\"},{\"esCode\":\"S42\",\"id\":796411489970814976,\"name\":\"半径2\",\"type\":1,\"value\":\"\"},{\"esCode\":\"S52\",\"id\":803563086572158976,\"name\":\"材质\",\"type\":3,\"value\":\"\"}]', NULL, '111.00000000', NULL, '0', NULL, NULL, NULL, NULL, '0.10000000', '11.00000000', '0.01000000', '0.10000000', '11.10000000', '0.00000000', '0.00000000', '0.00000000', '0.00000000', '0.00000000', '0.00000000', '0.00000000', '0.00000000', '0.00000000', '864243997951406080', '111.00000000', NULL, '2021-08-11 14:19:29', '2021-08-11 14:19:29', '0', '539223256875155458', '539223256875155456', '539223256875155457', '1', '0', NULL, '0', '0', NULL, '0', '539223256875155457', '796166148106256384', '1.00000000', '0', '', '0', '', '0', '0', '0', NULL, NULL, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0', '0.00000000', NULL)"
	for i in range(500, 501):
		id = 875020602885808130+i
		params = [(id, i)]
		sql.writSql(mysql, params)

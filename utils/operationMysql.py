#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import pymysql
from utils.readConfig import readConfig


class mysqlUtils(object):
	readConfig = readConfig()

	def connMysql(self, DB):
		dict = self.readConfig.getMysql()
		conn = pymysql.connect(
			host=dict["IP"],
			port=dict["PORT"],
			user=dict["username"],
			passwd=dict["password"],
			db=DB)
		return conn

	def readSql(self, mysql, params=None, DB="test_srm"):
		try:
			conn = self.connMysql(DB)
			cur = conn.cursor()
		except Exception as e:
			return e.args
		else:
			cur.execute(mysql, params)
			data = cur.fetchall()
			db = [item for item in data]  # 列表推导式：相当于for循环
			return db
		finally:
			cur.close()
			conn.close()

	def writSql(self, mysql, params=None, DB="test_srm"):
		try:
			conn = self.connMysql(DB)
			cur = conn.cursor()
		except Exception:
			return Exception
		else:
			cur.executemany(mysql, params)  # 该方法执行时，参数列表的参数必须是元组，params = [(15, 2)]
			conn.commit()
		finally:
			cur.close()
			conn.close()


# if __name__ == '__main__':
# 	sql = mysqlUtils()
# 	mysql = "INSERT INTO `test_srm`.`pur_contract_type_attachment` (`parent_id`, `attachment_code`, `attachment_name`, `status`, `required`, `supplier_flag`, `remark`, `tenant_id`, `business_id`, `shop_id`, `creator_id`, `last_modifier_id`, `gmt_create`, `gmt_modified`, `del_flag`, `deleted_time`)  " \
# 	        "VALUES (%s, %s, 'sd', '1', '1', '0', 'sd', '539223256875155458', '539223256875155456', '539223256875155457', '852473181966573568', '852473181966573568', '2021-06-11 10:38:20', '2021-06-11 11:11:36', '0', '0')"
# 	for i in range(3, 48):
# 		params = [(15, i)]
# 		sql.writSql(mysql, params)

		
	# # print(sql.readSql(mysql="select * from question_list limit 1"))
	# mysql = "select * from supplier_performance_report where supplier_code=%s and exam_date like %s"
	# params = ('B21887', '%2021-01%')
	# print(sql.readSql(mysql, params))
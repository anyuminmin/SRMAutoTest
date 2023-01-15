#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.logger import Logger

log = Logger("publicBusiness").logger


class AssertService:

	def base_assert_for_success(self, response):
		"""基础断言"""
		assert response.json()['status'] == 0
		assert response.json()['success'] is True

	def assert_message_fail(self, response, failText):
		"""断言失败，断言messages信息"""
		assert response.json()['messages'][0]['message'] == failText
		assert response.json()['success'] is False

	def assert_text_equal(self, actual, expect):
		"""
		断言字符串相同，第一个参数传实际值，第二个参数传期望值
		:param actual:实际值
		:param expect:期望值
		return:
		"""
		#log.info('正在断言字符申实际值【'+str(actual)+,】和期望值【'+str(expect)+·】是否一致.·.')
		if actual == expect:
			log.info('字符串实际值【'+str(actual)+'】和期望值【'+str(expect)+'】一致，断言成功')
			assert True
		else:
			log.debug('字符串实际值【'+str(actual)+'】和期望值【'+str(expect)+'】不一致，断言失败...')
			assert False
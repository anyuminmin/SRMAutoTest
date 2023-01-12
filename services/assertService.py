#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An


class AssertService:

	def base_assert_for_success(self, response):
		assert response.json()['status'] == 0
		assert response.json()['success'] is True

	def assert_message_fail(self, response, failText):
		assert response.json()['messages'][0]['message'] == failText
		assert response.json()['success'] is False
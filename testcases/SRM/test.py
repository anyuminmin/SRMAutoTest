#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import requests
import math
import json


def test():
	host = "https://srm-test.chinaboilers.com"
	json = {"sapBatchNum": "20220328000001", "tenantId": "539223256875155458"}
	response = requests.post(
		url=host + "/api/srm/paymentSchedule/start",
		json=json
	)
	assert response.json()['success'] is True


def test_demo():
	host = "https://srm-demo-pre.chinaboilers.com"
	json = {"sapBatchNum": "20220522000001", "tenantId": "566673673418452995"}
	response = requests.post(
		url=host + "/api/srm/paymentSchedule/start",
		json=json
	)
	assert response.json()['success'] is True

def test_as():
	tPage = math.ceil(787/20)
	print(tPage)


def test_e():
	print(round(float("0.0")))
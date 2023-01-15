#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import requests
import os
import urllib3
import yaml
from utils.ase_tool import des_ecb_encrypt
from utils.logger import Logger
from services.httpService import HttpService
from utils.read_config import ReadConfig
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = Logger("BaseService").logger
http = HttpService()
read_config = ReadConfig()
headers = {"Content-Type": "application/json;charset=UTF-8"}
token_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token.yaml')


def srm_buyer_login(paramDict):
	# 传参类似：{"accountNo": "13136166390", "password": "test123456"}
	data = read_config.get_param("SRM/public/base.yaml", "SRM_BUYER_LOGIN")
	for i in paramDict:
		data[i] = paramDict.get(i)
	url = read_config.get_url("SRM/public/base.yaml", "SRM_BUYER_LOGIN")
	rsp = requests.post(
		url=url,
		json=data,
		headers=headers
	)
	return rsp.json()


def srm_buyer_choose_shop(paramDict):
	# securityToken, loginName, password, shopId
	data = read_config.get_param("SRM/public/base.yaml", "SRM_BUYER_CHOOSE_SHOP")
	for i in paramDict:
		data[i] = paramDict.get(i)
	rsp = requests.post(
		url=read_config.get_url("SRM/public/base.yaml", "SRM_BUYER_CHOOSE_SHOP"),
		json=data,
		headers=headers
	)
	return rsp.json()


def srm_supplier_login(paramDict):
	# loginName, password
	data = read_config.get_param("SRM/public/base.yaml", "SRM_SUPPLIER_LOGIN")
	for i in paramDict:
		data[i] = paramDict.get(i)
	rsp = requests.post(
		url=read_config.get_url("SRM/public/base.yaml", "SRM_SUPPLIER_LOGIN"),
		json=data,
		headers=headers
	)
	return rsp


def srm_supplier_choose_shop(paramDict):
	# securityToken, loginName, password, shopId
	data = read_config.get_param("SRM/public/base.yaml", "SRM_SUPPLIER_CHOOSE_SHOP")
	for i in paramDict:
		data[i] = paramDict.get(i)
	rsp = requests.post(
		url=read_config.get_url("SRM/public/base.yaml", "SRM_SUPPLIER_CHOOSE_SHOP"),
		json=data,
		headers=headers
	)
	return rsp


def srm_buyer_login_get_token():
	username = read_config.user["loginName"]
	password = read_config.user["password"]
	shop_id = read_config.shopId
	shop_name = read_config.shopName
	try:
		data = srm_buyer_login({"accountNo": username, "password": des_ecb_encrypt(password)})["data"]
		if not data['securityToken']:
			token = data['token']
		else:
			paramDict = {"loginName": username, "password": des_ecb_encrypt(password), "securityToken": data['securityToken'], "shopId": shop_id}
			token = srm_buyer_choose_shop(paramDict)["data"]["token"]
		with open(token_path, 'r', encoding='utf-8')as f:
			ele_info = f.read()
			yaml_dict = yaml.safe_load(ele_info)
		if yaml_dict is None:
			yaml_dict = dict()
		if yaml_dict.get(shop_name):
			yaml_dict.pop(shop_name)
		yaml_dict.setdefault(shop_name, token)
		with open(token_path, 'w', encoding='utf-8')as f:
			yaml.dump(yaml_dict, f, allow_unicode=True)
	except TypeError:
		log.info('!!!!!!!!!!!!!登录失败，没有拿到token!!!!!!!!!!!!'+'\n')
	except NameError:
		log.info('通过登录接口登录失败，没有拿到token,报错NameError:name,''token'',is not defined.,,')


def srm_supplier_login_get_token():
	username = read_config.user2["loginName"]
	password = read_config.user2["password"]
	shop_id = read_config.shopId2
	shop_name = read_config.shopName2
	try:
		data = srm_supplier_login({"accountNo": username, "password": des_ecb_encrypt(password)})["data"]
		if not data['securityToken']:
			token = data['token']
		else:
			paramDict = {"loginName": username, "password": des_ecb_encrypt(password), "securityToken": data['securityToken'], "shopId": shop_id}
			token = srm_supplier_choose_shop(paramDict)["data"]["token"]
		with open(token_path, 'r', encoding='utf-8')as f:
			ele_info = f.read()
			yaml_dict = yaml.safe_load(ele_info)
		if yaml_dict is None:
			yaml_dict = dict()
		if yaml_dict.get(shop_name):
			yaml_dict.pop(shop_name)
		yaml_dict.setdefault(shop_name, token)
		with open(token_path, 'w', encoding='utf-8')as f:
			yaml.dump(yaml_dict, f, allow_unicode=True)
	except TypeError:
		log.info('!!!!!!!!!!!登录失败，没有拿到token!!!!!!!!!!!'+'\n')
	except NameError:
		log.info('通过登求接口登求失收，没有拿到token,报错NameError:name,''token''is not defined...')


def srm_buyer_query_scm_person():
	"""查询人员部门接口"""
	data = read_config.get_param("SRM/public/base.yaml", "QUERY_SCM_PERSON")
	data['phoneNo'] = read_config.user["loginName"]
	rsp = http.post_json(
		url=read_config.get_url("SRM/public/base.yaml", "QUERY_SCM_PERSON"),
		data=data
	)
	rspDict = {}
	rspDict['deptId'] = rsp.json()['data']['list'][0]['deptId']
	rspDict['deptName'] = rsp.json()['data']['list'][0]['deptName']
	rspDict['userId'] = rsp.json()['data']['list'][0]['id']
	rspDict['personCode'] = rsp.json()['data']['list'][0]['personCode']
	rspDict['personName'] = rsp.json()['data']['list'][0]['personName']
	return rspDict


def srm_buyer_query_shop_by_token():
	data = read_config.get_param("SRM/public/base.yaml", "QUERY_SHOP_BY_TOKEN")
	rsp = http.post_json(
		url=read_config.get_url("SRM/public/base.yaml", "QUERY_SHOP_BY_TOKEN"),
		data=data
	)
	return rsp


def srm_buyer_query_user_permission_by_dept():
	"""获取权限接口"""
	rspDict = srm_buyer_query_scm_person()
	data = read_config.get_param("SRM/public/base.yaml", "QUERY_USER_PERMISSION_BY_DEPT")
	data['id'] = rspDict['deptId']
	rsp = http.post_json(
		url=read_config.get_url("SRM/public/base.yaml", "QUERY_USER_PERMISSION_BY_DEPT"),
		data=data
	)
	return rspDict


if __name__ == '__main__':
	srm_buyer_login_get_token()
	# srm_buyer_query_user_permission_by_dept()
	# srm_buyer_login({"accountNo": "13136166390", "password": "test123456"})




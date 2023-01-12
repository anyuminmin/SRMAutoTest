#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from utils.read_config import ReadConfig
from services.httpService import HttpService

read_config = ReadConfig()
http = HttpService()


def get_sourcing_template(paramDict):
	url = read_config.get_url("SRM/supplier_select/sourcing_template.yaml", "SOURCING_TEMPLATE_FUZZY_PAGE")
	param = read_config.get_param("SRM/supplier_select/sourcing_template.yaml", "SOURCING_TEMPLATE_FUZZY_PAGE")
	for i in paramDict:
		param[i] = paramDict.get(i)
	rsp = http.post_json(
		url=url,
		data=param
	)
	return rsp.json()
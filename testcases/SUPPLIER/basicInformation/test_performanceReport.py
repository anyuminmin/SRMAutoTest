#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import requests
from utils.requestBody import requestBody
import pytest
_requestBody = requestBody()


def test_select_report(supplier_headers):
	response = requests.post(
		url=_requestBody.getUrl('SUPPLIER_SELECT_PERFORMANCE_REPORT', 'SUPPLIER_uri.paramsYaml'),
		headers=supplier_headers,
		json=_requestBody.getParamsBody('SUPPLIER_SELECT_PERFORMANCE_REPORT', 'SUPPLIER_params.paramsYaml')
	)
	assert response.json()['success']is True


if __name__ == '__main__':
	pytest.main("-s,-v,test_performanceReport.py")

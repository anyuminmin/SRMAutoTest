#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import pytest
from services import loginService


@pytest.fixture()
def srm_buyer_login():
	loginService.srm_buyer_login_get_token()
	rspDict = loginService.srm_buyer_query_user_permission_by_dept()
	loginService.srm_buyer_query_shop_by_token()
	return rspDict

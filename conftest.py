#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import pytest
from services.common.loginService import LoginService


@pytest.fixture()
def srm_buyer_login():
	LoginService().srm_buyer_login_get_token()
	rspDict = LoginService().srm_buyer_query_user_permission_by_dept()
	LoginService().srm_buyer_query_shop_by_token()
	return rspDict

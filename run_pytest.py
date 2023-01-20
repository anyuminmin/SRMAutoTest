#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

import pytest
import os, time
from utils.read_config import ReadConfig

read_config = ReadConfig()
date = time.strftime('%Y%m%d%H%M%S', time.localtime())
report_path = os.path.join(read_config.base_path, "reports", str(date))
test_folder = os.path.join(read_config.base_path, "testcases")

def run_test():
	pytest.main(["-s", "-v", test_folder, '--alluredir=%s'%(report_path), '-o log_cli=true -o log_cli_level=INFO'])


if __name__ == '__main__':
	run_test()
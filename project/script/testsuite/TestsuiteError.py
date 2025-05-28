# -*- coding: UTF-8 -*-

"""
File Name:      TestsuiteNormal
Author:         zhangwei04
Create Date:    2018/1/5
"""

from framework.core.ipecker import *
from framework.core.testcase_base import TestSuiteBase, TestCaseBase
from framework.logger.logger import g_logger


class TestsuiteError(TestCaseBase, TestSuiteBase):
    def setup_testcase(self):
        assert_true(False, "TestsuiteError setup error")
        g_logger.info("this is test TestsuiteError setup")

    def teardown_testcase(self):
        g_logger.info("this is test TestsuiteError teardown")
# -*- coding: UTF-8 -*-

"""
File Name:      TestsuiteNormal
Author:         zhangwei04
Create Date:    2018/1/5
"""

from framework.core.ipecker import *
from framework.core.testcase_base import TestSuiteBase, TestCaseBase
from framework.logger.logger import g_logger


class TestsuiteClassify(TestCaseBase, TestSuiteBase):
    def setup_testcase(self):
        DUT.Common.reset_app()
        assert_true(DUT.Common.into_game_center(self.data.newgame), "分类用例集进入游戏中心", target=DUT)

    def teardown_testcase(self):
        pass
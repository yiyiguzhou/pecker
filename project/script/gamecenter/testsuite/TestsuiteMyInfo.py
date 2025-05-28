# -*- coding: UTF-8 -*-

"""
File Name:      TestsuiteMyInfo
Author:         zhangwei04
Create Date:    2019/3/5
"""
import time
from framework.core.ipecker import *
from framework.core.testcase_base import TestSuiteBase, TestCaseBase
from framework.logger.logger import g_logger


class TestsuiteMyInfo(TestCaseBase, TestSuiteBase):
    def setup_testcase(self):
        DUT.Common.reset_app()
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_password(account_section="phone_1"), "密码登录", target=DUT)
        time.sleep(2)

    def teardown_testcase(self):
        pass
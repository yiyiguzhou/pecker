# -*- coding: UTF-8 -*-

"""
File Name:      MyFeedback
Author:         gufangmei_sx
Create Date:    2018/9/14
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class MyFeedback(TestsuiteNormal):
    """
        用例描述：我的-反馈页
        预置条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):
        assert_true(DUT.Smoke.logout(), "退出登录", target=DUT)

    def teardown(self):
        DUT.device.stop_log()


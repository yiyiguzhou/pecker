# -*- coding: UTF-8 -*-

"""
File Name:      SwitchEnvironment
Author:         gufangmei_sx
Create Date:    2018/10/12
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class SwitchEnvironment(TestsuiteNormal):
    """
    用例描述：切换环境
    预置条件：
    """
    def setup(self):
        self.desc = "切换环境"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        time.sleep(1)
        assert_true(DUT.Common.into_game_center(self.data.classification, self.data.list), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.enter_setting(), "进入个人中心设置页面", target=DUT)
        assert_true(DUT.MyInfoPage.switch_environment(self.data.env_type), "切换环境", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
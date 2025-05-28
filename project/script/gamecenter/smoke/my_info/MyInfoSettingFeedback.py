# -*- coding: UTF-8 -*-

"""
File Name:      MyInfoSettingFeedback
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
# from project.script.testsuite.TestsuiteNormal import *
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *


class MyInfoSettingFeedback(TestsuiteMyInfo):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "个人中心-设置-提交反馈"
        DUT.device.start_log()
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.Common.back_to_homepage())

        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)
        assert_true(DUT.MyInfoPage.click_setting(), "个人中心页点击设置图标", target=DUT)
        assert_true(DUT.MyInfoPage.check_setting_ui(), "设置页检测UI", target=DUT)
        assert_true(DUT.MyInfoPage.setting_into_submit(), "进入反馈页", target=DUT)
        assert_true(DUT.MyInfoPage.submit_feedback(self.data.feedback_content, feedback_type=self.data.feedback_type, contact=self.data.feedback_contact),
                    "填写并提交反馈信息", target=DUT)
        assert_true(DUT.MyInfoPage.check_setting_ui(), "设置页检测UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

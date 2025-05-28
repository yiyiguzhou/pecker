# -*- coding: UTF-8 -*-

"""
File Name:      UserHistoryIntoLiteRoom
Author:         zhangwei04
Create Date:    2019/7/26
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class UserHistoryIntoLiteRoom(TestsuiteNormal):
    def setup(self):
        self.desc = "个人中心-观看历史-进入直播间"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.Home.into_user_center(), desc="进入个人中心", target=DUT)
        assert_true(DUT.UserPage.click_tab("观看历史"), desc='进入我的关注Tab', target=DUT)
        assert_true(DUT.UserPage.check_history_ui(), desc='检测观看历史页面', target=DUT)
        assert_true(DUT.UserPage.into_live_room(room_index=1), desc='进入关注的第一个直播间', target=DUT)
        assert_true(DUT.LiveRoom.check_room_ui(), desc='检测直播间UI', target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
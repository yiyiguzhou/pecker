# -*- coding: UTF-8 -*-

"""
File Name:      HomeHistoryIntoLiteRoom
Author:         zhangwei04
Create Date:    2019/7/24
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeHistoryIntoLiteRoom(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-观看历史-进入直播间"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)

        assert_true(DUT.Home.click_history(), desc="点击观看历史，弹出观看历史列表弹窗", target=DUT)
        assert_true(DUT.Home.history_into_live_room(index=self.data.index, anchor=self.data.anchor, title=self.data.title), desc="从观看历史列表进入直播间", target=DUT)
        assert_true(DUT.LiveRoom.check_room_ui(anchor=self.data.anchor, title=self.data.title), desc="检测直播间UI", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
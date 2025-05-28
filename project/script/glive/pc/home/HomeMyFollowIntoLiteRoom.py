# -*- coding: UTF-8 -*-

"""
File Name:      HomeMyFollowIntoLiteRoom
Author:         zhangwei04
Create Date:    2019/7/24
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeMyFollowIntoLiteRoom(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-我的关注-进入直播间"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)

        assert_true(DUT.Home.click_follow(), desc="点击我的关注，弹出关注列表弹窗", target=DUT)
        assert_true(DUT.Home.follow_into_live_room(index=self.data.index, anchor=self.data.anchor, title=self.data.title), desc="从我的关注列表进入直播间", target=DUT)
        assert_true(DUT.LiveRoom.check_room_ui(anchor=self.data.anchor, title=self.data.title), desc="检测直播间UI", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
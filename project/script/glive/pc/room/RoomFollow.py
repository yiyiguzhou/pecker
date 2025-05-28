# -*- coding: UTF-8 -*-

"""
File Name:      RoomFollow
Author:         zhangwei04
Create Date:    2019/7/31
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomFollow(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-关注主播"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.LiveRoom.unfollow(), desc="取消关注主播", target=DUT)
        assert_true(DUT.LiveRoom.follow(), desc="关注主播", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
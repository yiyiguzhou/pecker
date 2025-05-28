# -*- coding: UTF-8 -*-

"""
File Name:      RoomCloseRecharge
Author:         zhangwei04
Create Date:    2019/7/30
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomCloseRecharge(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-关闭6折弹窗"
        # DUT.Common.ansy_catch_tips()

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        # assert_true(DUT.LiveRoom.close_first_recharge(), desc="关闭首次充值6折弹窗", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()

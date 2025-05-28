# -*- coding: UTF-8 -*-

"""
File Name:      RoomChargeUI
Author:         zhangwei04
Create Date:    2019/7/31
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomChargeUI(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-充值-页面UI"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.LiveRoom.click_charge(), desc="点击充值按钮", target=DUT)
        assert_true(DUT.Home.check_charge_ui(check_price=True), desc="检测充值页UI", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
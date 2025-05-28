# -*- coding: UTF-8 -*-

"""
File Name:      RoomSendGoldGift
Author:         zhangwei04
Create Date:    2019/7/30
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomSendGoldGift(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-金币礼物赠送"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1', check_chat_ready=True), desc="密码登录", target=DUT)
        assert_true(DUT.LiveRoom.check_room_ui(self.data.anchor), desc="检测直播间UI", target=DUT)

        assert_true(DUT.LiveRoom.send_gift(gift_name=self.data.gift_name, count=self.data.count), desc="赠送金币礼物", target=DUT)
        assert_true(DUT.LiveRoom.check_chat_gift_info(account_section='user1', gift_name=self.data.gift_name, gift_num=self.data.count),
                    desc="检测直播间礼物信息", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()

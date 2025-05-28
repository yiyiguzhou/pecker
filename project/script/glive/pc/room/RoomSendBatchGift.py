# -*- coding: UTF-8 -*-

"""
File Name:      RoomSendBatchGift
Author:         zhangwei04
Create Date:    2019/8/1
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomSendBatchGift(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-礼物批量送礼"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1', check_chat_ready=True), desc="密码登录", target=DUT)
        # assert_true(DUT.LiveRoom.close_first_recharge(account_section='phone_1'), desc="", target=DUT)

        assert_true(DUT.LiveRoom.check_room_ui(self.data.anchor), desc="检测直播间UI", target=DUT)
        assert_true(DUT.LiveRoom.send_gift(gift_index=self.data.gift_index, gift_name=self.data.gift_name, count=self.data.count, group=self.data.group),
                    desc="批量赠送礼物", target=DUT)
        assert_true(DUT.LiveRoom.check_chat_gift_info(account_section='user1', gift_name=self.data.gift_name, gift_num=self.data.count,  group=self.data.group),
                    desc="检测直播间礼物信息", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
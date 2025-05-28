# -*- coding: UTF-8 -*-

"""
File Name:      RoomOtherSendGift
Author:         zhangwei04
Create Date:    2019/8/1
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomOtherSendGift(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-其他用户送礼"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1', check_chat_ready=True), desc="用户密码登录", target=DUT)
        DUTP.LiveRoom.leave_one_window()
        DUTP.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUTP.Login.password_login(account_section='user2', check_chat_ready=True), desc="辅助用户密码登录", target=DUTP)

        assert_true(DUT.LiveRoom.check_room_ui(self.data.anchor), desc="用户检测直播间UI", target=DUT)
        assert_true(DUTP.LiveRoom.check_room_ui(self.data.anchor), desc="辅助用户密码登录", target=DUTP)

        assert_true(DUTP.LiveRoom.send_gift(gift_index=self.data.gift_index, gift_name=self.data.gift_name, count=self.data.count),
                    desc="辅助用户赠送礼物", target=DUTP)
        assert_true(DUT.LiveRoom.check_chat_gift_info(account_section='user2', gift_name=self.data.gift_name, gift_num=self.data.count),
                    desc="用户检测直播间礼物信息", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
        DUTP.Home.leave_one_window()
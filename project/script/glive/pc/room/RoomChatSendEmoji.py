# -*- coding: UTF-8 -*-

"""
File Name:      RoomChatSendEmoji
Author:         zhangwei04
Create Date:    2019/7/31
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class RoomChatSendEmoji(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-聊天室-发送表情"
        # DUT.Common.ansy_catch_tips()

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1', check_chat_ready=True), desc="密码登录", target=DUT)
        # assert_true(DUT.LiveRoom.close_first_recharge(account_section='phone_1'), desc="")
        assert_true(DUT.LiveRoom.check_room_ui(self.data.anchor), desc="检测直播间UI", target=DUT)
        assert_true(DUT.LiveRoom.chat_clean_msg(), desc="清空聊天信息", target=DUT)
        assert_true(DUT.LiveRoom.chat_send_msg(self.data.text, emoji=self.data.emoji), desc="发送聊天信息", target=DUT)
        assert_true(DUT.LiveRoom.check_chat_text_msg(text=self.data.text, emoji=self.data.emoji, user_section='user1'),
                    desc="检测聊天信息", target=DUT)

    def teardown(self):
        # DUT.Common.stop_catch_tips()
        DUT.Home.leave_one_window()
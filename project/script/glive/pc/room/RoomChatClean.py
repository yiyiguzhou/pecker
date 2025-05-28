# -*- coding: UTF-8 -*-

"""
File Name:      RoomChatClean
Author:         zhangwei04
Create Date:    2019/8/1
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomChatClean(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-聊天室-清空消息"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.LiveRoom.chat_clean_msg(), desc="清空聊天室信息", target=DUT)
        assert_true(DUT.LiveRoom.check_chat_msg_cleaned(), desc="检测聊天室", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
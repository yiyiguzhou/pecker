# -*- coding: UTF-8 -*-

"""
File Name:      RoomChatBan
Author:         zhangwei04
Create Date:    2019/8/1
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomChatBan(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-聊天室-禁言"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1', check_chat_ready=True), desc="房管密码登录", target=DUT)
        DUTP.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUTP.Login.password_login(account_section='user2', check_chat_ready=True), desc="辅助用户密码登录", target=DUTP)
        assert_true(DUT.LiveRoom.ban_user(user_section="user2", target=DUTP), desc="用户禁言", target=DUT)
        time.sleep(3)  # 放置打字快提示
        assert_true(DUTP.LiveRoom.check_user_ban(), desc="辅助用户是否被禁言", target=DUTP)

    def teardown(self):
        DUT.Home.leave_one_window()
        DUTP.Home.leave_one_window()

# -*- coding: UTF-8 -*-

"""
File Name:      RoomPlayerPausePlay
Author:         zhangwei04
Create Date:    2019/8/9
"""
from project.script.testsuite.TestsuiteNormal import *


class RoomPlayerPausePlay(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-播放器-暂停-播放"

    def test(self):
        g_logger.info(self.desc)
        self.load_data(os.path.join(os.path.dirname(__file__), "RoomPlayerCommonData.xml"))
        DUT.LiveRoom.url_into_room(self.data.room_id, reload=False)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        DUT.LiveRoom.close_lottery_box()
        assert_true(DUT.RoomPlayer.pause(), desc="暂停播放", target=DUT)
        assert_true(DUT.RoomPlayer.check_pause(), desc="检测暂停Tips", target=DUT)
        assert_true(DUT.RoomPlayer.play(), desc="继续播放", target=DUT)
        assert_true(DUT.RoomPlayer.check_play(), desc="检测播放Tips", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
# -*- coding: UTF-8 -*-

"""
File Name:      RoomPlayerDanmuSwitch
Author:         zhangwei04
Create Date:    2019/8/9
"""
from project.script.testsuite.TestsuiteNormal import *


class RoomPlayerDanmuSwitch(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-播放器-关闭弹幕"

    def test(self):
        g_logger.info(self.desc)
        self.load_data(os.path.join(os.path.dirname(__file__), "RoomPlayerCommonData.xml"))
        DUT.LiveRoom.url_into_room(self.data.room_id, reload=False)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        DUT.LiveRoom.close_lottery_box()
        assert_true(DUT.RoomPlayer.click_danmu(), desc="关闭弹幕", target=DUT)
        assert_true(DUT.RoomPlayer.check_danmu_closed(), desc="检测弹幕处于关闭", target=DUT)
        assert_true(DUT.RoomPlayer.click_danmu(), desc="打开弹幕", target=DUT)
        assert_true(DUT.RoomPlayer.check_danmu_opened(), desc="检测弹幕处于打开", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
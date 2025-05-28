# -*- coding: UTF-8 -*-

"""
File Name:      RoomPlayerDanmu
Author:         zhangwei04
Create Date:    2019/8/12
"""
from project.script.testsuite.TestsuiteNormal import *


class RoomPlayerDanmu(TestsuiteNormal):
    """不适合做压测"""
    def setup(self):
        self.desc = "直播间-播放器-弹幕"

    def test(self):
        g_logger.info(self.desc)
        self.load_data(os.path.join(os.path.dirname(__file__), "RoomPlayerCommonData.xml"))
        DUT.LiveRoom.url_into_room(self.data.room_id)
        DUT.LiveRoom.close_lottery_box()
        expect_true(DUT.RoomPlayer.click_video_start_button(), desc="点击'播放按钮播放视频'", target=DUT)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.Login.password_login(account_section='user1', check_chat_ready=True), desc="密码登录", target=DUT)
        assert_true(DUT.RoomPlayer.check_video_start(), desc="通过发送弹幕，检测视频是否播放", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
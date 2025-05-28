# -*- coding: UTF-8 -*-

"""
File Name:      RoomPlayerVoice
Author:         zhangwei04
Create Date:    2019/8/9
"""
from project.script.testsuite.TestsuiteNormal import *


class RoomPlayerVoice(TestsuiteNormal):
    """不适合做压测"""
    def setup(self):
        self.desc = "直播间-播放器-音量调节"

    def test(self):
        g_logger.info(self.desc)
        self.load_data(os.path.join(os.path.dirname(__file__), "RoomPlayerCommonData.xml"))
        DUT.LiveRoom.url_into_room(self.data.room_id, reload=False)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        DUT.LiveRoom.close_lottery_box()
        assert_true(DUT.RoomPlayer.voice_swipe(0), desc="音量降为0%", target=DUT)
        assert_true(DUT.RoomPlayer.check_voice_percent(0), desc="检测音量为0%", target=DUT)
        assert_true(DUT.RoomPlayer.voice_swipe(100), desc="音量升为100%", target=DUT)
        assert_true(DUT.RoomPlayer.check_voice_percent(100), desc="检测音量为100%", target=DUT)
        assert_true(DUT.RoomPlayer.voice_swipe(50), desc="音量设置为50%", target=DUT)
        assert_true(DUT.RoomPlayer.check_voice_percent(50), desc="检测音量为50%", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
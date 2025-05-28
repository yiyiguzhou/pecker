# -*- coding: UTF-8 -*-

"""
File Name:      RoomPlayerReload
Author:         zhangwei04
Create Date:    2019/8/9
"""
from project.script.testsuite.TestsuiteNormal import *


class RoomPlayerReload(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-播放器-刷新"

    def test(self):
        g_logger.info(self.desc)
        self.load_data(os.path.join(os.path.dirname(__file__), "RoomPlayerCommonData.xml"))
        DUT.LiveRoom.url_into_room(self.data.room_id, reload=False)
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        DUT.LiveRoom.close_lottery_box()
        assert_true(DUT.RoomPlayer.reload(), desc="刷新直播间", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
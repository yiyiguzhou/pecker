# -*- coding: UTF-8 -*-

"""
File Name:      RoomNotLive
Author:         zhangwei04
Create Date:    2019/8/1
"""
from project.script.testsuite.TestsuiteNormal import *
import os


class RoomNotLive(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-未开播-状态检测"

    def test(self):
        g_logger.info(self.desc)
        DUT.LiveRoom.url_into_room(self.data.room_id)
        assert_true(DUT.LiveRoom.check_not_live(), desc="检测未开播状态", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()

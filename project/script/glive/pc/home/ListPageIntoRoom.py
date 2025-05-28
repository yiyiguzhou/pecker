# -*- coding: UTF-8 -*-

"""
File Name:      ListPageIntoRoom
Author:         zhangwei04
Create Date:    2019/7/23
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class ListPageIntoRoom(TestsuiteNormal):
    def setup(self):
        self.desc = "列表页-进入直播间"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        assert_true(DUT.Home.into_second_classify(self.data.classify), "进入{}列表页".format(self.data.classify), target=DUT)
        assert_true(DUT.LiveListPage.into_live_room(room_index=self.data.room_index, author=self.data.anchor, number=self.data.number),
                    "从列表页进入直播间", target=DUT)
        assert_true(DUT.LiveRoom.check_room_ui(self.data.classify, self.data.anchor, self.data.room_title), "检测直播间", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()

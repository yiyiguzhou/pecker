# -*- coding: UTF-8 -*-

"""
File Name:      MatchImg
Author:         gufangmei_sx
Create Date:    2018/9/7
"""
import time
from project.script.testsuite.TestsuiteNormal import *
import aircv as ac


class MatchImg(TestsuiteNormal):

    def setup(self):
        self.desc = "图像匹配"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        # assert_true(DUT.Common.matchimg("D:\\svn\\auto\\code\\ipecker\\project\\conf\\img\\1.png"), "图片匹配", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      ClassifyHomeLookAllGame
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class ClassifyHomeLookAllGame(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "分类-推荐页-专题模块-查看全部X款"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.goto_classify(), "进入分类页", target=DUT)
        assert_true(DUT.ClassifyPage.check_ui(), "检测分类页UI", target=DUT)
        assert_true(DUT.ClassifyPage.home_horizontal_look_all(self.data.topic_title), "检测点击查看全部XX款进入专题页", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

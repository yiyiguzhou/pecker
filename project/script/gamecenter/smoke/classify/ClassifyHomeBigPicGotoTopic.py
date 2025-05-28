# -*- coding: UTF-8 -*-

"""
File Name:      ClassifyHomeBigPicGotoTopic
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class ClassifyHomeBigPicGotoTopic(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "分类-推荐页-大图推荐位-专题详情页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.goto_classify(), "进入分类页", target=DUT)
        assert_true(DUT.ClassifyPage.check_home_ui(), "检测分类页UI", target=DUT)
        assert_true(DUT.ClassifyPage.home_click_big_pic(self.data.pic_pos), "点击大图进入专题详情页", target=DUT)
        assert_true(DUT.ClassifyPage.check_topic_ui(self.data.topic_title), "检测专题页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

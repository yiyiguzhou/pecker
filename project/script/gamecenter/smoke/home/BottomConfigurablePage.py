# -*- coding: UTF-8 -*-

"""
File Name:      BottomConfigurablePage
Author:         gufangmei_sx
Create Date:    2018/8/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *
from appium import webdriver


class BottomConfigurablePage(TestsuiteNormal):
    """
    用例描述：首页-底部栏-可配置运营位
    预置条件：首页底部栏可配置运营位配置了一个H5页面，且H5页面配置点击“下载”按钮可以进入游戏详情页并下载游戏。
    """
    def setup(self):
        self.desc = "首页-底部栏-可配置运营位"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info(self.data.check_desc)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Configurablepage.into_bottom_h5_game(), "进入底部栏H5游戏", target=DUT)
        assert_true(DUT.Configurablepage.h5_click_download(self.data.check_desc), "点击下载按钮并查看下载情况", target=DUT)
        DUT.Configurablepage.delete_game()

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      AuthPresure
Author:         zhangwei04
Create Date:    2018/3/1
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class DownloadPressure(TestsuiteNormal):
    def setup(self):
        DUT.device.start_log()

    def test(self):
        g_logger.info('压测下载先重启APP确保是从基线版本进入, 进入基线脚本页面')
        assert_true(DUT.Demo.reset_app(), u"重置app")
        g_logger.info("进入游戏中心界面")
        assert_true(DUT.Demo.into_gamecenter(), u"进入游戏中心")
        g_logger.info('搜索葫芦娃跑酷')
        assert_true(DUT.Demo.gamecenter_search('葫芦娃跑酷'), u'搜索葫芦娃跑酷')
        g_logger.info('进入葫芦娃跑酷下载页面')
        assert_true(DUT.Demo.into_game('葫芦娃跑酷'), u'进入葫芦娃跑酷下载页面')
        g_logger.info('下载葫芦娃跑酷游戏')
        assert_true(DUT.Demo.satrt_download_game(remove_app_id='com.daqu.huluwa2.iqiyi'), u"下载游戏")
        g_logger.info('安装游戏')
        assert_true(DUT.Demo.install_game_huawei_mate10(), u"安装游戏")
        g_logger.info('移除游戏')
        assert_true(DUT.Demo.remove_game('com.daqu.huluwa2.iqiyi'), u"移除游戏")

    def teardown(self):
        DUT.device.stop_log()

# -*- coding: UTF-8 -*-

"""
File Name:      GameDownload
Author:         gufangmei_sx
Create Date:    2018/7/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class GameDownload(TestsuiteNormal):
    """
    用例描述：游戏下载
    预置条件：
    """
    def setup(self):
        self.desc = "游戏下载"
        DUT.device.start_log()
        DUT.Common.uninstall_game_from_conf(self.data.game_name)
        DUT.Common.reset_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("游戏名：{}".format(self.data.game_name))
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "进入游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), "检测游戏详情页UI", target=DUT)
        assert_true(DUT.GameDetailPage.game_download_and_install(self.data.game_name, open_game=True), "下载游戏", target=DUT)
        assert_true(DUT.GameDetailPage.uninstall_app(app_name=self.data.game_name), "卸载游戏", target=DUT)
        DUT.Common.click_sys_installed_page()

    def teardown(self):
        DUT.device.stop_log()

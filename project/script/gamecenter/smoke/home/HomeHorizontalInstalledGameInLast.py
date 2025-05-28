# -*- coding: UTF-8 -*-

"""
File Name:      HomeIntoConfPortURL
Author:         zhangwei04
Create Date:    2018/11/19
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HomeHorizontalInstalledGameInLast(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "首页-横排-已安装游戏最后面"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("横排: {}".format(self.data.title))
        g_logger.info("游戏: {}".format(self.data.game_name))

        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.horizontal_into_game_detail(self.data.title, self.data.game_name), desc="进入横排游戏详情页", target=DUT)
        assert_true(DUT.GameDetailPage.game_download_and_install(self.data.game_name, open_game=False), desc="游戏下载与安装", target=DUT)
        time.sleep(2)
        g_logger.info("重启app，查看横排")
        DUT.Common.reset_app()
        assert_true(DUT.HomePage.into_game_center(self.data.newgame), "重启app后进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.check_horizontal_game_index_in_last(self.data.title, self.data.game_name), desc="检测游戏是否在横排最后一个", target=DUT)

    def teardown(self):
        assert_true(DUT.GameDetailPage.uninstall_app(app_name=self.data.game_name), "卸载游戏", target=DUT)
        DUT.device.stop_log()
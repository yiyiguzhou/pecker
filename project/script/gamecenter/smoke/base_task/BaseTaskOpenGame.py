# -*- coding: UTF-8 -*-

"""
File Name:      BaseTaskOpenGame
Author:         zhangwei04
Create Date:    2018/12/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class BaseTaskOpenGame(TestsuiteNormal):
    """
    预置条件：无
    """
    def setup(self):
        self.desc = "基线任务-游戏中心每日任务-启动游戏"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)

        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_password(account_section="platform_1"), "密码登录", target=DUT)

        DUT.Common.reset_app()
        time.sleep(5)
        if not DUT.Common.check_game_installed(self.data.game_name):
            g_logger.info("检测到游戏：{}未安装，安装游戏".format(self.data.game_name))
            assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
            time.sleep(5)
            assert_true(DUT.HomePage.game_search_click_icon(self.data.game_name), "搜索游戏", target=DUT)
            assert_true(DUT.GameDetailPage.check_ui(self.data.game_name), desc="检测游戏详情页UI", target=DUT)
            assert_true(DUT.GameDetailPage.game_download_and_install(self.data.game_name, open_game=False, timeout=30), desc="下载并安装游戏", target=DUT)
            DUT.Common.reset_app()
            time.sleep(10)
        assert_true(DUT.BasePage.into_my(), "进入基线我的", target=DUT)
        assert_true(DUT.BasePage.into_task_center(), "进入任务中心", target=DUT)
        assert_true(DUT.BasePage.task_center_into_list(), "任务中心进入任务列表", target=DUT)
        assert_true(DUT.BasePage.doing_start_game_task_list(self.data.game_name), "做启动游戏任务", target=DUT)

    def teardown(self):
        DUT.device.stop_log()


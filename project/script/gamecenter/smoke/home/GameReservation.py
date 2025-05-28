# -*- coding: UTF-8 -*-

"""
File Name:      GameReservation
Author:         gufangmei_sx
Create Date:    2018/8/10
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class GameReservation(TestsuiteNormal):
    """
    用例描述：首页-游戏预约下载安装-预约游戏
    预置条件：首页预约模板运营位配置了一个预约状态的非会员游戏
    """
    def setup(self):
        self.desc = "首页-游戏预约下载安装-预约游戏"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info('首页预约模板运营位配置了一个预约状态的非会员游戏')
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.login_in(self.data.account, self.data.password), "登录", target=DUT)
        assert_true(DUT.Common.check_title(self.data.title), "检查游戏预约标题", target=DUT)
        assert_true(DUT.HomePage.click_reservation_button(self.data.game_name, self.data.promt, self.data.button), "点击预约按钮", target=DUT)
        # assert_true(DUT.HomePage.click_reservation_button(self.data.game_name, self.data.promt, self.data.button), "检查游戏是否预约成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
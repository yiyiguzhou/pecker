# -*- coding: UTF-8 -*-

"""
File Name:      DailyRecommendation
Author:         gufangmei_sx
Create Date:    2018/8/1
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class DailyRecommendation(TestsuiteNormal):
    """
        用例描述：每日推荐
        预置条件：配置第一个游戏是已上线游戏，第二个游戏是H5游戏
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):

        # assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        # assert_true(DUT.Smoke.check_event_title(self.data.title), "检查活动文字", target=DUT)
        assert_true(DUT.Smoke.check_title(self.data.game3), "检查活动文字", target=DUT)
        assert_true(DUT.Smoke.check_game_name(self.data.game1, self.data.game2, self.data.game3, self.data.game4), "检查每日推荐游戏信息", target=DUT)
        assert_true(DUT.Smoke.check_enter_button(), "检查进入按钮", target=DUT)
        assert_true(DUT.Smoke.click_enter_button1(), "点击第一个进入按钮", target=DUT)
        # assert_true(DUT.Smoke.click_enter_button2(), "点击第二个进入按钮", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

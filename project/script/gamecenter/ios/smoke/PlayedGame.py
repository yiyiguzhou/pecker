# -*- coding: UTF-8 -*-

"""
File Name:      PlayedGame
Author:         gufangmei_sx
Create Date:    2018/9/18
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class PlayedGame(TestsuiteNormal):
    """
        用例描述：我的页-最近玩过
        预置条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):
        assert_true(DUT.Smoke.into_ios_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.base_my_game(), "进入我的游戏", target=DUT)
        assert_true(DUT.Smoke.check_event_title(self.data.title), "检查活动文字", target=DUT)
        assert_true(DUT.Smoke.check_doudizhu_game('//Users//wzhang//doc//svn//auto//code//ipecker//project//conf//img//1.png'), "检查斗地主游戏显示样式", target=DUT)
        assert_true(DUT.Smoke.click_doudizhu_game(), "点击斗地主游戏的游戏行", target=DUT)
        assert_true(DUT.Smoke.click_enter_doudizhu('//Users//wzhang//doc//svn//auto//code//ipecker//project//conf//img//2.png'), "点击进入游戏", target=DUT)
        assert_true(DUT.Smoke.click_play_now('//Users//wzhang//doc//svn//auto//code//ipecker//project//conf//img//3.png'), "点击“点击立即试玩”", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

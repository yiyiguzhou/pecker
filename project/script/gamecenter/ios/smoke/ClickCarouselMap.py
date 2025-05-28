# -*- coding: UTF-8 -*-

"""
File Name:      ClickCarouselMap
Author:         gufangmei_sx
Create Date:    2018/7/31
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class ClickCarouselMap(TestsuiteNormal):

    def setup(self):
        DUT.device.start_log()
        DUT.Smoke.reset_app()

    def test(self):

        assert_true(DUT.Smoke.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.Smoke.click_carouse_map(), "点击轮播图", target=DUT)
        time.sleep(3)

    def teardown(self):
        DUT.device.stop_log()
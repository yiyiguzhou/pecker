# -*- coding: UTF-8 -*-

"""
File Name:      PingbackDemo
Author:         zhangwei04
Create Date:    2018/8/24
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class PingbackDemo(TestsuiteNormal):
    def setup(self):
        DUT.Pingback.reset_app()
        DUT.Pingback.start_catch()

    def test(self):
        assert_true(DUT.Pingback.into_game_center(), target=DUT)
        assert_true(DUT.Pingback.gamecenter_into_new_game(), target=DUT)

    def teardown(self):
        DUT.Pingback.stop_catch()
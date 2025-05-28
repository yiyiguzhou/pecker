# -*- coding: UTF-8 -*-

"""
File Name:      TestGameCenter1
Author:         zhangwei04
Create Date:    2018/1/8
"""

import time
from project.script.testsuite.TestsuiteError import *


class TestGameCenterError1(TestsuiteError):

    def setup(self):
        g_logger.info("this is TestGameCenterError1 setup")

    def test(self):
        time.sleep(1)
        g_logger.info("this is TestGameCenterError1 test")

        assert_true(True, "test true")

    def teardown(self):
        g_logger.info("this is TestGameCenterError1 teardown")


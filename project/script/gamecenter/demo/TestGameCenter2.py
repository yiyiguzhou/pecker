# -*- coding: UTF-8 -*-

"""
File Name:      TestGameCenter1
Author:         zhangwei04
Create Date:    2018/1/8
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class TestGameCenter2(TestsuiteNormal):

    def setup(self):
        g_logger.info("this is TestGameCenter2 setup")

    def test(self):
        time.sleep(1)
        g_logger.info("this is TestGameCenter2 test")
        assert_true(False, "test false")

    def teardown(self):
        g_logger.info("this is TestGameCenter2 teardown")


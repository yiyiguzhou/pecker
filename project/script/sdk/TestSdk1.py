# -*- coding: UTF-8 -*-

"""
File Name:      test_sdk1
Author:         zhangwei04
Create Date:    2017/12/27
"""
import time
import random
from ..testsuite.TestsuiteNormal import *


class TestSdk1(TestsuiteNormal):

    def setup(self):
        g_logger.info("this is TestSdk1 setup")

    def test(self):
        DUT.Demo.test()
        # DUT1.Demo.test()
        time.sleep(1)
        g_logger.info("this is TestSdk1 test")

        g_logger.debug("debug test")
        g_logger.info("info test")
        g_logger.warning("warning test")
        g_logger.error("error test")
        g_logger.critical("critical test")
        rand_num = random.randint(0, 10)
        if rand_num < 4:
            assert_true(False, "test False")

    def teardown(self):
        g_logger.info("this is TestSdk1 teardown")

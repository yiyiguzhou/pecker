# -*- coding: UTF-8 -*-

"""
File Name:      test_sdk1
Author:         zhangwei04
Create Date:    2017/12/27
"""
import time
from ..testsuite.TestsuiteNormal import *


class TestSdk2(TestsuiteNormal):

    def setup(self):
        g_logger.info("this is TestSdk2 setup")

    def test(self):
        time.sleep(1)
        g_logger.info("this is TestSdk2 test")

        assert_true(False, "test TestSdk2 false")

    def teardown(self):
        g_logger.info("this is TestSdk2 teardown")


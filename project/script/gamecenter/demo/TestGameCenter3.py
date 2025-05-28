# -*- coding: UTF-8 -*-

"""
File Name:      TestGameCenter1
Author:         zhangwei04
Create Date:    2018/1/8
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class TestGameCenter3(TestsuiteNormal):

    def setup(self):
        g_logger.info("this is TestGameCenter3 setup")

    def test(self):
        time.sleep(1)
        g_logger.info("this is TestGameCenter3 test")

        g_logger.debug("debug TestGameCenter3")
        g_logger.info("info TestGameCenter3")
        g_logger.warning("warning TestGameCenter3")
        g_logger.error("error TestGameCenter3")
        expect_true(False,
                    "test TestGameCenter3  except failed")
        assert_true(False,
                    "test TestGameCenter3 failed")
        if int(time.time() % 2) == 0:
            assert_true(True, "TestGameCenter3 true")
        else:
            assert_true(False,
                        "test TestGameCenter3 failed")

    def teardown(self):
        g_logger.info("this is TestGameCenter3 teardown")


# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseData
Author:         zhangwei04
Create Date:    2018/2/7
"""
from ..testsuite.TestsuiteNormal import *
import os
import random


class TestError(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        expect_true(True, "testError")
        # if random.randint(0, 3) % 3 == 0:
        raise Exception("testcase exception")

    def teardown(self):
        pass

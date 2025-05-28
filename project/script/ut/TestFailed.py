# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseData
Author:         zhangwei04
Create Date:    2018/2/7
"""
from ..testsuite.TestsuiteNormal import *
import os


class TestFailed(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        assert_true(False, "testFailed")
        pass

    def teardown(self):
        pass

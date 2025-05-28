# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseData
Author:         zhangwei04
Create Date:    2018/2/7
"""
from ..testsuite.TestsuiteNormal import *
import os

class TestCaseData(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        g_logger.info(self.data.username)
        g_logger.info(self.data.password)
        g_logger.info(self.data.looptimes)
        self.load_data(os.path.join(os.path.dirname(__file__), 'TestCaseData1.xml'))
        g_logger.info(self.data.username)
        g_logger.info(self.data.password)
        g_logger.info(self.data.looptimes)
        pass

    def teardown(self):
        pass

# -*- coding: UTF-8 -*-

"""
File Name:      Game_topList
Author:         xumohan
Create Date:    2018/7/18
"""

from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.testcase import testcase_reader_file_sheet as ts


class MixedGame_androidAndH5TodayOnline(TestsuiteNormal):
    def setup(self):
        #DUT.device.start_log()
        pass

    def test(self):
        file = os.path.join(os.path.dirname(__file__), 'MixedGame_androidAndH5TodayOnline.xml')
        ts.run_test_case(file)

    def teardown(self):
        #DUT.device.stop_log()
        pass
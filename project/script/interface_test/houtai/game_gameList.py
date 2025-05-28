# -*- coding: UTF-8 -*-

"""
File Name:      CardCardList
Author:         xumohan
Create Date:    2018/7/16
"""
import os
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.testcase import testcase_reader_file_sheet as ts


class game_gameList(TestsuiteNormal):
    def setup(self):
        #DUT.device.start_log()
        pass

    def test(self):
        file = os.path.join(os.path.dirname(__file__), 'game_gameList.xml')
        ts.run_test_case(file)

    def teardown(self):
        #DUT.device.stop_log()
        pass
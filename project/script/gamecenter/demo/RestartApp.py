# -*- coding: UTF-8 -*-

"""
File Name:      SmsLogin
Author:         zhangwei04
Create Date:    2018/4/9
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class RestartApp(TestsuiteNormal):
    def setup(self):
        DUT.device.start_log()

    def test(self):
        for times in range(int(self.data.times)):
            g_logger.info("第{}次重启".format(times + 1))
            DUT.Demo.reset_app()
            time.sleep(3)

    def teardown(self):
        DUT.device.stop_log()

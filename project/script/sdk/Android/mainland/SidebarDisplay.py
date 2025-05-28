"""
File Name:      SidebarDisplay
Author:         xuxiaofang_sx
Create Date:    2018/7/13
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class SidebarDisplay(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Sidebar.Sidebar_display(), "侧边栏登录页面", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
"""
File Name:      SidebarDisplayPop-ups
Author:         xuxiaofang_sx
Create Date:    2018/7/18
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class SidebarDisplayPopUps(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Sidebar.Sidebar_display_pop_ups(), "进入福利页面成功", target=DUT)
        assert_true(DUT.Sidebar.sidebar_message_box(), "进入消息盒页面成功", target=DUT)
        assert_true(DUT.Sidebar.sidebar_privilege(), "进入特权页面成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
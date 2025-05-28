"""
File Name:      DragSidebar
Author:         xuxiaofang_sx
Create Date:    2018/7/23
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class DragSidebar(TestsuiteNormal):
    """
        用例描述：拖动侧边栏
        预制条件：无
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Sidebar.Drag_sidebar(), "托动侧边栏成功", target=DUT)
        assert_true(DUT.Sidebar.Sidebar_display(), "侧边栏登录页面", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
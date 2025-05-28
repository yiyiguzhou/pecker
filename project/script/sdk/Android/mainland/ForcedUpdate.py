"""
File Name:      ForcedUpdate
Author:         xuxiaofang_sx
Create Date:    2018/7/19
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class ForcedUpdate(TestsuiteNormal):
    """
        用例描述：强制更新
        预制条件：该测试游戏配置了符合条件的插件更新包，并且更新方式是：强制更新
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):

        assert_true(DUT.Mainland.force_update_interface(), "强制页面更新显示成功成功", target=DUT)
        time.sleep(3)
        assert_true(DUT.Mainland.force_update(), "强制页面更新成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
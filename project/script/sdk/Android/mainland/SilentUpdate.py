"""
File Name:      SilentUpdate
Author:         xuxiaofang_sx
Create Date:    2018/7/16
"""
import time
from project.script.testsuite.TestsuiteNormal import *

class SilentUpdate(TestsuiteNormal):
    """
        用例描述：静默更新
        预制条件：该测试游戏配置了符合条件的插件更新包，并且更新方式是：静默更新
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        time.sleep(3)
        assert_true(DUT.Mainland.silent_update(), "静默更新成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

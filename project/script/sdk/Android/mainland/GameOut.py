"""
File Name:      GameOut
Author:         xuxiaofang_sx
Create Date:    2018/7/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *

class GameOut(TestsuiteNormal):
    """
        用例描述：游戏退出引导页显示
        预制条件：测试的游戏已配置退出引导
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Exit.game_out(), "游戏退出成功页面", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
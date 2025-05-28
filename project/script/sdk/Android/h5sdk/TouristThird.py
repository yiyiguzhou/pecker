"""
File Name:      Tourist_third
Author:         xuxiaofang_sx
Create Date:    2018/8/9
"""
import time
from project.script.testsuite.TestsuiteNormal import *

class TouristThird(TestsuiteNormal):
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.into_mygame_page(self.data.title), "成功进入爱奇艺小游戏", target=DUT)
        time.sleep(5)
        assert_true(DUT.H5sdk.coin(), "成功进入小游戏", target=DUT)
        assert_true(DUT.H5sdk.sidebar(self.data.is_tourist,self.data.is_sms), "成功进入侧边栏切换账号页面", target=DUT)
        assert_true(DUT.H5sdk.qq_login(), "成功进入qq页面", target=DUT)
    def teardown(self):
        DUT.device.stop_log()
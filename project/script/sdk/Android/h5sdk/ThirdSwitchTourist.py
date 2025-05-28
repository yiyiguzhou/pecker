"""
File Name:      ThirdSwitchTourist
Author:         xuxiaofang_sx
Create Date:    2018/8/10
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class ThirdSwitchTourist(TestsuiteNormal):
    """
        用例描述：第三方登录切换游客账号
        预制条件：1.本地没有缓存的手机
                  2.基线无登录状态
        """
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        time.sleep(2)
        assert_true(DUT.H5sdk.into_mygame_page(self.data.title), "成功进入爱奇艺小游戏页面", target=DUT)
        time.sleep(5)
        assert_true(DUT.H5sdk.coin(), "成功进入小游戏", target=DUT)
        assert_true(DUT.H5sdk.sidebar(self.data.is_tourist,self.data.is_sms,self.data.phone_num), "成功进入侧边栏切换账号进入qq登录页面", target=DUT)
        assert_true(DUT.H5sdk.qq_login(), "成功进入qq页面", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
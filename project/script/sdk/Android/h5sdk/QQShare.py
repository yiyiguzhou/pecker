"""
File Name:      QQShare
Author:         xuxiaofang_sx
Create Date:    2018/8/15
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class QQShare(TestsuiteNormal):
    """
        用例描述：QQ好友分享
        预制条件：无
        """
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.into_mygame_page(self.data.title), "成功进入爱奇艺小游戏", target=DUT)
        time.sleep(5)
        assert_true(DUT.H5sdk.coin(), "成功进入小游戏", target=DUT)
        assert_true(DUT.H5sdk.share(self.data.title1), "点击侧边栏切换账号进入分享页面", target=DUT)
        assert_true(DUT.H5sdk.qq_share(self.data.qq_account,self.data.qq_password), "QQ分享成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
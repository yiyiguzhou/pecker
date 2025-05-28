"""
File Name:      PhoneRealAuthentication
Author:         xuxiaofang_sx
Create Date:    2018/8/16
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class PhoneRealAuthentication(TestsuiteNormal):
    """
        用例描述：手机实名认证
        预制条件：1.账号未实名认证、实名认证
                  2.未注册过手机
                  3.注册过手机
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
        assert_true(DUT.H5sdk.sidebar(self.data.is_tourist,self.data.is_sms,self.data.phone_num), "进入其他登录方式页面成功", target=DUT)
        assert_true(DUT.H5sdk.sina_login(self.data.sina_account,self.data.sina_password), "新浪账号登录成功", target=DUT)
        assert_true(DUT.H5sdk.mobileauthentication(self.data.phone_num), "手机实名认证成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
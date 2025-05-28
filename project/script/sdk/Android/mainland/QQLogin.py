"""
File Name:      QQLogin
Author:         xuxiaofang_sx
Create Date:    2018/7/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class QQLogin (TestsuiteNormal):
    """
        用例描述：   QQ授权登录
        预制条件：1.该游戏支持qq授权登录
                  2.手机上有安装爱奇艺app,并且是已登录状态
                  3.is_qq：应设置为TRUE
                  4.vip_time:会员到期时间
                  5.qq：QQ账号
                  6.qq_password：QQ密码
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Registered.initialize_QQ_login(), "初始化QQ登陆", target=DUT)
        assert_true(DUT.Registered.qq_login_interface(self.data.is_qq,self.data.vip_time), "拉起qq登陆页面", target=DUT)
        assert_true(DUT.Registered.qq(self.data.qq,self.data.qq_password), "qq登陆成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
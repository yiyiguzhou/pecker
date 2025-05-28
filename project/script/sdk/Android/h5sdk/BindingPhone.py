"""
File Name:      BindingPhone
Author:         xuxiaofang_sx
Create Date:    2018/8/17
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class BindingPhone(TestsuiteNormal):
    """
        用例描述：绑定账号
        预制条件：1.账号未绑定手机
                  2.该手机注册过，手机没有
                  title:进入小游戏页面标题
                  phone_num1：
                  phone_num2:
                  new_password:
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
        assert_true(DUT.H5sdk.sidebar_binding(), "成功进入绑定页面", target=DUT)
        assert_true(DUT.H5sdk.binding_phone(self.data.phone_num1,self.data.phone_num2,self.data.new_password), "绑定账号", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
"""
File Name:      IqiyiLogin
Author:         xuxiaofang_sx
Create Date:    2018/7/25
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class IqiyiLogin(TestsuiteNormal):
    """
        用例描述：爱奇艺一键授权登录
        预制条件：1.手机无爱奇艺游戏用户缓存
                  2.奇玩后台极速登录云配开关为开启（position_id：43为关闭）
                  3.不满足授权登录的条件
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_iqiyi_app()
        DUT.Mainland.reset_app()

    def test(self):

        assert_true(DUT.Mainland.iqiyi_login(), "爱奇艺授权登录成功", target=DUT)



    def teardown(self):
        DUT.device.stop_log()
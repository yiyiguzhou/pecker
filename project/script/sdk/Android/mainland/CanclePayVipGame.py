"""
File Name:      CanclePayVipGame
Author:         xuxiaofang_sx
Create Date:    2018/8/8
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class CanclePayVipGame(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.reset_app()

    def test(self):
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Mainland.game_vip_page(), "会员卡购买页面显示正常", target=DUT)
        assert_true(DUT.Mainland.buy_vip_game(), "进入支付中心页面", target=DUT)
        assert_true(DUT.Mainland.cancel_payment(), "取消支付成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
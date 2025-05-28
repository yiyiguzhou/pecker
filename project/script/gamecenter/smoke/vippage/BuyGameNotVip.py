# -*- coding: UTF-8 -*-

"""
File Name:      BuyGameNotVip
Author:         gufangmei_sx
Create Date:    2018/7/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class BuyGameNotVip(TestsuiteNormal):
    """
    用例描述：游戏会员页-非会员-购买游戏-只可租用
    预置条件：用户未非会员，存在一款只可租用价格为：1奇贝的游戏，手机未安装支付宝应用
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Common.start_ipecker_app()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info("用户未非会员，存在一款只可租用价格为：1奇贝的游戏，手机未安装支付宝应用")
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入基线登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_password(self.data.account, self.data.password), "密码登录", target=DUT)
        assert_true(DUT.Common.back_to_homepage(), "返回游戏中心首页", target=DUT)
        assert_true(DUT.VipPage.into_vip_page(self.data.title), "进入游戏会员页", target=DUT)
        assert_true(DUT.HomePage.swipe_down_into_game_detail(self.data.game_name), "寻找1奇贝的游戏", target=DUT)
        assert_true(DUT.VipPage.click_1qibei_icon(self.data.order_confirm), "订单确认", target=DUT)
        assert_true(DUT.Common.check_title(self.data.rent_title), "检查标题", target=DUT)
        assert_true(DUT.Common.check_title(self.data.rent_price), "检查金额", target=DUT)
        assert_true(DUT.VipPage.click_pay_icon(), "立即支付", target=DUT)
        assert_true(DUT.Common.click_and_check_button(self.data.open_vip, self.data.actionBar_title), "开通会员", target=DUT)
        assert_true(DUT.VipPage.buy_vip_game(self.data.alipay_account, self.data.alipay_password, self.data.game_name), "购买游戏", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
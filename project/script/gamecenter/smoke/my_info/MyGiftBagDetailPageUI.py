# -*- coding: UTF-8 -*-

"""
File Name:      MyGiftBagDetailPageUI
Author:         zhangwei04
Create Date:    2018/1/2
"""
import time
from project.script.gamecenter.testsuite.TestsuiteMyInfo import *
# from project.script.testsuite.TestsuiteNormal import *


class MyGiftBagDetailPageUI(TestsuiteMyInfo):
    """
    预置条件：账户有礼包
    """
    def setup(self):
        self.desc = "个人中心-我的礼包详情页UI"
        DUT.device.start_log()
        # DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        # assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        #         # assert_true(DUT.Common.into_game_center(self.data.newgame), "进入游戏中心", target=DUT)
        #         # assert_true(DUT.Login.into_login_page(), "进入游戏中心登录页面", target=DUT)
        #         # assert_true(DUT.Login.login_in_with_password(account_section="phone_1"), "密码登录", target=DUT)
        assert_true(DUT.Common.back_to_homepage())
        assert_true(DUT.HomePage.into_my_info(), "进入个人中心", target=DUT)
        time.sleep(3)
        assert_true(DUT.MyInfoPage.click_my_gift(), "点击我的礼包", target=DUT)
        # assert_true(DUT.MyInfoPage.check_my_gift_page_ui(), "检测我的礼包页UI", target=DUT)
        assert_true(DUT.MyInfoPage.gift_into_gift_detail(self.data.gift_name), "进入礼包详情页", target=DUT)
        assert_true(DUT.MyInfoPage.check_gift_detail_ui(self.data.gift_name), "检测礼包详情页UI", target=DUT)

    def teardown(self):
        DUT.device.stop_log()

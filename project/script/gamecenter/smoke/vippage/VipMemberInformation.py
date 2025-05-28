# -*- coding: UTF-8 -*-

"""
File Name:      VipMemberInformation
Author:         gufangmei_sx
Create Date:    2018/7/12
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class VipMemberInformation(TestsuiteNormal):
    """
    用例描述：游戏会员页-充值会员-点击会员信息模块
    预置条件：用户为充值会员
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info("用户为充值会员")
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Login.into_login_page(), "进入基线登录页面", target=DUT)
        assert_true(DUT.Login.login_in_with_password(self.data.account, self.data.password), "密码登录", target=DUT)
        assert_true(DUT.Common.back_to_homepage(), "返回游戏中心首页", target=DUT)
        assert_true(DUT.VipPage.into_vip_page(self.data.title), "进入游戏会员页", target=DUT)
        assert_true(DUT.Common.click_right_arrow(self.data.actionBar_title), "进入我的游戏会员", target=DUT)
        assert_true(DUT.Common.check_title(self.data.button_name), "立即续费", target=DUT)
        assert_true(DUT.Common.check_title(self.data.qibei), "奇贝余额", target=DUT)
        assert_true(DUT.Common.check_title(self.data.qibei_value), "奇贝数值", target=DUT)
        assert_true(DUT.Common.click_and_check(self.data.qibei, self.data.qibei_recharge), "进入奇贝充值页面", target=DUT)
        time.sleep(5)
        assert_true(DUT.Common.check_title(self.data.qibei_recording), "奇贝记录", target=DUT)
        assert_true(DUT.Common.click_and_check(self.data.qibei_recording, self.data.qibei_recording),"进入奇贝记录页面", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
# -*- coding: UTF-8 -*-

"""
File Name:      MemberInformation
Author:         gufangmei_sx
Create Date:    2018/7/12
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class MemberInformation(TestsuiteNormal):
    """
    用例描述：游戏会员页-未登录-点击会员信息模块
    预置条件：用户未登录
    """
    def setup(self):
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info("用户为非会员")
        time.sleep(3)
        assert_true(DUT.Login.base_login_out(), "退出登录", target=DUT)
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.VipPage.into_vip_page(self.data.entrance, self.data.title), "进入游戏会员页", target=DUT)
        assert_true(DUT.Common.click_and_check(self.data.button_name, self.data.text), "进入购买会员页", target=DUT)
        assert_true(DUT.Common.click_and_check(self.data.open_icon, self.data.login), "开通会员页", target=DUT)
        assert_true(DUT.Login.login_in_with_password(self.data.account, self.data.password), "账号登录", target=DUT)
        assert_true(DUT.Common.check_title_xpath(self.data.actionBar_title), "检查登录后的页面标题", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
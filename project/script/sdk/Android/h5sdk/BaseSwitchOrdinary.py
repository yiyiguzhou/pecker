"""
File Name:      HomeSwitchSms
Author:         xuxiaofang_sx
Create Date:    2018/8/10
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class BaseSwitchOrdinary(TestsuiteNormal):
    """
        用例描述：基线切普通账号登录
        预制条件：1.本地没有缓存的手机
                  2.基线登录状态
                  phone：基线手机账号
                  base_password：基线账号密码
                  game_text：游戏名称
                  account_display：基线账号显示
                  game_account：游戏中心账号
                  game_password：游戏中心密码
                  is_tourist：是否要游客方式登录 应设置为false
                  is_sms：是否要短信方式登录 应设置为false
                  phone_num:短信登录时的手机号码
        """
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.no_cache())
        assert_true(DUT.H5sdk.mycount(self.data.phone, self.data.base_password), "基线登陆成功", target=DUT)
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.gamecenter_search(self.data.game_text), "进入搜索框成功", target=DUT)
        assert_true(DUT.H5sdk.into_gamedetail(self.data.game_text), "进入游戏详情成功", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "进入非棋牌游戏成功", target=DUT)
        assert_true(DUT.H5sdk.sidebar(self.data.is_tourist, self.data.is_sms, self.data.phone_num), "点击侧边栏切换账号进入普通登录页面", target=DUT)
        assert_true(DUT.H5sdk.password_login(self.data.game_account, self.data.game_password), "普通账号登录成功", target=DUT)
        assert_true(DUT.H5sdk.phone_return(), "点击物理返回键成功退出游戏", target=DUT)
        assert_true(DUT.H5sdk.into_h5game(self.data.game_text), "再次进入非棋牌游戏成功", target=DUT)
        assert_true(DUT.H5sdk.account_display(self.data.account_display,self.data.game_account, self.data.game_password), "账号显示正确", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
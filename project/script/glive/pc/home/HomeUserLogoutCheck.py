# -*- coding: UTF-8 -*-

"""
File Name:      PasswordLogin
Author:         zhangwei04
Create Date:    2019/7/19
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class HomeUserLogoutCheck(TestsuiteNormal):
    def setup(self):
        self.desc = "首页-个人信息-退出登录检测状态同步"

    def test(self):
        DUT.Home.into_home()
        g_logger.info(self.desc)
        title = self.data.title
        assert_true(DUT.Login.password_login(account_section='user1'), desc="密码登录", target=DUT)
        assert_true(DUT.Login.logout(), desc="退出登录", target=DUT)
        assert_true(DUT.Home.into_side_list_title(title), desc="查找导航列表，点击标题{}".format(title), target=DUT)
        assert_true(DUT.Home.check_subtitle_page(title), desc="检测跳转后的标题页", target=DUT)
        assert_true(DUT.LiveListPage.into_live_room(room_index=1), desc="进入第一个直播间", target=DUT)
        assert_false(DUT.Login.is_login(), desc='检测用户不在登录状态', target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
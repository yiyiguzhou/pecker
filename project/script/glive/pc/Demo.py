# -*- coding: UTF-8 -*-

"""
File Name:      Demo
Author:         zhangwei04
Create Date:    2019/7/12
"""


from project.script.testsuite.TestsuiteNormal import *
import os


class Demo(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        DUT.Demo.into_home()
        # assert_true(DUT.Demo.click_classify("英雄联盟"), "点击英雄联盟标签")
        # assert_true(DUT.Demo.check_classify_active("英雄联盟"), "检测英雄联盟标签")
        # assert_true(DUT.Demo.into_fisrt_room())
        assert_true(DUT.Demo.click_login_button(), "点击登录按钮")
        assert_true(DUT.Login.password_login("11100000743", "Pass_7772"), "密码登录")


    def teardown(self):
        pass
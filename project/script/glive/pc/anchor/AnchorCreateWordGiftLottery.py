# -*- coding: UTF-8 -*-

"""
File Name:      AnchorCreateWordGiftLottery
Author:         zhangwei04
Create Date:    2019/8/6
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class AnchorCreateWordGiftLottery(TestsuiteNormal):
    def setup(self):
        self.desc = "主播页-我的抽奖-创建口令道具抽奖"

    def test(self):
        g_logger.info(self.desc)
        DUT.Home.into_home()
        assert_true(DUT.Login.password_login(account_section='anchor1'), desc="主播账户密码登录", target=DUT)
        assert_true(DUT.Home.into_anchor(), desc="进入主播页", target=DUT)
        assert_true(DUT.AnchorPage.click_tab("我的抽奖"), desc="点击我的抽奖Tab", target=DUT)
        assert_true(DUT.AnchorPage.check_my_lottery_ui(), desc="检测我的抽奖Tab UI", target=DUT)
        data = self.data
        assert_true(DUT.AnchorPage.create_word_gift_lottery(data.word, data.name, number=data.number, l_range=data.l_range, continue_time=data.continue_time),
                desc="创建口令道具抽奖", target=DUT)
        assert_true(DUT.AnchorPage.check_lottery_status(), desc="检测进行中抽奖状态", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
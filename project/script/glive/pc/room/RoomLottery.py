# -*- coding: UTF-8 -*-

"""
File Name:      RoomLottery
Author:         zhangwei04
Create Date:    2019/8/7
"""

from project.script.testsuite.TestsuiteNormal import *
import os


class RoomLottery(TestsuiteNormal):
    def setup(self):
        self.desc = "直播间-参与抽奖-中奖"

    def test(self):
        g_logger.info(self.desc)
        anchor = "anchor1"
        data = self.data

        g_logger.info("用户取消关注")
        DUT.LiveRoom.url_into_room(DUT.LiveRoom.account_conf.get(anchor, "room"))
        assert_true(DUT.Login.password_login(account_section="user1", check_chat_ready=True), desc="用户账户密码登录", target=DUT)
        already_drawn_lottery = DUT.LiveRoom.is_drawn_lottery()  # 检测是否已经在抽奖
        if not already_drawn_lottery:
            assert_true(DUT.LiveRoom.unfollow(), desc="用户取消关注主播", target=DUT)

        # 检测是否正在抽奖，若不在抽奖，则主播创建抽奖
        if not already_drawn_lottery:
            g_logger.info("主播创建抽奖")
            DUTP.Home.into_home()
            assert_true(DUTP.Login.password_login(account_section=anchor), desc="主播账户密码登录", target=DUTP)
            assert_true(DUTP.Home.into_anchor(), desc="进入主播页", target=DUTP)
            assert_true(DUTP.AnchorPage.click_tab("我的抽奖"), desc="点击我的抽奖Tab", target=DUTP)
            assert_true(DUTP.AnchorPage.check_my_lottery_ui(), desc="检测我的抽奖Tab UI", target=DUTP)
            assert_true(DUTP.AnchorPage.create_word_gift_lottery(data.word, data.name, number=data.number, l_range=data.l_range, continue_time=data.continue_time),
                        desc="创建口令抽奖", target=DUTP)
            DUT.LiveRoom.refresh()

        g_logger.info("用户参与抽奖")
        if already_drawn_lottery and DUT.LiveRoom.check_follow():   # 用户已关注并且已经抽奖，关注任务自动完成
            pass
        else:
            assert_true(DUT.LiveRoom.do_follow_task(), desc="用户做关注任务", target=DUT)
        assert_true(DUT.LiveRoom.do_copy_word_task(data.word), desc="用户做口令任务", target=DUT)
        time.sleep(2)
        assert_true(DUT.LiveRoom.check_all_task_done(), desc="检测所有的任务都完成", target=DUT)
        assert_true(DUT.LiveRoom.wait_for_lottery_end(), desc="等待抽检时间结束", target=DUT)

        g_logger.info("检测中奖弹窗")
        assert_true(DUT.LiveRoom.check_lottery_win_ui(), desc="检测中奖弹窗信息", target=DUT)

    def teardown(self):
        DUT.Home.leave_one_window()
        DUTP.Home.leave_one_window()
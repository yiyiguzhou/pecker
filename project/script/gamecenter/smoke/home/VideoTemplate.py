# -*- coding: UTF-8 -*-

"""
File Name:      VideoTemplate
Author:         gufangmei_sx
Create Date:    2018/8/13
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class VideoTemplate(TestsuiteNormal):
    """
    用例描述：首页-视频模板运营位
    预置条件：首页第一个视频模板运营位正确配置了关联视频，视频时长超过30秒
    """
    def setup(self):
        self.desc = "首页-视频模板运营位"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("首页第一个视频模板运营位正确配置了关联视频，视频时长超过30秒")
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.HomePage.click_first_video_template(self.data.game_name), "点击第一个视频模板运营位的播放按钮", target=DUT)
        assert_true(DUT.HomePage.check_video(self.data.game_name), "视频播放", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
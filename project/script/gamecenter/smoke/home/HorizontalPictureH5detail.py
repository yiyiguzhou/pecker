# -*- coding: UTF-8 -*-

"""
File Name:      HorizontalPictureH5detail
Author:         gufangmei_sx
Create Date:    2018/7/10
"""
import time
from project.script.testsuite.TestsuiteNormal import *


class HorizontalPictureH5detail(TestsuiteNormal):
    """
    预置条件：1. 奇玩1.0后台运营位：1369配置了横排图片推荐位一的标题；运营位：1345横排图片推荐位一配置了5个图片，其中的第二张图片配置了H5活动页
    """
    def setup(self):
        self.desc = "首页-横排图片模板运营位-进入H5活动页"
        DUT.device.start_log()
        DUT.Common.reset_app()

    def test(self):
        g_logger.info(self.desc)
        g_logger.info("横排名：{}".format(self.data.title))
        assert_true(DUT.Common.into_game_center(self.data.newgame, self.data.poker), "进入游戏中心", target=DUT)
        assert_true(DUT.Common.check_title(self.data.title, timeout=240), "横排图片H5活动页 ", target=DUT)
        assert_true(DUT.HomePage.click_horizontal_pic_first(self.data.title), "H5活动详情页", target=DUT)
        assert_true(DUT.Common.check_h5_web_side(), "通过WebView检查是否进入H5页面 ", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
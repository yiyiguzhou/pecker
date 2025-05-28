# -*- coding: UTF-8 -*-

"""
File Name:      rankpage
Author:         zhangwei04
Create Date:    2018/12/11
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common
from appium.webdriver.common.touch_action import TouchAction


class RankPage(Common):
    """榜单页面"""

    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self):
        """检测榜单页UI"""
        if not self.device.check_textview_text("排行榜"):
            return False
        if not self.device.check_textview_text("精品榜"):
            return False
        if not self.device.check_textview_text("飙升榜"):
            return False
        if not self.device.check_textview_text("新游榜"):
            return False
        return True

    def check_tab_top_game(self, games):
        """检测标签页顶部游戏， 不大于三款,处于第一页"""
        if isinstance(games, str):
            games = [games]
        if len(games) > 3:
            g_logger.error("最多支持3款游戏检测，实际配置{}款".format(len(games)))
            return False

        g_logger.info("查找游戏: {}".format(", ".join(games)))
        for game_name in games:
            try:
                self.device.find_element_by_xpath(self.conf.rank.xpath_game.format(game_name), timeout=5)
            except:
                g_logger.error("游戏'{}'未找到".format(game_name))
                return False
        return True

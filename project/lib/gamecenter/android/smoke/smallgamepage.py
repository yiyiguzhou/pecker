# -*- coding: UTF-8 -*-

"""
File Name:      SmallGamePage
Author:         zhangwei04
Create Date:    2018/12/11
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common
from appium.webdriver.common.touch_action import TouchAction


class SmallGamePage(Common):
    """小游戏中心页"""

    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.last_env = None

    def check_ui(self):
        """
        检测小游戏中心UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        title_xpath = self.conf.comment_title.xpath.format("爱奇艺小游戏")

        try:
            self.device.find_element_by_xpath(title_xpath, timeout=15)
        except:
            g_logger.error("查找小游戏中心标题失败")
            return False
        
        return True

    def click_game(self, game_name):
        """
        点击小游戏
        Args:
            game_name: 小游戏游戏名
        Returns:
            True: 点击成功, False: 点击失败
        """
        ele = self.device.swipe_down_find_ele("//android.view.View[@content-desc='{}']".format(game_name), timeout=60)
        if ele:
            ele.click()
            time.sleep(5)
            return True
        else:
            g_logger.error("查找游戏:{}失败".format(game_name))
            return False







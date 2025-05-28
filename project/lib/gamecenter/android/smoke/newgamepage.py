# -*- coding: UTF-8 -*-

"""
File Name:      h5page
Author:         zhangwei04
Create Date:    2018/11/19
"""

import os
import time
import re
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common


class NewGamePage(Common):
    """新游页面"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self, desc=""):
        """检测H5页面UI，目前根据WebView控件检测"""
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='新游' and @resource-id='com.qiyi.gamecenter:id/common_title_tv']", timeout=10)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='最新上线']", timeout=5)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='最新预约']", timeout=5)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='封测专区']", timeout=5)
            return True
        except:
            return False

    def check_up_to_date_tab_ui(self):
        """
        检测最新上线UI
        Returns:
            True: 检测成功, Fals: 检测失败
        """
        if not self.device.check_textview_text("新游推荐"):
            g_logger.error("未找到'新游推荐'文字")
            return False

        if not self.device.check_textview_text("今日新游", timeout=10):
            g_logger.error("查找'今日新游'超时")

        if not self.device.check_textview_text("本月新游", swipe=True, timeout=120):
            g_logger.error("查找'本月新游'超时")
            return False

        if not self.device.check_textview_text("季度新游", swipe=True, timeout=180):
            g_logger.error("查找'季度新游'超时")
            return False
        return True

    def check_is_into_game(self):
        """检查是否进入H5游戏，若有侧边栏，则代表进入了H5游戏"""
        try:
            self.device.find_element_by_id("sidebar", timeout=30)
            return True
        except:
            g_logger.error("未检测到侧边栏")
            return False

    def click_latest_book_tab(self):
        """
        点击最新预约Tab
        Returns:
            True: 点击成功， False: 点击失败
        """
        return self._click_title_tab("最新预约")

    def _click_title_tab(self, tab_name):
        """点击标题标签
        Args:
            tab_name: 标签名
        Returns:
            True: 点击成功， False: 点击失败
        """
        title_xpath = self.conf.gamecenter_newgame.xpath_title.format(tab_name)
        try:
            self.device.click_by_xpath(title_xpath, desc="点击标签：{}".format(tab_name), timeout=10)
            time.sleep(3)
            return True
        except:
            return False

    def _get_book_number(self, game_name):
        """
        获取游戏预定人数
        Args:
            game_name: 游戏名

        Returns:
            人数或者None
        """
        for i in range(2):
            try:
                ele = self.device.find_element_by_xpath(self.conf.new_game_latest_book.xpath_book_num.format(game_name), timeout=10)
                number = re.findall("\d+", ele.get_attribute("text"))
                if number:
                    return number[0]
                else:
                    return None
            except Exception as e:
                self.device.swipe_screen(rate=0.2)
                time.sleep(2)
        return None

    def check_book_tab_ui(self):
        """
        检测预约列表的UI，能够正常显示游戏和预约人数
        Returns:
            True: 检测成功, False: 检测失败
        """
        ret = True
        game_dict = {}
        while len(game_dict) < 3:
            eles = self.device.find_elements_by_xpath(self.conf.new_game_latest_book.xpath_games, timeout=10)
            if eles:
                for ele in eles:
                    game_name = ele.get_attribute("text")
                    if game_name not in game_dict:
                        game_num = self._get_book_number(game_name)
                        if game_num:
                            game_dict[game_name] = game_num
                        else:
                            g_logger.error("游戏名：{}获取预约数失败".format(game_name))
                            ret = False
                            break
            else:
                break
            if not ret:
                break
            self.device.swipe_screen(rate=0.3)

        for game in game_dict:
            g_logger.info("预约游戏名：{}，预约数：{}".format(game, game_dict[game]))
        return ret

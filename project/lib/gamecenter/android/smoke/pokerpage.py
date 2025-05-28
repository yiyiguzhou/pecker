# -*- coding: UTF-8 -*-

"""
File Name:      pokerpage
Author:         zhangwei04
Create Date:    2018/12/12
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common
from appium.webdriver.common.touch_action import TouchAction


class PokerPage(Common):
    """棋牌中心页"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self):
        """
        检测棋牌中心UI
        Returns:
            True: 检测成功，False: 检测失败
        """
        msg = "查找标题"
        try:
            self.device.find_element_by_xpath(self.conf.poker.xpath_title, timeout=10)
            msg = "查找视频模块"
            self.device.find_element_by_id(self.conf.poker.id_top_bg, timeout=5)
            return True
        except:
            g_logger.error("{}失败".format(msg))
            return False

    def check_hot_video_title(self):
        """
        检测热门视频模块
        Returns:
        True: 检测成功 False: 检测失败
        """
        return self.device.check_textview_text("热门视频", swipe=True, timeout=120)

    def check_top_recommend_dl(self):
        """
        检测顶部推荐模块游戏下载、安装、打开，检测后游戏卸载
        Returns:
            True: 检测成功, False: 检测失败
        """
        game_name = "顶部推荐游戏"
        if not self.top_recommend_dl(game_name):
            return False
        self.uninstall_game(game_name)
        return True

    def top_recommend_dl(self, game_name):
        try:
            self.device.click_by_id(self.conf.poker_top.id_dl_button, timeout=10)
            time.sleep(5)
        except:
            g_logger.error("点击顶部推荐模块游戏下载按钮失败")
            return False
        for i in range(2):
            if not self.game_install(game_name=game_name, open_game=True, click_last_installed=False):
                ele = self.cmd_back_and_find_ele(id=self.conf.poker_top.id_dl_button)
                if ele:
                    ele.click()
                    continue
                else:
                    break
            else:
                if self.device.get_manufacturer() == 'xiaomi':
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_done, timeout=10)
                        time.sleep(2)
                    except:
                        pass
                return True
        g_logger.info("安装游戏失败")
        return False

    def check_top_recommend_get_gift(self):
        """
        顶部模块点击每日礼包，跳转至游戏详情页福利页
        Returns:
            True: 跳转成功， False: 跳转失败
        """
        get_gitf_xpath = self.conf.poker_top.xpath_title.format("领每日礼包")
        try:
            self.device.click_by_xpath(get_gitf_xpath, timeout=10)
            time.sleep(8)
        except:
            g_logger.error("点击'领取每日礼包'失败")
            return False
        for i in range(2):
            self.device.swipe_screen(rate=0.6, direction='down')
        return self.target.GameDetailPage.check_welfare_ui(titles="激活码礼包")

    def check_top_recommend_start_privilege(self):
        """
        顶部模块点击启动特权，跳转至游戏详情页福利页
        Returns:
            True: 跳转成功， False: 跳转失败
        """
        get_gitf_xpath = self.conf.poker_top.xpath_title.format("启动特权")
        try:
            self.device.click_by_xpath(get_gitf_xpath, timeout=10)
            time.sleep(5)
        except:
            g_logger.error("点击'启动特权'失败")
            return False
        return self.target.GameDetailPage.check_welfare_ui(titles="启动特权")

    def check_top_recommend_bubble_circle(self):
        """
        顶部模块点击游戏社区，跳转至游戏详情页游戏圈
        Returns:
            True: 跳转成功， False: 跳转失败
        """
        get_gitf_xpath = self.conf.poker_top.xpath_title.format("游戏社区")
        try:
            self.device.click_by_xpath(get_gitf_xpath, timeout=10)
            time.sleep(5)
        except:
            g_logger.error("点击'游戏社区'失败")
            return False
        return self.target.GameDetailPage.check_bubble_circle_ui()

    def check_top_recommend_play_without_dl(self):
        """
        顶部模块点击免下载畅玩，跳转至H5游戏
        Returns:
            True: 跳转成功， False: 跳转失败
        """
        get_gitf_xpath = self.conf.poker_top.xpath_title.format("免下载畅玩")
        try:
            self.device.click_by_xpath(get_gitf_xpath, timeout=10)
            time.sleep(5)
        except:
            g_logger.error("点击'免下载畅玩'失败")
            return False
        return self.target.H5Page.check_game_ui()

    def huge_imge_into_topic(self, image_desc, topic_title, topic_desc=None):
        """
        从大图进入专题
        Args:
            image_desc: 大图描述
            topic_title: 专题标题
            topic_desc: 专题描述
        Returns:
            True: 进入成功, False: 进入失败
        """
        if not self.click_huge_image(image_desc):
            return False

        return self.check_topic_ui(topic_title, topic_desc)

    def huge_imge_into_activity(self, image_desc, activity_title):
        """
        从大图进入活动页
        Args:
            image_desc: 大图描述
            activity_title: 活动标题
        Returns:
            True: 进入成功, False: 进入失败
        """
        if not self.click_huge_image(image_desc):
            return False
        time.sleep(2)
        return self.target.H5Page.check_activity_ui(activity_title)

    def check_video_play(self, video_title, auto_play=True):
        """
        检测视频播放功能
        Args:
            video_title: 视频标题
            auto_play: 是否自动播放
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.click_video_template(video_title):
            return False
        if not auto_play:
            try:
                self.device.click_by_id(self.conf.detail_video_play.id, timeout=5)
                time.sleep(0.5)
            except:
                pass
        return self.check_video()

    def click_video_template(self, video_title):
        """
        点击视频模块视频部分
        Args:
            video_title: 视频标题
        Returns:
            True: 点击成功，False:点击失败
        """
        self.conf.poker_video_template.xpath_title.format(video_title)
        self.conf.poker_video_template.xpath_video.format(video_title)
        self.conf.poker_video_template.xpath_desc.format(video_title)
        self.conf.poker_video_template.xpath_find_more.format(video_title)
        if not self._video_template_full_screen(video_title):
            return False
        try:
            self.device.click_by_xpath(self.conf.poker_video_template.xpath_video.format(video_title), timeout=10)
            time.sleep(0.5)
        except Exception as e:
            pass    # 播放后id会改变

        return True

    # def check_video_templat_find_more(self, video_title):
    #     if not self.click_video_template_find_more(video_title):
    #         return False

    def click_video_template_find_more(self, video_title):
        """
        点击视频模块'查看全部节目'
        Args:
            video_title: 视频标题
        Returns:
            True: 执行点击操作了， False: 未找到此模块的查看全部节目
        """
        if not self._video_template_full_screen(video_title):
            return False
        for i in range(3):
            try:
                self.device.click_by_xpath(self.conf.poker_video_template.xpath_find_more.format(video_title), desc='点击查看全部节目', timeout=10)
                time.sleep(2)
                return True
            except:
                self.device.swipe_screen(rate=0.1)
        return False

    def _video_template_full_screen(self, video_title):
        """
        棋牌视频滑动之全屏显示出来
        Args:
            video_title: 视频标题
        Returns:
            True: 滑动之全屏成功，False:全屏显示失败
        """
        if not self.device.swipe_down_find_ele(xpath=self.conf.poker_video_template.xpath_title.format(video_title)):
            g_logger.error("检测视频模块顶部标题失败")
            return False
        if not self.device.swipe_down_find_ele(xpath=self.conf.poker_video_template.xpath_find_more.format(video_title), rate=0.1):  # 带有查看全部界面底部的
            g_logger.error("检测视频模块底部描述失败")
            return False
        return True









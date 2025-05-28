# -*- coding: UTF-8 -*-

"""
File Name:      h5page
Author:         zhangwei04
Create Date:    2018/11/19
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common


class H5Page(Common):
    """H5页面"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self, view_desc=None, webview_desc=None):
        """检测H5页面UI，目前根据WebView控件检测
        Args:
            view_desc: view类描述
            webview_desc: Webview类描述
            """
        try:
            self.device.find_element_by_id("com.qiyi.gamecenter:id/h5_web_view", timeout=10)
        except:
            return False

        if webview_desc:
            try:
                self.device.find_element_by_xpath("//android.webkit.WebView[@content-desc='{}']".format(webview_desc), timeout=20)
            except:
                g_logger.warning("H5检测UI查找描述：{}失败".format(webview_desc))
                return False
        if view_desc:
            try:
                self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(view_desc), timeout=20)
            except:
                g_logger.warning("H5检测UI查找描述：{}失败".format(view_desc))
                return False

        return True

    def check_game_ui(self):
        """检测H5游戏页面UI，目前根据WebView控件检测"""
        try:
            self.device.click_by_xpath(self.conf.common_button.xpath_add, timeout=5)
            time.sleep(2)
        except:
            pass
        try:
            self.device.find_element_by_id("com.qiyi.gamecenter:id/h5_game_view", timeout=10)
            self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "h5_game.png"))
            return True
        except:
            g_logger.error("未检测到游戏webview")
            return False

    def check_activity_ui(self, title):
        """
        检测活动页UI
        Returns:

        """
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}' and @resource-id='com.qiyi.gamecenter:id/common_title_tv']".format(title), timeout=10)
        except:
            g_logger.error("查找h5页面标题：{}失败".format(title))
            return False
        return self.check_ui()

    def check_is_into_game(self):
        """检查是否进入H5游戏，若有侧边栏，则代表进入了H5游戏"""
        try:
            self.device.find_element_by_id("sidebar", timeout=30)
            return True
        except:
            g_logger.error("未检测到侧边栏")
            return False

    def check_topic_from_poker_video(self, topic_title):
        """
        检测由棋牌中心视频查看更多跳转的专题页面
        Args:
            topic_title: 专题标题
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.device.check_textview_text(topic_title, timeout=10)

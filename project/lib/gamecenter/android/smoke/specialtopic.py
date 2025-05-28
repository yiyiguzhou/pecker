# -*- coding: UTF-8 -*-

"""
File Name:      activitypage
Author:         zhangwei04
Create Date:    2018/11/19
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common


class SpecialTopic(Common):
    """专题页类"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self, title=None, game_name=None):
        """
        检测UI是否显示正确，检测内容，标题，游戏名称
        Args:
            title: 标题名称
            game_name: 游戏名称
        Returns:
        """
        if title:
            ret = self.check_title(title)
            if not ret:
                return False
        if game_name:
            return self.check_game(game_name)
        return True

    def check_title(self, title):
        """
        查找标题
        Args:
            title: 活动页标题
        Returns:
            True: 标题检测成功，False: 标题检测失败
        """
        return self.device.check_textview_text(title, swipe=False, timeout=10)

    def check_game(self, game_name, timeout=30):
        """
        查找游戏是否存在
        Args:
            game_name: 活动页标题
            timeout: 查找超时时间
        Returns:
            True: 标题检测成功，False: 标题检测失败
        """
        return self.device.check_textview_text(game_name, swipe=True, timeout=timeout)

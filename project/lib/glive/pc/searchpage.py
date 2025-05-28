# -*- coding: UTF-8 -*-

"""
File Name:      searchpage
Author:         zhangwei04
Create Date:    2019/7/23
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from framework.utils.selenium.action_chains import ActionChains


class SearchPage(Common):
    """直播间"""
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self, part_text):
        """
        检测搜索页UI
        Args:
            part_text: 搜索文本
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            ele = self.device.find_element_by_xpath(self.conf.home_subtitle.title_xpath)
            if ele.text != "相关直播":
                return g_logger.error("检测搜索页标题失败")
        except:
            return g_logger.error("查找搜索页标题失败")

        try:
            ul_ele = self.device.find_element_by_id("search-list")
            search_list = []
            for ele in ul_ele.find_elements_by_tag_name("li"):
                item_dict = self.format_room_item_msg(ele)
                search_list.append(item_dict)
                g_logger.info(item_dict)
        except Exception as e:
            return g_logger.warning("搜索页没有搜索记录")
        return True


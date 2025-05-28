# -*- coding: UTF-8 -*-

"""
File Name:      rankpage
Author:         zhangwei04
Create Date:    2019/7/25
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from framework.utils.selenium.action_chains import ActionChains


class RankPage(Common):
    """直播排行榜单页"""
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_rank_ui(self):
        """
        检测榜单页UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            eles = self.device.find_elements_by_xpath(self.conf.rank.classify)
            for ele in eles:
                self.device.check_ele_text_by_ele(ele, timeout=3, desc="榜单标签页")
        except:
            return g_logger.error("查找分类标签元素失败")

        if not self.device.check_ele_text_by_xpath(self.conf.rank.week_title, text='本周角逐榜', desc="本周榜单标题"):
            return False

        if not self.device.check_ele_text_by_xpath(self.conf.rank.last_week_title, text='上周王者榜', desc="上周榜单标题"):
            return False

        return True

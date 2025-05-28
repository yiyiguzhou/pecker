# -*- coding: UTF-8 -*-

"""
File Name:      anchorpage
Author:         zhangwei04
Create Date:    2019/7/25
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from framework.utils.selenium.action_chains import ActionChains


class AnchorPage(Common):
    """直播排行榜单页"""
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def click_tab(self, tab="主播等级"):
        """
        点击tab，进入tab页
        Args:
            tab: tab名
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.anchor.tab.format(tab))

    def check_my_lottery_ui(self, ):
        """
        检测我的抽奖页面UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.device.check_ele_text_by_xpath(self.conf.anchor.active_tab, text="我的抽奖", desc='当前活动标签'):
            return False
        return True

    def create_word_gift_lottery(self, word, name, number=1, l_range=1, continue_time=5):
        """
        创建口令道具抽奖
        Args:
            word: 抽奖口令
            name: 道具名，需要已存在的道具
            number: 抽奖数量
            l_range: 抽奖范围，1：关注我的用户， 2：我的粉丝徽章用户
            continue_time: 抽奖时间，单位分钟
        Returns:
            True: 创建成功, False: 创建失败
        """
        if self.check_lottery_status():
            return g_logger.info("已经有抽奖")
        conf = self.conf.anchor_lottery_word_gift
        try:
            number = int(number)
            l_range = int(l_range)
            continue_time = int(continue_time)
        except:
            return g_logger.error("参数转化整型失败")

        if not self.device.click_by_partial_link_text("创建抽奖", desc="创建抽奖按钮"):
            return False

        if not self.device.click_by_xpath(conf.gift_div):
            return g_logger.error("点击口令抽奖奖品按钮失败")
        gift_div_ele = self.device.get_ele_by_xpath(conf.gift_div)
        if not gift_div_ele:
            return g_logger.error("点击口令抽奖奖品按钮失败")
        try:
            gift_div_ele.find_element_by_xpath(conf.gift_li_name_f.format(name)).click()
        except:
            return g_logger.error("查找礼物:{}失败".format(name))
        # 获取礼物数量
        try:
            gift_div_number_ele = self.device.find_element_by_xpath(conf.gift_number)
            have_gift_num = int(gift_div_number_ele.text[1:-1])
            if have_gift_num < number:
                return g_logger.error("口令抽奖实际礼物数量[{}]小于抽奖数量[{}]".format(have_gift_num, number))
        except:
            return g_logger.error("查找口令抽奖奖品数量失败")

        gift_element = self.device.get_ele_by_xpath(conf.number_input)
        if not gift_element:
            return g_logger.error("查找奖品数量输入框失败")
        else:
            gift_element.send_keys(number)

        if not self.device.click_by_xpath(conf.range_div):
            return g_logger.error("点击抽奖范围按钮失败")
        try:
            ele = self.device.find_element_by_xpath(conf.range_div)
            ele.find_element_by_xpath(conf.range_li_f.format(l_range)).click()
            time.sleep(1)
        except Exception as e:
            return g_logger.error("查找点击抽奖范围按钮失败")

        if not self.device.click_by_xpath(conf.time_div):
            return g_logger.error("点击抽奖范围按钮失败")
        try:
            ele = self.device.find_element_by_xpath(conf.time_div)
            ele.find_element_by_xpath(conf.time_li_f.format(continue_time)).click()
            time.sleep(1)
        except Exception as e:
            return g_logger.error("查找点击抽奖时间按钮失败")
        try:
            self.device.find_element_by_xpath(conf.world_input).send_keys(word)
        except:
            return g_logger.error("输入抽奖口令失败")

        return self.device.click_by_xpath(conf.submit, desc='提交按钮')

    def check_lottery_status(self):
        """
        检测抽奖状态
        Returns:
            True: 有进行中的抽奖， False: 未找到进行中的抽奖
        """
        ele = self.device.get_ele_by_xpath(self.conf.anchor_lottery_status.tr)
        if not ele:
            return g_logger.error("查找进行中的抽奖元素失败")
        th = ("时间", "抽奖类型", "奖品类型", "奖品名称", "奖品数量", "参与人数", "抽奖状态", "中奖名单")
        for t, e in zip(th, ele.find_elements_by_xpath("./td")):
            g_logger.info("{}:{}".format(t, e.text))
        return True



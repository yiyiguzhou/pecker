# -*- coding: UTF-8 -*-

"""
File Name:      userpage
Author:         zhangwei04
Create Date:    2019/7/25
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from framework.utils.selenium.action_chains import ActionChains


class UserPage(Common):
    """直播排行榜单页"""
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_info_ui(self, account_section=None):
        """
        检测个人信息页面UI
        Args:
            user_name: 用户名
        Returns:
            True: 检测成功, False: 检测失败
        """
        if account_section:
            if self.account_conf.check_available(account_section):
                user_name = self.account_conf.get(account_section, "base_name")
            if not self.device.check_ele_text_by_xpath(self.conf.user_info.name, text=user_name, desc='用户名'):
                return False
        if not self.device.check_ele_by_xpath(self.conf.user_info.account_set):
            return False
        if not self.device.check_ele_text_by_xpath(self.conf.user_info.uid, desc='用户UID'):
            return False
        if not self.device.check_ele_text_by_xpath(self.conf.user_info.beans, desc='用户奇豆'):
            return False
        if not self.device.check_ele_text_by_xpath(self.conf.user_info.gold, desc='用户金币'):
            return False
        return True

    def check_follow_ui(self):
        """
        点击我的关注Tab
        Returns:
            True: 点击成功, False: 点击失败
        """
        g_logger.info("检测高亮元素是否是我的关注")
        if not self.device.check_ele_text_by_xpath(self.conf.user.active_tab, text='我的关注'):
            return g_logger.error("检测失败")

        for li_ele in self.device.find_elements_by_xpath(self.conf.user_follow.room_li, timeout=5):
            g_logger.info(self.format_room_item_msg(li_ele))
        return True

    def check_history_ui(self):
        """
        点击我的关注Tab
        Returns:
            True: 点击成功, False: 点击失败
        """
        g_logger.info("检测高亮元素是否是观看历史")
        if not self.device.check_ele_text_by_xpath(self.conf.user.active_tab, text='观看历史'):
            return g_logger.error("检测失败")
        for li_ele in self.device.find_elements_by_xpath(self.conf.user_follow.room_li, timeout=5):
            g_logger.info(self.format_room_item_msg(li_ele))
        return True

    def click_package_special_tab(self):
        """
        点击背包特殊道具Tab
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.user_package.tab_format.format("特殊道具"), desc="特殊道具Tab")

    def check_package_gift_ui(self):
        """
        检测背包-礼物道具UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.device.check_ele_text_by_xpath(self.conf.user_package.gift_tab_active, text="礼物道具"):
            return False

        eles = self.device.find_elements_by_xpath(self.conf.user_package.gift_li)
        if eles:
            for li_ele in eles:
                g_logger.info(self.format_gift_msg(li_ele))
            return True
        else:
            g_logger.info("无礼物，检测空态图")
            try:
                ele = self.device.find_element_by_id("card-empty")
                return ele.is_displayed()
            except:
                return False

    def check_package_special_gift_ui(self):
        """
        检测背包-特殊道具UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.device.check_ele_text_by_xpath(self.conf.user_package.gift_tab_active, text="特殊道具"):
            return False

        eles = self.device.find_elements_by_xpath(self.conf.user_package.gift_li)
        if eles:
            for li_ele in eles:
                g_logger.info(self.format_gift_msg(li_ele))
            return True
        else:
            g_logger.info("无礼物，检测空态图")
            try:
                ele = self.device.find_element_by_id("card-empty")
                return ele.is_displayed()
            except:
                return False

    def format_gift_msg(self, li_ele):
        """
        格式化礼物道具信息
        Args:
            li_ele: 礼物道具li对象
        Returns:
            dict: 礼物名[name]，贡献值[contribute]、经验值[experience]、亲密度[affinity]、有效期[validity]
        """
        item = {}
        try:
            item['name'] = li_ele.find_element_by_xpath(self.conf.user_package_gift.name).text
            item['contribute'] = li_ele.find_element_by_xpath(self.conf.user_package_gift.contribute).text
            item['experience'] = li_ele.find_element_by_xpath(self.conf.user_package_gift.experience).text
            item['affinity'] = li_ele.find_element_by_xpath(self.conf.user_package_gift.affinity).text
            item['validity'] = li_ele.find_element_by_xpath(self.conf.user_package_gift.validity).text
        except Exception as e:
            g_logger.warning("获取礼物item部分信息失败，请确认是否正常!")
        return item

    def click_tab(self, tab_name):
        """
        点击Tab
        Args:
            tab_name: tab名
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.user.tab.format(tab_name), desc=tab_name, timeout=5)

    def into_live_room(self, room_index=None, room_title=None, author=None, number=None, timeout=10):
        """
        进入直播间
        Args:
            room_index: 直播间位置标号，即在列表页的索引，从1开始
            room_title: 直播间标题
            author: 主播名
            number: 直播间号
            timeout: 超时
        Returns:
            True: 点击直播成功， False: 点击直播间失败
        """
        if not room_index and not room_title and not author and not number:
            g_logger.warning("参数：room_index, room_title，author, number 参数必须传一个")
            return False

        if room_index:
            # 通过索引值进入直播间
            find_xpath = self.conf.live_list_room.index_xpath.format(room_index)
        elif room_title:
            find_xpath = self.conf.live_list_room.title_xpath.format(room_title)
        elif author:
            # find_xpath = self.conf.live_list_room.anchor_xpath.format(author)
            try:
                ele = self.device.find_element_by_partial_link_text(author)
                ele.click()
                time.sleep(2)
                return True
            except:
                return g_logger.error("查找直播间信息元素失败")
        else:
            find_xpath = self.conf.live_list_room.number_xpath.format(number)
        time_start = time.time()
        while time.time() - time_start < timeout:
            try:
                el = self.device.find_element_by_xpath(find_xpath, timeout=2)
                el.click()
                time.sleep(2)
                return True
            except:
                try:
                    self.device.click_by_xpath("//div[@class='_ok lottery-close']", time_sleep=0.5, timeout=1)
                except:
                    pass
        else:
            return g_logger.error("查找直播间信息元素失败")

# -*- coding: UTF-8 -*-

"""
File Name:      livelistpage
Author:         zhangwei04
Create Date:    2019/7/23
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from framework.utils.selenium.action_chains import ActionChains


class LiveListPage(Common):
    """直播列表页"""
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self, title, active=None, tabs=[], focus_check=False):
        """
        检测直播列表页UI
        Args:
            title: 标题
            tabs:  子标题列表，如['全部', '王者荣耀']
            focus_check: 焦点图检测
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            title_ele = self.device.find_element_by_xpath(self.conf.live_list.title_xpath)
            if title_ele.text != title:
                g_logger.error("标题检测失败，期望值[{}], 实际值[{}]".format(title, title_ele.text))
                return False
        except:
            g_logger.error("查找标题：{}失败".format(title))
            return False

        if active:
            try:
                active_ele = self.device.find_element_by_xpath(self.conf.live_list.subtitle_active_xpath, timeout=5)
                if active_ele.text != active:
                    g_logger.error("查找当前标签失败，期望值[{}], 实际值[{}]".format(active, active_ele.text))
                    return False
            except:
                g_logger.error("未找active标签元素")
                return False

        if tabs:
            if isinstance(tabs, str):
                tabs = [tabs]

            page_tabs = [ele.find_element_by_tag_name("a").text for ele in self.device.find_elements_by_xpath(self.conf.live_list.subtitles_li_xpath)]
            for tab in tabs:
                if tab not in page_tabs:
                    g_logger.error("子标题匹配失败，期望值{}, 实际值{}".format(tabs, page_tabs))
                    return False
            else:
                g_logger.error("子标题匹配成功，期望值{}, 实际值{}".format(tabs, page_tabs))

        if focus_check:
            try:
                self.device.find_element_by_xpath(self.conf.live_list_focus.xpath)
                return True
            except:
                g_logger.error("检测游戏列表焦点图失败")
                return False
        return True

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








# -*- coding: UTF-8 -*-

"""
File Name:      common
Author:         zhangwei04
Create Date:    2019/7/19
"""
from project.lib.pc import PC
import os
import time
from selenium.webdriver.common.by import By
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread


class Common(PC):
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.conf_img_dir = os.path.join(g_resource['project_path'], 'conf', 'img', 'glive', 'pc')
        self._thread_tips = None
        self._thread_close_tips_flag= False

    def ansy_catch_tips(self):
        """异步方式抓取弹窗，并点击掉"""
        self._thread_tips = IpeckerThread()
        self._thread_close_tips_flag = True     # tips捕获进程标志
        self._thread_tips.start(self._ansy_click_tip)

    def stop_catch_tips(self):
        if self._thread_tips:
            self._thread_close_tips_flag = False

    def _ansy_click_tip(self):
        first_recharge = False  # 6折优惠弹窗
        while self._thread_close_tips_flag:
            if not first_recharge:
                try:
                    ele = self.device.find_element_by_id(self.conf.first_recharge.id, timeout=2)
                    if ele.is_displayed():
                        ele.find_element_by_xpath(self.conf.first_recharge.close, timeout=2).click()
                        time.sleep(0.2)
                        first_recharge = True
                        continue
                except:
                    pass
            time.sleep(0.5)

    @classmethod
    def format_room_item_msg(cls, li_ele):
        """
        格式化房间item信息(ps： 此接口耗时约0.15s)
        Args:
            li_ele: 房间item列表元素
        Returns:
            dict: 房间信息字典，包含房间号[room]、直播标题[title]、主播名[anchor]、所属标签(即二级分类)[label]、直播状态['status']、直播人气['hot']
        """
        item = {}
        try:
            item['room'] = li_ele.get_attribute('data-room')
            if item['room'] is None:
                item['room'] = li_ele.get_attribute('data-id')
            item['title'] = li_ele.find_element_by_class_name("t").text
            item['anchor'] = li_ele.find_element_by_class_name("author").text
            item['label'] = li_ele.find_element_by_class_name("label").text
            item['status'] = li_ele.find_element_by_xpath(".//span[contains(@class,'st')]").text
            item['hot'] = li_ele.find_element_by_xpath(".//span[@class='vv']").text
        except Exception as e:
            g_logger.warning("获取房间item部分信息失败，请确认是否正常!")
        return item

    @classmethod
    def format_room_cross_msg(cls, li_ele):
        """
        格式化侧边栏弹出直播间item信息
        Args:
            li_ele: 直播间li元素
        Returns:
            dict: 格式化的字典信息，直播间标题[title], 直播间链接[href], 主播名[author], 直播状态[status]，
        """
        item = {}
        try:
            a_ele = li_ele.find_element_by_tag_name('a')
            item['title'] = a_ele.get_attribute("title")
            item['href'] = a_ele.get_attribute("href")
            item['anchor'] = a_ele.find_element_by_xpath("./p[@class='author']").text
            item['status'] = a_ele.find_element_by_xpath(".//span[contains(@class,'st')]").text
        except Exception as e:
            g_logger.warning("获取弹窗列表直播间部分信息失败，请确认是否正常!")
        return item

    def close_recommend_tips(self, timeout=2):
        """
        点掉主播推荐弹窗
        Returns:
            True
        """
        g_logger.info("检测直播推荐弹窗，若有，则关闭")
        # time.sleep(1)   # 等待1秒，确保弹窗能够弹出来
        try:
            self.device.find_element_by_id("recommend_anchor_modal", timeout=timeout).find_element_by_xpath("//span[@class='content-skip']").click()
            time.sleep(1)
        except Exception as e:
            return False

        return True

    def close_lottery_tips(self):
        """
        关闭主播互动弹窗
        Returns:
            True
        """
        try:    # 检测首页弹窗
            self.device.find_element_by_xpath("//div[@class='_ok lottery-close']", timeout=2).click()
            time.sleep(0.5)
        except:
            pass
        return True

    def is_room(self):
        return "gamelive.iqiyi.com/w/" in self.device.current_url

    def leave_one_window(self):
        """
        关闭其他窗口，只保留最开始的窗口
        Returns:
            True: 关闭成功, False: 关闭失败
        """
        g_logger.info("关闭其他窗口")
        self.device.leave_one_window()

    def refresh(self):
        """
        刷新页面
        Returns:
        """
        g_logger.info("刷新页面")
        self.device.refresh()





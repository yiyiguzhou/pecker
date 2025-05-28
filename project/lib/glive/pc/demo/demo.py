# -*- coding: UTF-8 -*-

"""
File Name:      demo
Author:         zhangwei04
Create Date:    2019/7/12
"""


import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread
from framework.exception.exception import TimeoutException

from project.lib.pc import PC


class Demo(PC):
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

        self.target = target
        self.data = target.data
        self.device = target.device

    def into_home(self):
        self.device.get(self.conf.url.glive_home)
        try:    # 检测首页弹窗
            self.device.find_element_by_xpath("//div[@class='_ok lottery-close']").click()
            time.sleep(0.5)
        except:
            pass
        return True

    def click_login_button(self):
        try:
            self.device.find_element_by_xpath("//div[@class='login']/a[@data-user='login-btn']").click()
            time.sleep(1)
            return True
        except Exception as e:
            g_logger.error(str(e))
            return False

    def click_classify(self, tab_name='全部'):
        """
        点击直播间主页分类Tab
        Args:
            tag_name: 分类标签名
        Returns:
            True：点击成功, False: 点击失败
        """
        try:
            ele = self.device.find_element_by_link_text(tab_name)
            g_logger.info("url: {}".format(ele.get_attribute("href")))
            ele.click()
            time.sleep(1)
        except:
            return False
        return True

    def check_classify_active(self, tab_name='全部'):
        """
        检测是否是当前分类页
        Args:
            tab_name:
        """
        try:
            # ele = self.device.find_element_by_link_text(tab_name)
            ele = self.device.find_element_by_xpath(self.conf.home_classify.xpath_active)
            text = ele.get_attribute("text")
            return text == tab_name
        except Exception as e:
            return False

    def into_fisrt_room(self):
        try:
            self.device.switch_to_last_window()
            self.device.find_element_by_id("room").find_element_by_xpath("//li[@class='item']").click()
            time.sleep(1)
            self.device.switch_to_last_window()
            title = self.device.find_element_by_xpath("//div[@class='main-left']//div[@class='info-title']")
            g_logger.info(title.get_attribute("title"))
            g_logger.info("cookies: {}".format(self.device.get_cookies()))
            g_logger.info("title: {}".format(self.device.title))
            return True
        except Exception as e:
            return False


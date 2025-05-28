"""
File Name:      sidebar_display
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.sdk.android.mainland.mainland import Mainland



class  Sidebar(Mainland):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')
        self.target = target
        self.data = target.data
        self.device = target.device

    def Drag_sidebar(self):
        """
        进入游戏-拖动侧边栏
        Returns:
            True: 显示正常
            False：显示失败
        """
        time.sleep(5)
        try:
            self.device.adb.adb_shell("input swipe 120 159 144 540")
            time.sleep(3)
            self.device.tap([(144, 540)], duration=1, timeout=5)
            time.sleep(2)
            self.device.click_by_xpath("//android.widget.RadioButton[@text='活动']",timeout=3,desc="点击活动图标")
            time.sleep(2)
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.adb.adb_shell("input swipe 144 540 120 159")
            time.sleep(3)
        except Exception as e:
            return False
        return True

    def Sidebar_display(self):
        """
        进入游戏-侧边栏-显示正常
        Returns:
            True: 显示正常
            False：显示失败
        """
        time.sleep(5)
        try:
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(3)
            self.device.find_element_by_xpath("//android.widget.RadioButton[@text='活动']", timeout=4)
            time.sleep(2)
        except Exception as e:
            return False
        return True

    def Sidebar_display_pop_ups(self):
        """
        进入游戏-侧边栏-各个功能点入口
        Returns:
            True: 弹窗正常显示
            False：进入失败
        """
        time.sleep(5)
        try:
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(5)
            g_logger.info('11')
            self.device.click_by_xpath("//android.widget.RadioButton[@text='福利']",timeout=5,desc="点击福利按钮")
            g_logger.info('2')
            time.sleep(2)
            self.device.find_element_by_id('com.iqiyigame.sdk:id/tv_slide_com_top_bar_right').click()
            g_logger.info('3')
            self.device.find_element_by_id('com.iqiyigame.sdk:id/tv_sidebar_empty_content').click()
            g_logger.info('4')
            g_logger.info('福利界面显示正确')
        except:
            return False
        return True

    def sidebar_message_box(self):
        """
        进入游戏-侧边栏-消息盒
        Returns:
            True:  进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_xpath("//android.widget.RadioButton[@text='消息']",timeout=3).click()
            self.device.find_element_by_xpath("//android.widget.TextView[@text='消息盒']",timeout=3)
            g_logger.info('消息盒显示正确')
        except:
            return False
        return True

    def sidebar_privilege(self):
        """
        进入游戏-侧边栏-特权
        Returns:
            True:  进入成功
            False：进入失败
        """
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.tap([(120, 159)], duration=1, timeout=5)
            g_logger.info('5')
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.RadioButton[@text='特权']",timeout=3).click()
            g_logger.info('6')
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='领取方法']")
            time.sleep(2)
            g_logger.info('特权页面显示正确')
        except:
            return False
        return True
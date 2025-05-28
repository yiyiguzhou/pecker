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


class  Mainland(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device


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
            time.sleep(5)
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
        try:
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(5)
            self.device.find_element_by_xpath("//android.widget.RadioButton[@text='福利']").click()
            self.device.find_element_by_id('com.iqiyigame.sdk:id/tv_slide_com_top_bar_right').click()
            self.device.find_element_by_id('com.iqiyigame.sdk:id/tv_sidebar_empty_content').click()
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


            self.device.find_element_by_xpath("//android.widget.RadioButton[@text='消息']").click()
            self.device.find_element_by_xpath("//android.widget.TextView[@text='消息盒']")
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
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(5)
            self.device.find_element_by_xpath("//android.widget.RadioButton[@text='特权']").click()
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='领取方法']")
            time.sleep(2)
            g_logger.info('特权页面显示正确')
        except:
            return False
        return True
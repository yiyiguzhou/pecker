"""
File Name:      account_password_login_page
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.sdk.android.mainland.mainland import Mainland



class  Login(Mainland):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def test(self):
        """
        daluDemo测试接口
        """
        # self.device.test()
        g_logger.info("Demoapk test")

    def Other_login_retrieve_password_mobile(self,title):
        """
        进入游戏-登录界面-其他登录界面-忘记密码-密码找回
        Args:
            title: 忘记密码界面
        Returns:
            True: 找回密码成功界面
            False：找回密码失败界面
        """
        try:
            self.device.find_element_by_id(self.conf.other_log.id, timeout=5).click()
            time.sleep(10)
            self.device.click_by_id(self.conf.retrieve_password.id, timeout=5,desc="点击找回密码")
            time.sleep(5)
            self.device.find_element_by_xpath("// android.widget.TextView[@text='{}']".format(title), timeout=5)
            time.sleep(3)
        except:
            return False
        return True

    def Other_login_retrieve_password_email(self):
        """
        进入游戏-登录界面-其他登录界面-忘记密码

        Returns:
            True: 找回密码成功界面
            False：找回密码失败界面
        """
        try:
            self.device.find_element_by_id(self.conf.other_log.id, timeout=5).click()
            time.sleep(10)
            self.device.find_element_by_id(self.conf.retrieve_password.id, timeout=5).click()
            time.sleep(5)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='找回密码']")
        except  Exception as e:
            return False
        return True

    def customer(self):
        """
        进入游戏-登录界面-其他登录界面-客服界面

        Returns:
            True: 进入客服界面成功
            False：进入客服界面失败
        """
        try:
            self.device.click_by_id('com.iqiyigame.sdk:id/tv_custom_service', timeout=5,desc="进入客服页面")
            time.sleep(5)
            self.device.find_element_by_id('com.iqiyigame.sdk:id/tv_title', timeout=5)
        except  Exception as e:
            return False
        return True
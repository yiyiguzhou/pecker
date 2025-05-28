# -*- coding: UTF-8 -*-

"""
File Name:      intogame
Author:         fuhongzi
Create Date:    2018/5/9
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource


class login(object):
    def __init__(self, target):
        self.target = target
        self.data = target.data
        self.device = target.device

    """
           游客登录
           Returns:
               True: 进入成功
               False：进入失败
    """
    def guest_login(self,game_text=''):
        time.sleep(3)
        g_logger.info('guest login start:' + game_text)
        try:
            self.device.find_element_by_id("tourist", timeout=3).click()
            time.sleep(3)
            self.device.find_element_by_id("ntcBtn", timeout=3)
            g_logger.info('guest login success:' + game_text)
        except:
            g_logger.error('guest login failed:'+ game_text)
            return False
        return True

    """
              基线登录
              Returns:
                  True: 进入成功
                  False：进入失败
       """

    def base_login(self, account='', password=''):
        time.sleep(10)
        try:
            #点击“我的”
            self.device.find_element_by_id('com.qiyi.video:id/navi3', timeout=3).click()
            time.sleep(2)
            #点击密码登录
            self.device.find_element_by_id('com.qiyi.video:id/my_main_login', timeout=3).click()
            time.sleep(2)
            self.device.find_element_by_id('com.qiyi.video:id/img_four', timeout=3).click()
            time.sleep(2)
            self.device.find_element_by_id('com.qiyi.video: id/et_phone').set_text(name)
            self.device.find_element_by_id('com.qiyi.video:id/et_pwd').set_text(password)
            self.device.find_element_by_id('com.qiyi.video: id/tv_login', timeout=3).click()
            time.sleep(2)
        except:
            g_logger.error('base login failed')
            return False
        return True
    """
              普通账号登录
              Returns:
                  True: 进入成功
                  False：进入失败
       """
    def common_account_login(self, account='', password=''):
        time.sleep(10)
        try:
            self.device.find_element_by_id('normal_login_btn', timeout=3).click()
            time.sleep(2)
            self.device.find_element_by_id('user_name_login').set_text(account)
            # time.sleep(2)
            # self.device.adb.adb_shell("ime set com.nuance.swype.emui/com.nuance.swype.input.HuaweiIME")
            self.device.find_element_by_id('user_pswd_login').set_text(password)
            time.sleep(2)
            self.device.hide_keyboard()
            # self.device.adb.adb_shell("ime set ime set io.appium.android.ime/.UnicodeIME")
            self.device.find_element_by_id('login_btn', timeout=3).click()
            time.sleep(2)
            self.device.find_element_by_id("ntcBtn", timeout=3)
            g_logger.info('common_account login success')
        except:
            g_logger.error('common_account login failed')
            return False
        return True
    """
              普通账号登录
              Returns:
                  True: 进入成功
                  False：进入失败
       """
    def third_qq_login(self, account='', password=''):
        time.sleep(10)
        try:
            self.device.find_element_by_id('normal_login_btn', timeout=3).click()
            time.sleep(2)
            self.device.find_element_by_id('user_name_login').set_text(account)
            # time.sleep(2)
            # self.device.adb.adb_shell("ime set com.nuance.swype.emui/com.nuance.swype.input.HuaweiIME")
            self.device.find_element_by_id('user_pswd_login').set_text(password)
            time.sleep(2)
            self.device.hide_keyboard()
            # self.device.adb.adb_shell("ime set ime set io.appium.android.ime/.UnicodeIME")
            self.device.find_element_by_id('login_btn', timeout=3).click()
            time.sleep(2)
            self.device.find_element_by_id("ntcBtn", timeout=3)
            g_logger.info('common_account login success')
        except:
            g_logger.error('common_account login failed')
            return False
        return True
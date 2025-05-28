"""
File Name:      switch_account
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android

class Switch_account(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def sidebar(self, is_tourist, is_sms, phone_num):
        """
        点击侧边栏切换账号成功
        Returns:
            True：进入成功
            False：进入失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        time.sleep(3)
        for i in range(5):
            try:
                self.device.swipe(width / 2, height * 1 / 4, width / 2, height * 3 / 4)
                time.sleep(1)
                self.device.find_element_by_id('sidebar', timeout=5).click()
                time.sleep(2)
                break
            except  Exception as e:

                if i == 4:
                    return False
                continue
        # 进入侧边栏
        try:
            time.sleep(2)
            self.device.find_element_by_id(self.conf.sidebar_account.id, timeout=5).click()
            self.device.find_element_by_id(self.conf.switch_account.id, timeout=5).click()
            if is_tourist == 'TRUE':
                return self.tourist_login()
            elif is_sms == 'TRUE':
                return self.sms_login(phone_num)
            else:
                for i in range(30):
                    try:
                        self.device.find_element_by_id('normal_login_btn', timeout=5).click()
                        time.sleep(2)
                        self.device.find_element_by_id('login_btn', timeout=5)
                        break
                    except  Exception as e:
                        if i == 29:
                            return False
                        continue
        except:
            try:
                time.sleep(2)
                self.device.find_element_by_id('normal_login_btn', timeout=5).click()
                self.device.find_element_by_id('login_btn', timeout=5)
            except:
                return False
            return False
        return True


    def qq_login(self):
        """
        点击qq图标进行登录
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(2)
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(3)
            self.device.tap([(200,1490)], duration=1, timeout=5)
            # self.device.find_element_by_xpath(self.conf.into_qq_login_page.xpath, timeout=5).click()
            # self.device.find_element_by_xpath(self.conf.qq_one_login1.xpath, timeout=5).click()
            # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
        except  Exception as e:
            return False
        return True

    def tourist_login(self):
        """
        游客登录
        Returns:
            True：进入成功
            False：进入失败
        """
        try:

            self.device.find_element_by_id(self.conf.tourist.id, timeout=5).click()
        except:
            return False
        return True

    def sina_login(self, sina_account, sina_password):
        """
        点击sina图标进行登录
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(2)
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_xpath('//android.view.View[@content-desc="新浪微博账号登录"]', timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_xpath(self.conf.sina_interface.xpath, timeout=5)
            g_logger.info("进入微博登录页面")
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请用微博帐号登录']", timeout=5).set_text(
                sina_account)
            time.sleep(3)
            self.device.find_element_by_id('passwd', timeout=5).send_keys(sina_password)
            self.device.find_element_by_xpath(self.conf.sina_login_button.xpath, timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_id('sidebar', timeout=5)
            g_logger.info('sina login success')
        except  Exception as e:
            g_logger.error('sina login failed:')
        return True



    def into_mygame_page(self, title):
        """ 从游戏中心首页进入我的小游戏页
        Args:
         title: 页面标题
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(2)
        try:

            self.device.find_element_by_id(self.conf.into_mygame_page.id, timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
            g_logger.info("进入爱奇艺H5页面成功")
        except Exception as e:
            g_logger.error('进入爱奇艺H5页面失败')
            return False
        return True

    def coin(self):
        """
        从小游戏页进入游戏
        Returns:
            True：进入成功
            False：进入失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        time.sleep(1)
        try:
            self.device.swipe(width / 2,height * 1 / 4, width / 2,  height * 3 / 4)
            time.sleep(1)
            self.device.tap([(300, 400)], duration=1, timeout=3)
            # self.device.find_element_by_xpath(self.conf.small_game.xpath, timeout=5).click()
            try:
                time.sleep(2)
                self.device.find_element_by_xpath(self.conf.notice1.xpath, timeout=5)
                self.device.find_element_by_xpath(self.conf.return1.xpath, timeout=5).click()
                g_logger.info("进入小游戏成功")
            except  Exception as e:
                pass
        except  Exception as e:
            g_logger.info("进入小游戏失败")
            pass
        return True

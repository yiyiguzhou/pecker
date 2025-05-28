"""
File Name:      gift_share
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class Gift_share(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def gift(self, gift_text):
        """ 点击侧边栏领取礼包
        Args:
            game_text: 领取礼包按钮
        Returns:
            True：领取礼包成功
            False：领取礼包失败
        """
        try:
            time.sleep(5)
            self.device.find_element_by_id('sidebar', timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_id('libao', timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_xpath("//android.view.View[@content-desc='']".format(gift_text), timeout=5)
            time.sleep(2)
            g_logger.info("进入礼包领取页面成功")
        except  Exception as e:
            g_logger.info("进入礼包领取页面失败")
            return False
        return True

    def get_gift(self, receive, receive_look):
        """ 领取礼包
        Args:
            receive: 领取礼包界面按钮显示
            receive_look：领取礼包界面查看按钮显示
        Returns:
            True：领取礼包成功
            False：领取礼包失败
        """
        time.sleep(1)
        try:
            self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(receive),
                                              timeout=5).click()
            self.device.find_element_by_xpath("//android.view.View[@content-desc='激活码']", timeout=5)
            g_logger.info("礼包领取成功")
        except  Exception as e:
            try:
                self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(receive_look),
                                                  timeout=5).click()
                self.device.find_element_by_xpath("//android.view.View[@content-desc='激活码']", timeout=5)
                g_logger.info("礼包查看成功")
            except  Exception as e:
                return False
        return True

    def share(self,title1):
        """
        点击侧边栏进行分享
        Args:
            title1: 领取礼包界面按钮显示
        Returns:
            True：进入成功
            False：进入失败
        """
        try:
            time.sleep(6)
            self.device.find_element_by_id('sidebar', timeout=5).click()
            self.device.find_element_by_xpath(self.conf.into_share.xpath, timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title1), timeout=5).click()
            time.sleep(2)
        except  Exception as e:
            return False
        return True

    def qq_share(self,qq_account,qq_password):
        """
        QQ分享
        Args:
           qq_account: QQ账号
           qq_password：QQ密码
        Returns:
            True：分享成功
            False：分享失败
        """
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='发送到']", timeout=5)
                self.device.find_element_by_xpath(self.conf.my_computer.xpath, timeout=5).click()
                time.sleep(2)
                self.device.find_element_by_xpath(self.conf.qq_send.xpath, timeout=5).click()
                self.device.find_element_by_xpath("//android.widget.TextView[@text='已发送']", timeout=5)
                self.device.find_element_by_id(self.conf.return_iqiyi.id, timeout=5).click()
            except  Exception as e:
                # self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
                # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="请输入QQ号码或手机或邮箱"]', timeout=5).set_text(qq_account)
                self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="密码 安全"]',timeout=5).set_text(qq_password)
                self.device.find_element_by_xpath('//android.widget.Button[@content-desc="登录"]', timeout=5).click()
                self.device.find_element_by_xpath("//android.widget.TextView[@text='发送到']", timeout=5)
                self.device.find_element_by_xpath(self.conf.my_computer.xpath, timeout=5).click()
                time.sleep(2)
                self.device.find_element_by_xpath(self.conf.qq_send.xpath, timeout=5).click()
                self.device.find_element_by_xpath("//android.widget.TextView[@text='已发送']", timeout=5)
                self.device.find_element_by_id(self.conf.return_iqiyi.id, timeout=5).click()
                return False
        except  Exception as e:
            return False
        return True

    def qqzone_share(self,qq_account,qq_password):
        """
        QQ空间分享-qq已经登录
        Args:
           qq_account: qq账号
           qq_password：qq密码
        Returns:
            True：分享成功
            False：分享失败
        """
        try:
            self.device.find_element_by_id(self.conf.qq_zone_public.id, timeout=5).click()
            time.sleep(2)
        except  Exception as e:
            self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="请输入QQ号码或手机或邮箱"]',timeout=5).set_text(qq_account)
            self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="密码 安全"]', timeout=5).set_text(qq_password)
            self.device.find_element_by_xpath('//android.widget.Button[@content-desc="登录"]', timeout=5).click()
            self.device.find_element_by_id(self.conf.qq_zone_public.id, timeout=5).click()
        return True

    def sina_share(self):
        """
        新浪分享-手机有新浪微信微博账号登录
        Returns:
            True：分享成功
            False：分享失败
        """
        try:

            self.device.find_element_by_xpath("//android.widget.TextView[@text='转发到微博']", timeout=5)
            try:
                self.device.find_element_by_id('android:id/button1', timeout=5).click()
                self.device.find_element_by_xpath(self.conf.sina_send.xpath, timeout=5).click()
            except  Exception as e:
                self.device.find_element_by_xpath(self.conf.sina_send.xpath, timeout=5).click()
                time.sleep(2)
        except  Exception as e:
            return False
        return True


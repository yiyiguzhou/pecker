"""
File Name:      pay
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.sdk.android.mainland.mainland import Mainland

class Pay(Mainland):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def num(self, num):
        """
       支付方式
        Args:
            num:充值金额
        Returns:
            True: 进入成功
            False：进入失败
        """
        # 微信支付
        try:
            self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)

            self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
            time.sleep(5)

        except:
            return False
        return True

    def pay(self, select_pay):
        """
       进入支付页面
        Args:
            select_pay:选择支付方式
        Returns:
            True: 进入成功
            False：进入失败
        """
        # 支付宝支付
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
            time.sleep(2)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(select_pay),
                                              timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
            time.sleep(2)
            # self.device.find_element_by_id(self.conf.alipay_switch.id, timeout=5).click()
            # time.sleep(2)
            # self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入登录密码']", timeout=5)
            # self.device.find_element_by_xpath("//android.widget.Button[@text='手机号/邮箱/淘宝会员名']",timeout=5)
        except:
            return False
        return True

    def alipay_login(self, account,password,pay_password):
        """
       支付宝登录
        Args:
            account:账号
            password：密码
            pay_password：支付密码
        Returns:
            True: 登录成功
            False：登录失败
        """

            #支付宝登录支付
        try:
            try:
                #支付宝已登录
                self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
                self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']",timeout=6)
                self.device.find_element_by_xpath(self.conf.alipay_login_confirm.xpath, timeout=5).click()
                time.sleep(2)
                #输入支付密码
                #self.device.find_element_by_xpath(self.conf.alipay_login_confirm_password.xpath,timeout=5).set_text(pay_password)
                #time.sleep(2)
                #self.device.find_element_by_xpath("//android.widget.TextView[@text='支付成功']")
            except:
                #检测之前已有支付宝登陆过

                 self.device.find_element_by_xpath("//android.widget.TextView[@text='更多']",timeout=6)
                 self.device.find_element_by_xpath("//android.widget.TextView[@text='更多']", timeout=6).click()
                 #self.device.find_element_by_id(self.conf.more_pay_suss_ali.id, timeout=5).click()
                 self.device.find_element_by_xpath("//android.widget.TextView[@text='登录其他账号']").click()
                 #self.device.background_app(2, timeout=3)
                 self.device.find_element_by_xpath("//android.widget.EditText[@text='手机号/邮箱/淘宝会员名']", timeout=5).set_text(account)
                 time.sleep(2)
                 self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入登录密码']", timeout=5).set_text(password)
                 time.sleep(2)
                 self.device.find_element_by_id(self.conf.alipay_login.id, timeout=3).click()
                 #self.device.background_app(2, timeout=3)
                 # self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']",timeout=6)
                 self.device.find_element_by_xpath(self.conf.alipay_login_confirm.xpath, timeout=5).click()
                 time.sleep(5)
                 # 输入支付密码
                 # self.device.find_element_by_xpath(self.conf.alipay_login_confirm_password.xpath, timeout=5).set_text(pay_password)
                 # time.sleep(2)
                 #self.device.find_element_by_xpath("//android.widget.TextView[@text='支付成功']")
            return True
        except Exception as e:
            try:
                #账号密码登录
                self.device.find_element_by_xpath("//android.widget.EditText[@text='手机号/邮箱/淘宝会员名']",timeout=5)
                self.device.find_element_by_xpath("//android.widget.EditText[@text='手机号/邮箱/淘宝会员名']").set_text(account)
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入登录密码']", timeout=10).set_text(password)
                time.sleep(2)
                self.device.find_element_by_id(self.conf.alipay_login.id, timeout=5).click()
                time.sleep(6)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']")
                self.device.find_element_by_xpath(self.conf.alipay_login_confirm.xpath, timeout=5).click()
                time.sleep(3)
               # 输入支付密码
               # self.device.find_element_by_xpath(self.conf.alipay_login_confirm_password.xpath, timeout=5).set_text(pay_password)
               # time.sleep(2)
               # self.device.find_element_by_xpath("//android.widget.TextView[@text='支付成功']")
            except Exception as e:
                return True
            return False

    def wechatpay(self, num):
        """
       支付方式
        Args:
            num:充值金额
        Returns:
            True: 进入成功
            False：进入失败
        """
        #微信支付
        try:
            #self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
            self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)
            self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
            time.sleep(5)
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_id(self.conf.continue_pay.id, timeout=5).click()
            time.sleep(2)
            #self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(pay_select), timeout=5)
            #time.sleep(2)
            self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
            time.sleep(10)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']")
        except:
            return False
        return True

    def wechat_pay_suss(self,account,password):
        """登录
        微信支付
        Args:
            account: 登录账号
            password:登录密码
        Returns:
            微信未登录
            微信已经登录
        """
        time.sleep(2)
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']",timeout=5)
        except:
            return self.pay_wechat_interface(self,account, password)
        return self.pay_wechat_confirm(self)

    def pay_wechat_interface(self, title, account, password):
        """
        进入游戏-支付-微信支付—微信没有登陆
        Args:
            title:
            account：微信账号
            password：微信密码
        Returns:
            True: 微信支付界面显示正确
            False：微信支付显示失败
        """
        try:

            self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写微信号/QQ号/邮箱']", timeout=5).set_text(account)
            time.sleep(3)
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写密码']", timeout=5).set_text(password)
            time.sleep(3)
            # self.device.find_element_by_id(self.conf.pay_wechat_login.id, timeout=5).click()
            # time.sleep(6)
            # self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            # time.sleep(3)
            # self.device.find_element_by_id(self.conf.pay_wechat_one_click_login.id, timeout=5).click()
            # time.sleep(3)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']")
            # self.device.find_element_by_xpath(self.conf.pay_wechat_one_click_login_Password.xpath, timeout=5).set_text(pay_password)
            # time.sleep(5)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
            # time.sleep(2)

            # self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']")
            # time.sleep(3)
            # self.device.find_element_by_id(self.conf.into_pay_wechat_login.id, timeout=5).click()
        except  Exception as e:
            return False
        return True

    def pay_wechat_confirm(self, title):
        """
        进入游戏-充值-微信支付界面-微信支付
        Args:
            title:
        Returns:
            True: 支付成功
            False：支付失败
        """
        time.sleep(3)
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_id(self.conf.pay_wechat_one_click_login.id, timeout=5).click()
            time.sleep(3)
            # self.device.find_element_by_xpath(self.conf.pay_wechat_one_click_login_Password.xpath, timeout=5).set_text(pay_password)
            # time.sleep(5)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
            # time.sleep(2)
        except:
            return False
        return True

    def Alipay_suss(self, title, account, password):
        """
       支付宝方式
        Args:
            account:支付宝账号
            password：支付宝账号密码
        Return:
            True:
            False:
        """

        # 支付宝支付
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺']", timeout=5)
        except:
            return self.Alipay_login(self, account, password)
        return self.Alipay_login_confirm(self, title)

    def Alipay_login_confirm(self, title, pay_password):
        """
       支付宝登录
        Args:
           title:
           pay_password:
        Return:
            True:
            False:
        """
        # 支付宝支付
        try:
            self.device.find_element_by_xpath(self.conf.alipay_login_confirm.xpath, timeout=5).click()
            time.sleep(5)
            self.device.find_element_by_xpath(self.conf.alipay_login_confirm_password.xpath, timeout=5).set_text(
                pay_password)
            time.sleep(5)
            # self.device.find_element_by_xpath("//android.widget.EditText[@text='手机号/邮箱/淘宝会员名']")

        except:
            return False
        return True

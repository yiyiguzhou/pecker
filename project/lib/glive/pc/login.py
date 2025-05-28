# -*- coding: UTF-8 -*-

"""
File Name:      login
Author:         zhangwei04
Create Date:    2019/7/19
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.base_module.login import BaseLogin
from project.lib.glive.pc.common import Common


class Login(Common, BaseLogin):
    """登录类"""
    def __init__(self, target):
        super().__init__(target)
        self.current_user_name = None

    def password_login(self, account_section=None, account=None, password=None, check_chat_ready=False):
        self.close_recommend_tips()  # 关闭主播推荐弹窗
        self.close_lottery_tips()   # 关闭主播抽奖互动弹窗
        self.target.LiveRoom.get_fans_daily_welfare()
        if account_section:
            if self.account_conf.check_available(account_section):
                account = self.account_conf.get(account_section, "username")
                password = self.account_conf.get(account_section, "passwd")
            else:
                g_logger.error("查找账户配置文件section:{}失败".format(account_section))
                return False
        if self.check_is_login(account_section=account_section):
            if check_chat_ready:
                self.refresh()
                if not self.target.LiveRoom.check_chat_ready():
                    return False
            return g_logger.info("用户已登录,不重复登录")
        elif self.is_login():
            for i in range(2):
                if not self.logout():
                    return g_logger.error("用户已登录，执行退出登录失败")
                if not self.is_login():
                    break
                else:
                    g_logger.info("第一次退出登录失败，刷新页面，继续退出登录")
                    self.device.refresh()
                    time.sleep(1)
            else:
                return g_logger.error("用户已登录，2次执行退出登录失败")
        else:
            g_logger.info("用户未登录")

        self.target.Home.click_login_button()  # 点击登录按钮
        if self.is_login(timeout=2):
            g_logger.warning("检测到账户自动登录，刷新页面，重新退出登录")
            self.device.refresh()
            self.close_recommend_tips()  # 关闭主播推荐弹窗
            self.close_lottery_tips()  # 关闭主播抽奖互动弹窗
            self.logout()
            self.target.Home.click_login_button()

        try:
            with self.device.switch_frame("login_frame"):
                self.device.find_element_by_link_text("账号密码登录").click()
                # self.device.find_element_by_xpath("//a[@text='账号密码登录']").click()
                time.sleep(1)
                name_ele = self.device.find_element_by_xpath("//input[@data-pwdloginbox='name']")
                name_ele.clear()
                name_ele.send_keys(account)
                pwd_ele = self.device.find_element_by_xpath("//input[@data-pwdloginbox='pwd']")
                pwd_ele.clear()
                pwd_ele.send_keys(password)
                self.device.find_element_by_link_text("登录").click()
                time.sleep(2)
        except Exception as e:
            return False

        self.close_recommend_tips()  # 关闭主播推荐弹窗
        self.target.LiveRoom.get_fans_daily_welfare()
        self.current_user_name = account

        if check_chat_ready:
            self.refresh()
            if not self.target.LiveRoom.check_chat_ready():
                return False
        return True

    def qq_login(self):
        return False

    def sms_login(self):
        """短信登录"""
        g_logger.error("不支持短信登录")
        return False

    def wechat_login(self):
        return False

    def is_login(self, timeout=3):
        return not self.device.check_ele_by_xpath("//div[@class='login']/a[@data-user='login-btn']", timeout=timeout)

    def logout(self):
        """退出登录"""
        if self.is_login():
            g_logger.info("已登录，退出重新登录")
            try:
                ele = self.device.find_element_by_link_text("个人中心")
                self.device.move_to_element(ele)
                self.device.find_element_by_xpath("//a[@class='exit' and @data-user='logout-btn']").click()
                time.sleep(1)
            except:
                return g_logger.error("用户已登录，未找到个人中心或退出按钮")
        else:
            return g_logger.info("用户未登录，不需要退出登录")
        self.current_user_name = None
        return True

    def check_is_login(self, account_section=None):
        """
        检测用户已经登录
        Args:
            account_section: 用户session，若此参数为空，则仅检测是否登录
        Returns:
            True: (用户)已登录， False: 未登录或者当前登录不是此用户
        """
        if not self.is_login():
            return False
        elif account_section:
            try:
                ele = self.device.find_element_by_link_text("个人中心", timeout=3)
                self.device.move_to_element(ele)
                time.sleep(0.5)
            except:
                pass
            base_name = self.account_conf.get(account_section, "base_name")
            if not base_name:
                return g_logger.error("检测用户是否登录：用户配置文件，未配置基线用户名base_name,假设为未登录状态")
            ele = self.device.get_ele_by_xpath(self.conf.home_user.name, timeout=3)
            if ele:
                return ele.text == base_name
            else:
                return g_logger.error("检测用户是否登录：未找到用户登录的基线用户名,假设为未登录状态")
        else:   # 没有用户账户匹配，且已经登录
            return True


if __name__ == "__main__":
    class Target:
        def __init__(self):
            self.data=None
            self.device=None


    l = Login(target=Target())
    b = l.sms_login()

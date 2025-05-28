# -*- coding: UTF-8 -*-

"""
File Name:      livetool
Author:         zhangwei04
Create Date:    2019/8/8
"""
import re
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread
from appium.webdriver.common.touch_action import TouchAction
from framework.exception.exception import TimeoutException
from project.lib.android import Android


class LiveTool(Android):
    """直播工具类"""
    def __init__(self, target, ele_conf_name='android_live_tool'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def launch_live_tool(self):
        """打开直播工具"""
        self.device.adb.start_app("com.qiyi.game.live", "com.qiyi.game.live.activity.MainActivity", stop_flag=True)
        time.sleep(3)
        return True

    def check_is_login(self):
        """
        根据是否有房间号检测是否已登录
        Returns:
            True: 已经登录， False: 没有登录
        """
        try:
            self.device.find_element_by_id(self.conf.home.room_number, timeout=2)
            return True
        except:
            return False

    def get_room_number(self):
        """
        读取直播房间号
        Returns:
            int: 直播房间号, None：获取房间号失败
        """
        try:
            ele = self.device.find_element_by_id(self.conf.home.room_number, timeout=2)
            number = re.findall("\d+", ele.get_attribute("text"))[0]
            return int(number)
        except:
            return None

    def passwd_login(self, account_section):
        """
        用户密码登录
        Args:
            account_section: 直播用户section，在account.conf文件里面配置
        Returns:
            True: 登录成功, False: 登录失败
        """
        username = self.account_conf.get(account_section, "username")
        passwd = self.account_conf.get(account_section, "passwd")
        # room = self.account_conf.get(account_section, "room")
        g_logger.info("账户密码登录")

        if not self.device.click_by_id(self.conf.home.passwd_login, desc="账号密码登录按钮"):
            return False
        try:
            user_ele = self.device.find_element_by_id(self.conf.login.account, timeout=5)
            user_ele.clear()
            user_ele.set_text(username)
        except:
            return g_logger.error("查找用户元素，输入用户名失败")

        try:
            self.device.find_element_by_id(self.conf.login.passwd, timeout=5).set_text(passwd)
        except Exception as e:
            return g_logger.error("查找输入密码元素，输入密码失败")

        if not self.device.click_by_id(self.conf.login.login, desc="登录按钮"):
            return False
        time.sleep(2)
        return self.check_is_login()

    def logout(self):
        """
        退出登录
        Returns:
            True: 退出登录成功, False: 退出登录失败
        """
        if not self.device.click_by_id(self.conf.home.user_icon, desc="点击首页用户图标"):
            return False
        if not self.device.click_by_id(self.conf.my.user_icon, desc="点击我的页用户图标"):
            return False
        if not self.device.click_by_id(self.conf.my_info.logout, desc="点击个人资料页退出按钮"):
            return False
        if not self.device.click_by_id(self.conf.my_info.logout_ok, desc="点击个人资料页退出确认按钮"):
            return False
        g_logger.info("检测非登录状态")
        return not self.check_is_login()

    def once_step_live(self, account_section, title, second_lab, first_lab=None, horizon=True):
        """
        一键开播
        Args:
            account_section: 用户
            title: 直播标题
            second_lab: 直播二级分类
            first_lab: 直播一级分类
            horizon: 是否横屏
        Returns:
            True: 一键开启成功, False: 开启失败
        """
        self.launch_live_tool()
        room_number = self.get_room_number()
        if room_number:
            # 已登录
            try:
                anchor_room = int(self.account_conf.get(account_section, "room"))
            except:
                return g_logger.error("读取配置文件主播{}直播间失败".format(account_section))
            if room_number != anchor_room:
                self.logout()
                if not self.passwd_login(account_section):
                    return False
        else:
            if not self.passwd_login(account_section):
                return False

        return self.start_live(title, second_lab, first_lab=first_lab, horizon=horizon)

    def start_live(self, title, second_lab, first_lab=None, horizon=True):
        """
        开启直播,当前用户已登录，且处于首页
        Args:
            title: 直播标题
            second_lab: 直播二级分类标签
            first_lab: 直播一级分类标签
            horizon: 是否横屏开播
        Returns:
            True: 开启成功, False: 开启失败
        """
        if not self._select_subject(second_lab, first_lab=first_lab):
            return False
        if not self._write_title(title):
            return False
        if not self.device.click_by_id(self.conf.home.card_start_live, desc="录屏开播", timeout=5):
            return False
        if horizon:
            if not self.device.click_by_id(self.conf.home.horizon_live, desc="横屏开播", timeout=5):
                return False
        else:
            if not self.device.click_by_id(self.conf.home.vertical_live, desc="竖屏开播", timeout=5):
                return False
        if not self.device.click_by_id(self.conf.home.start_live, desc="开始直播", timeout=5):
            return False

        self.device.click_by_xpath(self.conf.home.start_immediately, timeout=3)

        time.sleep(2)
        return self._check_living()

    def _check_living(self):
        """
        检测是否正在直播
        Returns:
            True:正在直播, False: 没有
        """
        try:
            self.device.find_element_by_id(self.conf.live_room.stop, timeout=5)
            return True
        except:
            return False

    def _select_subject(self, second_lab, first_lab=None):
        """
        选择主播主题
        Args:
            second_lab: 二级标签
            first_lab: 一级标签
        Returns:
            True: 选择成功, False: 选择失败
        """
        self.device.click_by_id(self.conf.home.card_subject, desc="游戏直播标题", timeout=5)
        if first_lab:
            if not self.device.click_by_xpath(self.conf.subject.first_label.format(first_lab), desc="一级直播标题:{}".format(first_lab), timeout=5):
                return False
        return self.device.click_by_xpath(self.conf.subject.second_label.format(second_lab), desc="二级直播标题:{}".format(second_lab), timeout=5)

    def _write_title(self, title):
        """
        写直播间标题
        Args:
            title: 直播间标题
        Returns:
            True: 写入成功, False: 写入失败
        """
        try:
            ele = self.device.find_element_by_id(self.conf.home.card_title)
            ele.clear()
            ele.set_text(title)
        except:
            return g_logger.error("写入标题失败")
        return g_logger.info("写入标题成功")

    def stop_live(self, room_number=None):
        """
        停止直播，返回首页
        Args:
            room_number: 直播间号
        Returns:
            True: 停止成功, False: 停止失败
        """
        if not self._check_living():
            return g_logger.error("当前不在直播中")
        if not self.device.click_by_id(self.conf.live_room.stop, desc="停止直播", timeout=5):
            return False
        if not self.device.click_by_xpath(self.conf.live_room.stop_ensure, desc="退出直播", timeout=5):
            return False
        if not self.device.click_by_id(self.conf.live_stop_page.back_to_home, desc="回首页", timeout=5):
            return False
        if room_number is None:
            return self.check_is_login()
        else:
            return int(room_number) == self.get_room_number()
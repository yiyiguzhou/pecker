"""
File Name:      identity_real_name_authentication
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class Identity_real_name_authentication(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def identity_name_authentication(self, name, id_card):
        """
        进入安全实名认证页面进行身份认证
        Args:
            name: 身份证姓名
            id_card：身份证号码
        Returns:
            True：身份认证成功
            False：身份认证失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.secure_real_name_certification1.xpath, timeout=5)
            try:
                self.device.find_element_by_xpath('//android.widget.EditText[@text="请输入您的真实姓名"]', timeout=5).set_text(name)
                self.device.find_element_by_xpath('//android.widget.EditText[@text="请输入您的身份证"]', timeout=5).set_text(id_card)
                self.device.find_element_by_xpath(self.conf.once_conf.xpath, timeout=5).click()
                g_logger.info("身份实名认证成功")
            except  Exception as e:
                pass
                return False
        except  Exception as e:
            g_logger.info("该账号身份认证过")
        return True
"""
File Name:      bind_account
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class Bind_account(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def sidebar_binding(self):
        """
        点击侧边栏进行手机绑定页面
        Returns:
            True：进入页面成功
            False：进入页面失败
        """
        try:
            time.sleep(6)
            self.device.find_element_by_xpath(self.conf.sidebar.xpath, timeout=5).click()
            self.device.find_element_by_id(self.conf.sidebar_account.id, timeout=5).click()
            self.device.find_element_by_xpath("//android.view.View[@content-desc='绑定手机']", timeout=5).click()
            self.device.find_element_by_xpath("//android.view.View[@content-desc='绑定手机']", timeout=5)
        except  Exception as e:
            return False
        return True

    def binding_phone(self,phone_num1,phone_num2,new_password):
        """
        绑定账号
        Args:
            phone_num1: 手机号
            phone_num2：未注册过的手机号
            new_password:手机新密码
        Returns:
            True：账号显示成功
            False：账号显示失败
        """
        try:
            self.device.find_element_by_xpath("//android.view.View[@content-desc='绑定手机']", timeout=5)
            self.device.find_element_by_xpath("//android.view.View[@content-desc='绑定手机']", timeout=5).click()
            try:
                self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入手机号码']", timeout=5).set_text(phone_num1)
            except Exception as e:
                pass
            # 移除日志
            self._rm_ipecker_log()
            try:
                self.device.find_element_by_xpath(self.conf.get_phone1_code.xpath, timeout=10).click()
                try:
                    self.device.find_element_by_xpath("//android.view.View[@content-desc='绑定其他手机号']", timeout=5)
                    g_logger.info("账号被占用")
                    g_logger.info("请用其他账号绑定")
                    try:
                        self.device.find_element_by_xpath("//android.view.View[@content-desc='绑定其他手机号']",timeout=5).click()
                        self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入手机号码']",timeout=5).set_text(phone_num2)
                    except Exception as e:
                        pass

                        # 移除日志
                    self._rm_ipecker_log()
                    try:
                        self.device.find_element_by_xpath(self.conf.get_phone1_code.xpath, timeout=10).click()
                        time.sleep(1)
                    except Exception as e:
                        pass
                    # 切换到android输入法
                    self.device.adb.adb_shell('ime set com.android.inputmethod.latin/.LatinIME')
                    ret = True
                    data_list = self._get_sms_from_ipecker_log()

                    for data in data_list:
                        g_logger.info(data)
                        try:
                            # for i, char in enumerate(data):
                            #     id_n = "com.qiyi.video:id/enter_pwd_block%d" % (i + i)
                            #     self.device.find_element_by_id(id_n).send_keys(char)
                            self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入短信验证码']",timeout=5).set_text(data)
                        except Exception as e:
                            continue

                    # 确认
                    try:
                        # 输入新密码
                        self.device.find_element_by_id(self.conf.enter_new_password.id, timeout=5).set_text(new_password)
                        # 确定绑定手机
                        self.device.find_element_by_xpath(self.conf.phone1_confirm.xpath, timeout=5).click()
                        g_logger.info("绑定成功")
                    except Exception as e:
                        pass
                        # 切回appium输入法
                    self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
                    return ret
                except Exception as e:
                    g_logger.info("账号被占用")
            except  Exception as e:
                return False
        except  Exception as e:
            return False
"""
File Name:      mobile_phone_real_name_authentication
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class Mobile_phone_real_name_authentication(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def mobileauthentication(self, phone_num):
        """
        手机实名认证
        Args:
            phone_num: 手机号
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.notice1.xpath, timeout=5)
            self.device.find_element_by_xpath(self.conf.confirm_at_once1.xpath, timeout=5).click()
            try:
                self.device.find_element_by_xpath(self.conf.confirm_phone1.xpath, timeout=5)
                try:
                    # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入您的手机号']", timeout=10).send_keys(phone)
                    self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入手机号码']", timeout=5).set_text(
                        phone_num)
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
                        self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入短信验证码']",
                                                          timeout=5).set_text(data)


                    except Exception as e:
                        continue

                # 确认
                try:
                    # 确认
                    self.device.find_element_by_xpath(self.conf.phone1_confirm.xpath, timeout=5).click()
                    time.sleep(2)
                    try:
                        # 验证成功
                        self.device.find_element_by_xpath(self.conf.verify_success1.xpath, timeout=5)
                        g_logger.info("手机认证成功")
                    except Exception as e:
                        g_logger.info("绑定密码成功")



                except Exception as e:
                    pass
                    # 切回appium输入法
                self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
                return ret
            except  Exception as e:
                return False
        except Exception as e:
            g_logger.info("该账号已经进行过手机实名认证")
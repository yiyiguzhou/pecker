"""
File Name:      login_and_register
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.sdk.android.mainland.mainland import Mainland


class  Registered(Mainland):
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




    def Account_correct(self,cache_account):
        """
        进入游戏-侧边栏-账户显示正确
        Args:
            cache_account: 缓存账号
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        try:
            # self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(2)
            self.device.click_by_xpath("//android.widget.TextView[@text='{}']".format(cache_account), timeout=5,desc="账号显示")
            time.sleep(2)
        except:
            return False
        return True

    def iqiyi_login(self):
        """
        进入游戏-登录-爱奇艺登录页面

        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
            time.sleep(5)

            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_id(self.conf.iqiyi_login.id, timeout=5).click()
            # self.device.find_element_by_xpath("//android.widget.Button[@text='一键授权登录']", timeout=10).click()
            time.sleep(2)
        except Exception as e:
            self.device.find_element_by_xpath("//android.widget.Button[@text='一键授权登录']")
            return False
        return True



    def Other_login(self, vip_time):
        """
        进入游戏-登录界面-其他登录界面
        Args:
            vip_time: 会员到期时间
            #登录注册页面
            #注销页面-若是会员账号 提前设置好会员到期时间
        Returns:
            True: 进入其他登录界面
            False：进入失败
        """
        time.sleep(2)
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        try:
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(2)
            try:
                self.device.click_by_xpath("//android.widget.TextView[@text='{}']".format(vip_time), timeout=5)
                self.device.click_by_id(self.conf.into_logout.id, timeout=5,desc="点击进入注销页面")
                time.sleep(3)
                self.device.click_by_id(self.conf.logout.id, timeout=5,desc="点击注销手机号")
                time.sleep(3)
                self.device.click_by_id(self.conf.other_log.id, timeout=5,desc="点击进入其他登录页面")
            except Exception as e:
                self.device.click_by_id(self.conf.into_logout.id, timeout=5,desc="点击进入注销页面")
                self.device.click_by_id(self.conf.logout_mobile.id, timeout=5,desc="点击注销手机号")
                self.device.click_by_id(self.conf.other_log.id, timeout=5,desc="点击进入其他登录页面")
        except Exception as e:
            pass
            # 滑动查找切换账号
            for i in range(10):
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='切换账号']", timeout=5).click()
                    time.sleep(2)
                    break
                except:
                    if i == 9:
                        return False
                    self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
                    time.sleep(1)
                    continue
        self.device.find_element_by_id('com.iqiyigame.sdk:id/tv_custom_service', timeout=5)
        time.sleep(3)
        return True

    def mobilelogin_sms(self, phone):
        """
        短信方式登录
        Args:
            phone: 手机号
        """
        # 手机号
        time.sleep(5)
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入您的手机号']", timeout=10).send_keys(phone)
            self.device.find_element_by_id(self.conf.mobile_verifylogin.id, timeout=5).set_text(phone)
        except Exception as e:
            pass
        # 移除日志
        self._rm_ipecker_log()

        try:
            self.device.click_by_id(self.conf.get_verifycode.id, timeout=10,desc="点击获取验证码按钮")
            # self.device.find_element_by_xpath("//android.widget.Button[@text='获取短信验证码']", timeout=10).click()
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
                self.device.find_element_by_id(self.conf.sms_code.id, timeout=5).set_text(data)
            except Exception as e:
                continue

        # 确认
        try:
            # 进入游戏
            self.device.click_by_id(self.conf.into_game.id, timeout=5,desc="点击进入游戏按钮")
            time.sleep(2)
        except Exception as e:
            pass
            # 切回appium输入法
        self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
        return ret

    def initialize_wetchat_login(self):
        """
        进入游戏-点击初始微信信登录按钮

        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(5)
        try:
            self.device.click_by_id(self.conf.init_wetchat.id, timeout=5,desc="点击初始微信信登录按钮")
        except Exception as e:
            return False
        return True

    def Tourist_login(self):
        """
        进入游戏-侧边栏-游客试玩

        Returns:
            True: 自动登录账号显示正常
            False：自动登录失败
        """
        try:
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(2)
            self.device.find_element_by_id(self.conf.into_logout.id, timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_id(self.conf.logout.id, timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_id(self.conf.tourist_game.id, timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
        except  Exception as e:
            return False
        return True

    def account_password_login(self, account, password):
        """
        进入游戏-侧边栏-其他登录方式—账号密码登录
        Args:
            account: 登录账号
            password：登录密码
        Returns:
            True: 自动登录账号显示正常
            False：自动登录失败
        """
        time.sleep(2)
        try:
            self.device.click_by_id(self.conf.other_log.id, timeout=5,desc="点击其他登录按钮")
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_id(self.conf.old_user.id, timeout=5).set_text(account)
            self.device.find_element_by_id(self.conf.old_user_password.id, timeout=5).set_text(password)
            time.sleep(3)
            self.device.click_by_id(self.conf.old_user_into.id, timeout=5,desc="点击进入游戏按钮")
            time.sleep(6)
            try:
                self.device.find_element_by_xpath('//android.widget.TextView[@text="安全实名认证"]', timeout=5)
                self.device.click_by_id(self.conf.mobile_authentication_interface_close.id, timeout=5,desc="点击关闭实名认证界面")
                self.device.click_by_id(self.conf.initialize_qq.id, timeout=5,desc="点击初始化qq登录按钮")
            except Exception as e:
                pass
                time.sleep(3)
                self.device.click_by_id(self.conf.initialize_qq.id, timeout=5, desc="点击初始化qq登录按钮")
        except  Exception as e:
            return False
        return True

    def initialize_QQ_login(self):
        """
        进入游戏-点击初始QQ登录

        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        try:
            self.device.click_by_id(self.conf.initialize_qq.id, timeout=5,desc="点击初始化QQ登录")
        except Exception as e:
            return False
        return True

    def qq_login_interface(self,is_qq,vip_time):
        """
        初始化QQ登录-qq授权登录
        Args:
            is_qq:qq登录开关
            vip_time：会员到期时间
        Returns:
            True: 微信登录成功
            False：微信登录失败
        """
        time.sleep(3)
        try:

            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(1)
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(vip_time), timeout=5)
                self.device.find_element_by_id(self.conf.into_logout.id, timeout=5).click()
                time.sleep(3)
                self.device.find_element_by_id(self.conf.logout.id, timeout=5).click()
                self.device.find_element_by_id(self.conf.into_qq_login_old.id, timeout=5).click()
                time.sleep(3)
            except Exception as e:
                return self.switch_login(is_qq)
        except Exception as e:
            return False
        return True

    def switch_login(self,is_qq):
        """
        进入游戏-滑动查找切换账号
        Args:
            is_qq: QQ登录的开关
        Returns:
            True: 显示成功
            False：显示失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        try:
            # 滑动查找切换账号
            for i in range(10):
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='切换账号']",timeout=5).click()
                    time.sleep(2)
                    break
                except:
                    if i == 9:
                        return False

                    self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
                    time.sleep(1)
                    continue
            if is_qq == "TRUE":
                self.device.find_element_by_id('com.iqiyigame.sdk:id/login_qq', timeout=5).click()
            else:
                self.device.click_by_id(self.conf.other_log.id, timeout=5,desc="点击其他登录界面").click()
                time.sleep(3)
        except:
            return False
        return True

    def qq(self, qq, qq_password):
        """
        qq登录-授权登录
        Args:qq：qq账号
            qq_password：QQ密码
        Returns:
            True: 登录成功
            False：登录失败
        """
        try:
            # self.device.background_app(1, timeout=3)
            self.device.click_by_id(self.conf.into_qq_login_old.id, timeout=5,desc="点击其他登录按钮")
            time.sleep(3)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_xpath("//android.widget.Button[@text='授权并登录']", timeout=5)
            self.device.click_by_xpath("//android.widget.Button[@text='授权并登录']", timeout=5,desc="点击授权登录")
            time.sleep(3)
        except:
            try:
                self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
                self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                self.device.find_element_by_xpath("//android.widget.Button[@text='登录']", timeout=5)
                self.device.find_element_by_xpath("//android.widget.Button[@text='登录']", timeout=5).click()
            except:
                try:
                    self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
                    self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                    self.device.find_element_by_xpath(self.conf.qq_account.xpath, timeout=5).set_text(qq)
                    time.sleep(5)
                    self.device.find_element_by_id(self.conf.qq_password.id, timeout=5).set_text(qq_password)
                    time.sleep(5)
                    self.device.click_by_id(self.conf.enter_qq.id, timeout=5,desc="登录QQ")
                    time.sleep(5)
                except Exception as e:
                    return True
            return True
        return True

    def wetchat_login(self,wechat_account,wechat_password):
        """
        进入游戏-登录-初始化微信登录-微信登录
        Args:
           wechat_account:微信账号
           wechat_password：微信密码
        Returns:
            True: 微信登录成功
            False：微信登录失败
        """
        time.sleep(3)
        try:
            try:
                self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
                self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                self.device.click_by_id(self.conf.into_wechat_login.id, timeout=5,desc="进入微信登录按钮")
                time.sleep(3)
            except Exception as e:
                return self.wechat_login(wechat_account,wechat_password)
        except:
            return False
        return True

    def wechat_login(self,wechat_account,wechat_password):
        """
        填写账号密码进入微信登录
         Args:wechat_account：微信账号
              wechat_password：微信密码
        :return:
            True: 进入成功
            False：进入失败
        """
        try:
            time.sleep(5)
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写微信号/QQ号/邮箱']", timeout=5).set_text(wechat_account)
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写密码']", timeout=5).set_text(wechat_password)
            time.sleep(6)
            self.device.click_by_xpath("//android.widget.Button[@text='登录']", timeout=5,desc="登录按钮")
            time.sleep(6)
        except:
            return self.authentication_close()
        return True

    def authentication_close(self):
        """
        出现实名认证关闭
        Returns:
            True: 关闭成功
            False：关闭失败
        """
        time.sleep(3)
        try:
            self.device.find_element_by_xpath('//android.widget.TextView[@text="安全实名认证"]', timeout=5)
            self.device.find_element_by_id(self.conf.mobile_authentication_interface_close.id, timeout=5).click()
            self.device.find_element_by_xpath('//android.widget.TextView[@text="通知"]', timeout=5)
            self.device.find_element_by_id(self.conf.mobile_authentication_close.id, timeout=5).click()
        except:
            return self.notice_close()
        return True

    def notice_close(self):
        """
        出现手机验证页面关闭
        Returns:
            True: 关闭成功
            False：关闭失败
        """
        time.sleep(3)
        try:
            self.device.find_element_by_xpath('//android.widget.TextView[@text="通知"]', timeout=5)
            self.device.find_element_by_id(self.conf.mobile_authentication_close.id, timeout=5).click()
        except:
            return False
        return True
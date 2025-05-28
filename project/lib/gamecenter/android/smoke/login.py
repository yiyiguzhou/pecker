# -*- coding: UTF-8 -*-

"""
File Name:      login
Author:         gufangmei_sx
Create Date:    2018/8/14
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.gamecenter.android.smoke.common import Common


class Login(Common):
    """登录操作类"""
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android')

        self.target = target
        self.data = target.data
        self.device = target.device

    def login_in(self, account=None, password=None, account_section=None):
        """
        用户登录
        Args:
            account: 用户账号
            password: 密码
            account_section:  读取project/conf/element_conf/account.conf里面section名，若传入此参数，则优先读取对应section里面的用户名和密码
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            time.sleep(2)
            self.device.click_by_id(self.conf.gamecenter_user.id, timeout=5, desc="点击基线我的tab")
            time.sleep(2)
            self.device.click_by_xpath("//android.widget.TextView[@text='登录']", timeout=5, desc="点击登录按钮")
            try:
                self.login_in_with_password(account, password, account_section=account_section)
                self.device.click_by_id(self.conf.gamecenter_game_download_back.id, timeout=5, desc="点击返回按钮")
            except:
                return False
        except:
             g_logger.info("用户已登录")
        return True

    def base_login_in(self, account=None, password=None, account_section=None):
        """
        游戏中心基线入口--密码登录
        Args:
            account: 登录账号
            password: 登录密码
            account_section:  读取project/conf/element_conf/account.conf里面section名，若传入此参数，则优先读取对应section里面的用户名和密码
        Returns:
            True: 进入成功
            False：进入失败
        """
        if not self.device.click_textview_text("我的", timeout=15):
            return False
        if not self.device.click_textview_text("登录", timeout=10):
            return False
        return self.login_in_with_password(account, password, account_section=account_section, check_title="我的")

    def login_in_with_password(self, account=None, password=None, account_section=None, check_title="个人中心"):
        """
        游戏中心--密码登录
        Args:
            account: 登录账号
            password: 登录密码
            account_section:  读取project/conf/element_conf/account.conf里面section名，若传入此参数，则优先读取对应section里面的用户名和密码
            check_title: 检测标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        if account_section:
            if self.account_conf.check_available(account_section):
                account = self.account_conf.get(account_section, "username")
                password = self.account_conf.get(account_section, "passwd")
            else:
                g_logger.error("查找账户配置文件section:{}失败".format(account_section))
                return False
        return self.enter_account_password(account, password, check_title=check_title) if self._exchange_login_style('password') else False

    def enter_account_password(self, account, password, check_title="个人中心"):
        """
        输入账号密码登录
        Args:
            account: 登录账号
            password: 密码
            check_title: 检测标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_id(self.conf.gamecenter_my_game_vip_login_account.id, timeout=5).send_keys(account)
            self.device.find_element_by_id(self.conf.gamecenter_my_game_vip_login_password.id, timeout=5).send_keys(password)
            time.sleep(2)
            self.device.click_by_id(self.conf.gamecenter_my_game_vip_login_in.id, timeout=5, desc="点击登录按钮")
            time.sleep(2)

            manu = self.device.get_manufacturer()
            if manu in ('vivo', 'google'):
                if not self._cancel_finger_login():
                    # return False
                    pass
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(check_title), timeout=5)
        except:
            return False
        return True

    def login_in_with_sms(self, account):
        """
        游戏中心--短信验证码登录
        Args:
            account: 登录账号
        Returns:
            True: 进入成功
            False：进入失败
        """
        if not self._exchange_login_style("sms"):
            return False
        try:
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入您的手机号']", timeout=5)
        except:
            self.device.click_by_xpath("//android.widget.TextView[@text='切换账号']", timeout=5, desc="点击切换账号按钮")

        return self._mobile_sms_authentication(account)

    def login_in_with_qq(self):
        """
        游戏中心--qq登录（手机qq已登录）
        Returns:
            True: 进入成功
            False：进入失败
        """
        if not self._exchange_login_style("qq"):
            return False

        time.sleep(5)
        self.device.screen_tap(self.conf.gamecenter_qq_login)
        time.sleep(3)

        manu = self.device.get_manufacturer()
        if manu in ('vivo', 'google'):
            self._cancel_finger_login()

        try:
            g_logger.info("检测个人中心   ")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=10)
        except Exception as e:
            return False

        return True

    def login_in_with_wechat(self):
        """
        游戏中心--微信登录
        Returns:
            True: 进入成功
            False：进入失败
        """
        if not self._exchange_login_style('wechat'):
            return False

        manu = self.device.get_manufacturer()
        if manu in ('vivo', 'google'):
            if not self._cancel_finger_login():
                # return False
                pass

        for i in range(2):
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=10)
                break
            except:
                try:
                    g_logger.info("查看并点击微信授权登录")
                    self.device.find_element_by_xpath("//android.widget.Button[@text='确认登录']", timeout=5).click()
                    continue
                except:
                    pass
        else:
            return False
        return True

    def _exchange_login_style(self, login_style):
        login_style_set = ("sms", "password", "qq", "wechat")
        if login_style == "password":
            # 当前页已经是密码登录页面
            try:
                # self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入手机号或邮箱']", timeout=5)
                self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写密码']", timeout=5)
                return True
            except:
                xpath = self.conf.gamecenter_my_setting_password_login.icon_xpath
        elif login_style == "sms":  # 手机验证码登录
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='获取短信验证码']", timeout=5)
                return True
            except:
                xpath = self.conf.gamecenter_my_setting_sms_login.icon_xpath
        elif login_style == 'qq':
            try:
                self.device.click_by_xpath("//android.widget.TextView[@text='QQ登录']", timeout=5)  # 点击到QQ授权页面
                return True
            except:
                xpath = self.conf.gamecenter_my_setting_qq_login.icon_xpath

        elif login_style == 'wechat':
            try:
                self.device.click_by_xpath("//android.widget.TextView[@text='微信登录']", timeout=5) # 点击到微信登录界面
                return True
            except:
                xpath = self.conf.gamecenter_my_setting_wechat_login.icon_xpath

        # 滑动其他方式登录键
        try:
            ele = self.device.find_element_by_xpath("//android.widget.TextView[@text='其它方式登录']/../..", timeout=30)
        except:
            g_logger.error("查找更多登录模块栏失败")
            return False
        x, y = ele.location['x'], ele.location['y']
        width, height = ele.size['width'], ele.size['height']
        start_x, start_y = x + width * 9 / 10, y + height / 2
        end_x, end_y = x + width / 10, y + height / 2
        for i in range(3):
            try:
                self.device.click_by_xpath(xpath, timeout=10)
                time.sleep(2)
                return True
            except:
                self.device.swipe(start_x, start_y, end_x, end_y)
                time.sleep(1.5)
        else:
            g_logger.error("手机号码方式查找登录入口图标失败")
            return False

    def base_login_out(self):
        """
        用户退出登录
        Returns:
            True: 进入成功
            False：进入失败
        """
        # if not self.target.BasePage.into_home_page():
        #     return False
        g_logger.info("等待5秒")
        time.sleep(5)
        if not self.target.BasePage.into_my():
            return False
        if self.device.check_textview_text('登录', timeout=5):
            g_logger.error("用户未登录")
            return True
        if not self.device.click_textview_text('设置', swipe=True, timeout=60):
            g_logger.error("基线我的点击'设置'入口失败")
            return False

        if not self.device.click_textview_text('退出登录', swipe=True, timeout=60):
            g_logger.error("设置页'退出登录'失败")
            return False

        manu = self.device.get_manufacturer()
        if manu in ('vivo', 'google'):
            if not self._cancel_finger_login():
                return self.device.click_textview_text('退出登录', swipe=True, timeout=30)
            else:
                return True
        else:
            if not self.device.click_textview_text('退出登录', swipe=True, timeout=60):
                g_logger.error("'退出登录'失败")
                return False
        return True

    def into_login_page_bought(self):
        """
        从已购买tab进入基线登录页面
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_id(self.conf.gamecenter_user.id, timeout=5, desc="点击基线我的tab")
            time.sleep(2)
            self.device.click_by_xpath("//android.widget.TextView[@text='已购买']", timeout=5, desc="点击已购买按钮")
            self.device.click_by_xpath("//android.widget.Button[@text='登录']", timeout=5, desc="点击登录按钮")
        except:
             return False
        return True

    def into_login_page_reserved(self):
        """
        从已预约tab进入基线登录页面
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_id(self.conf.gamecenter_user.id, timeout=5, desc="点击基线我的tab")
            time.sleep(2)
            self.device.click_by_xpath("//android.widget.TextView[@text='已预约']", timeout=5, desc="点击已预约按钮")
            self.device.click_by_xpath("//android.widget.Button[@text='登录']", timeout=5, desc="点击登录按钮")
        except:
             return False
        return True

    def into_login_page(self):
        """
        个人中心页上方登录模块的“登录”按钮进入基线登录页面
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_id(self.conf.gamecenter_user.id, timeout=5, desc="点击个人中心")
            time.sleep(2)
            e = self.device.find_element_by_xpath("//android.widget.TextView[@text='登录']", timeout=15)
            g_logger.info("位置：{}".format(e.location))
            self.device.click_by_xpath("//android.widget.TextView[@text='登录']", timeout=5, desc="点击登录按钮")
            time.sleep(2)
        except:
             return False
        return True

    def _mobile_sms_authentication(self, account):
        """
        短信验证码
        Args:
            account: 用户账号
        Returns:
            True: 进入成功
            False: 进入失败
        """
        manu = self.device.get_manufacturer()
        try:
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入您的手机号']", timeout=5).send_keys(account)
            # 移除日志
            self.device.adb.rm_ipecker_log_file()

            self.device.click_by_xpath("//android.widget.TextView[@text='获取短信验证码']", timeout=10, desc="点击获取短信验证码按钮")
            time.sleep(2)
            try:
                self.device.click_by_xpath("//android.widget.Button[@text='上行短信验证']", timeout=5)
                return self._sms_up_authentication()
            except:
                pass

            # 切换到android输入法
            if manu == 'google':
                self.device.adb.adb_shell('ime set com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME')
            else:
                self.device.adb.adb_shell('ime set com.android.inputmethod.latin/.LatinIME')

            data_list = self._get_sms_from_ipecker_log()

            ret = False
            for data in data_list:
                g_logger.info("读取到的短信验证码为：{}".format(data))
                try:
                    self.device.find_element_by_xpath("//android.widget.EditText", timeout=10).send_keys(data)
                    time.sleep(3)

                    if manu in ('vivo', 'google'):
                        if not self._cancel_finger_login():
                            # return False
                            pass
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=10)
                        ret = True
                        break
                    except:
                        g_logger.info("验证码错误")
                        return False
                except:
                    continue

            # 切回appium输入法
            self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
            return ret
        except:
            return False

    def _sms_up_authentication(self):
        """
        短信登录上行验证
        Returns:
            True: 验证登录成功， False: 失败
        """
        try:
            self.device.click_by_xpath("//android.widget.TextView[@text='立即发送短信']", desc='点击立即发送短信', timeout=10)
            time.sleep(1)
            self.device.click_by_id("com.android.mms:id/send_button_sms", desc="点击'发送'", timeout=10)
            time.sleep(3)
            self.device.click_by_xpath('//android.widget.ImageView[@content-desc="向上导航"]', desc="点击'向上导航'", timeout=10)
            time.sleep(5)
        except:
            g_logger.error("短信登录：上行验证失败")
            return False

        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=30)
        except:
            g_logger.info("短信登录：上行验证，确认返回界面'个人中心'失败")
            return False

        return True

    def _cancel_finger_login(self, timeout=10):
        """
        取消指纹快速登录
        Returns:
            True: 取消成功, False: 取消失败
        """
        g_logger.info("点掉指纹快速登录弹窗")
        try:
            self.device.click_by_xpath(self.conf.common_button.xpath_cancel, desc="点击取消", timeout=timeout)
            time.sleep(2)
            return True
        except:
            return False
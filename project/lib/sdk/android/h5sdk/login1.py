"""
File Name:      login1
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class H5sdk(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def gamecenter_search(self, game_text):
        """
        游戏中心页面搜索操作
        Args:
            game_text: 搜索游戏名称
        Returns:
            True: 搜索成功
            False: 搜索失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        time.sleep(3)
        try:
            # 切回appium输入法
            self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
            self.device.swipe(width / 2, height * 1 / 4, width / 2, height * 3 / 4)
            time.sleep(2)
            for i in range(5):
                try:
                    self.device.find_element_by_id('com.qiyi.gamecenter:id/navtitle_search_text_ly',timeout=5).click()
                    time.sleep(2)
                    self.device.find_element_by_id('com.qiyi.gamecenter:id/et_game_center_search_search').send_keys(game_text)
                    time.sleep(2)
                    self.device.hide_keyboard()
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_text),timeout=10)
                    break
                except  Exception as e:
                    pass
                    self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                    if i == 4:
                      return False
        except Exception as e:
            g_logger.info('search game：{} failed'.format( game_text))
            return False
        return True

    def into_gamedetail(self, game_text):
        """
        游戏中心-进入游戏详情界面
        Args:
            game_text: 进入的游戏名
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_text)).click()
        except:
            g_logger.info('into game：{} failed'.format(game_text))
            return False
        return True

    def into_h5game(self, game_text):
        """
        进入非棋牌游戏
        Args:
            game_text: 非棋牌游戏名称
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(6)
        try:
            self.device.find_element_by_id('com.qiyi.gamecenter:id/pv_game_state_prompt').click()

        except:
            g_logger.error('into h5 game failed:' + game_text)
            return False
        return True

    def guest_login(self,game_text):
        """
        游客登录
        Args:
            game_text: 游戏名称
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        g_logger.info('guest login start:' + game_text)
        try:
            self.device.find_element_by_id("tourist", timeout=3).click()
            time.sleep(3)
            self.device.find_element_by_id('sidebar', timeout=3)
            g_logger.info('guest login success:' + game_text)
        except:
            g_logger.error('guest login failed:' + game_text)
            return False
        return True

    def mycount(self,phone,base_password):
        """ 从游戏中心点击密码登录
        Args:
            phone: 基线游戏手机账号
            base_password：基线密码
        Returns:
            True：密码登录成功
            False：密码登录失败
        """
        time.sleep(2)
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            for i in range(5):
                try:
                    self.device.find_element_by_xpath(self.conf.myaccount.xpath, timeout=5).click()
                    time.sleep(2)
                    break
                except:
                    try:
                        self.device.find_element_by_id(self.conf.base_upgrade_close.id, timeout=5).click()
                        time.sleep(1)
                        continue
                    except:
                        pass
                    if i == 4:
                        return False
            try:
                time.sleep(5)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='登录']", timeout=5).click()
                try:
                    self.device.find_element_by_xpath(self.conf.login_password_button.xpath, timeout=5).click()
                    self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入您的手机号']", timeout=5).set_text(phone)
                    time.sleep(3)
                    self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写密码']", timeout=5).set_text(base_password)
                    time.sleep(3)
                    self.device.find_element_by_id(self.conf.password_login.id, timeout=5).click()
                    time.sleep(2)
                    self.device.find_element_by_id('com.qiyi.video:id/navi0', timeout=5).click()
                except Exception as e:
                    g_logger.error('账号或密码错误')
            except:
                 g_logger.info("用户已登录")
                 self.device.find_element_by_xpath(self.conf.home.xpath, timeout=5).click()
        except  Exception as e:
            return False
        return True

    def into_game_center(self):
        """从推荐页面中基线进入游戏中心

         Returns:
            True: 进入成功
            False：进入失败
        """

        time.sleep(5)
        for i in range(6):
            try:
                # self.device.find_element_by_id('com.qiyi.video:id/navi0', timeout=5).click()
                time.sleep(5)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']", timeout=5).click()
                self.device.find_element_by_xpath("//android.widget.TextView[@text='新游']", timeout=5)
                time.sleep(2)
                g_logger.info("进入游戏中心成功")
                break
            except  Exception as e:
                g_logger.info(str(e))
                # 升级提示
                try:
                    self.device.find_element_by_id(self.conf.base_upgrade_close.id, timeout=3).click()
                    time.sleep(1)
                except:
                    pass
                    if i == 5:
                        g_logger.info("进入游戏中心失败")
                        self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
                                                                        "into_gamecenter_{}_failed.png".format(
                                                                            g_resource['testcase_loop'])))
                        return False
            time.sleep(2)
            # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
        return True

    def account_display(self,account_display,game_account,game_password):
        """
        侧边栏-账号显示
        Args:
            account_display: 领取礼包界面按钮显示
            game_account：普通登陆账号
            game_password:普通登录密码
        Returns:
            True：账号显示成功
            False：账号显示失败
        """
        time.sleep(5)
        for i in range(5):
            try:
                self.device.find_element_by_id('sidebar', timeout=5).click()
                time.sleep(1)
                self.device.find_element_by_id(self.conf.sidebar_account.id, timeout=5).click()
                time.sleep(6)
                self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(account_display), timeout=5)
                break
            except  Exception as e:
                if i == 4:
                    return False
                self.other_login()
                self.password_login(game_account,game_password)
                self.phone_return()
                self.device.find_element_by_id('com.qiyi.gamecenter:id/pv_game_state_prompt').click()
                continue

                #再次进入

            # try:
            #     self.device.find_element_by_id(self.conf.sidebar_account.id, timeout=5).click()
            #     time.sleep(3)
            #     self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(account_display),timeout=5)
            #     break
            # except  Exception as e:
            #     pass
            #     if i == 4:
            #         return False
            #  return True

    def phone_return(self):
        """
        物理返回
        Returns:
            True：退出游戏成功
            False：退出游戏失败
        """
        time.sleep(10)
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(1)
            self.device.find_element_by_id('exit_game_sure', timeout=5).click()
            time.sleep(2)
        except  Exception as e:
            return False
        return True

    def sms_login(self,phone_num):
        """
        短信登录
        Args:
            phone_num: 手机号
        Returns:
            True：登录成功
            False：登录失败
        """
        time.sleep(6)
        try:
            # 手机号
            try:
                self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入手机号码']", timeout=10).set_text(phone_num)
                #self.device.find_element_by_id(self.conf.login_sms.id, timeout=5).set_text(phone_num)
            except Exception as e:
                pass

            # 移除日志
            self._rm_ipecker_log()

            try:
                self.device.find_element_by_id('get_sms').click()
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
                    self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入短信验证码']", timeout=5).set_text(data)

                except Exception as e:
                    continue

            # 确认
            try:
                # 进入游戏
                self.device.find_element_by_id('regist_btn').click()
                self.device.find_element_by_id('sidebar', timeout=3)
                g_logger.info('Sms login success')
                time.sleep(2)
            except Exception as e:
                g_logger.error('Sms login failed:' )
                # 切回appium输入法
            self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
                # 切回搜狗输入法
            self.device.adb.adb_shell('ime list -s')
            time.sleep(2)
            self.device.adb.adb_shell('ime set com.sohu.inputmethod.sogou.xiaomi/.SogouIME')
            return ret
        except  Exception as e:
            return False

    def other_login(self):
        """
        点击其他登录方式进行账号登录
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(5)
        for i in range(10):
            try:
                time.sleep(3)
                self.device.find_element_by_id('normal_login_btn', timeout=3).click()
                break
            except  Exception as e:
                if i == 9:
                    return False
                time.sleep(1)
            continue
        try:
            self.device.find_element_by_id('login_btn', timeout=5)
        except:
            return False
        return True

    def password_login(self, game_account, game_password):
        """
        账号密码登录/普通中文账号登录
        Args:
            receive: 领取礼包界面按钮显示
            receive_look：领取礼包界面查看按钮显示
         Args:
         account: 账号
         password11：密码
        Returns:
            True：登录成功
            False：登录失败
        """
        time.sleep(3)
        try:
            self.device.find_element_by_id('login_btn', timeout=5)
            self.device.find_element_by_id('user_name_login', timeout=5).set_text(game_account)
            time.sleep(1)
            self.device.find_element_by_id('user_pswd_login', timeout=5).set_text(game_password)
            time.sleep(2)
            self.device.find_element_by_id('login_btn', timeout=5).click()
            time.sleep(5)
            self.device.find_element_by_id('sidebar', timeout=5)
        except  Exception as e:
            g_logger.info("账号密码登陆失败")
        return True





    def alipay_login(self):
        """
        点击支付宝图标进行登录-进入扫码登录页面
        Returns:
            True：进入成功
            False：进入失败
        """
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.tap([(650, 1490)], duration=1, timeout=5)
            # self.device.find_element_by_xpath(self.conf.login_ali_button.xpath, timeout=5).click()
        except  Exception as e:
            return False
        return True

    def xm_login(self,xmi_account,xmi_password):
        """
        点击小米图标进行登录
        Args:
            xmi_account: 小米账号
            xmi_password：小米密码
        Returns:
            True：进入成功
            False：进入失败
        """
        try:

            self.device.find_element_by_xpath(self.conf.login_xiaomi_button.xpath, timeout=5).click()
            self.device.find_element_by_xpath(self.conf.xiaomi_interface.xpath, timeout=5).click()
            g_logger.info("进入小米登录页面")
            self.device.find_element_by_xpath(self.conf.xiaomi_account.xpath, timeout=5).set_text(xmi_account)
            self.device.find_element_by_xpath(self.conf.xiaomi_password.xpath, timeout=5).set_text(xmi_password)
            self.device.find_element_by_xpath(self.conf.xiaomi_login1.xpath, timeout=5).click()
            self.device.find_element_by_xpath(self.conf.sidebar.xpath, timeout=5)
            g_logger.info('Xiaomi login success')
        except  Exception as e:
            g_logger.error('Xiaomi login failed:')
        return True
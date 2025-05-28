"""
File Name:      h5sdk
Author:         xuxiaofang_sx
Create Date:    2018/8/9
"""
"""
File Name:      sdk.h5
Author:         xuxiaofang_sx
Create Date:    2018/8/7
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

    def no_cache(self):
        """
        清除缓存
        Returns:
            True: 清除成功
            False：清除失败
        """
        # self.device.test()
        time.sleep(2)
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        time.sleep(3)
        self.device.adb.clear_app_data("com.qiyi.video")
        time.sleep(3)
        self.device.launch_app()
        # self.device.find_element_by_id('android:id/button1', timeout=5).click()

        try:
            self.device.click_by_id('com.qiyi.video:id/a0_', timeout=5,desc="用户协议与隐私同意并继续")
            time.sleep(5)
            self.device.find_element_by_id('com.qiyi.video:id/navi0', timeout=5).click()
            g_logger.info('11')
            self.device.swipe(width / 2, height * 1 / 4, width / 2, height * 3 / 4)
            time.sleep(6)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']", timeout=5).click()
            g_logger.info('22')
            time.sleep(6)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='点击进入']", timeout=5).click()
            g_logger.info('33')
            time.sleep(30)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']", timeout=3)
        except Exception as e:
            g_logger.error('clear cache fail ')
            return False
        return True

    def into_mygame_page(self, title):
        """ 从游戏中心首页进入我的小游戏页
        Args:
         title: 页面标题
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(2)
        try:

            self.device.find_element_by_id(self.conf.into_mygame_page.id, timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
            g_logger.info("进入爱奇艺H5页面成功")
        except Exception as e:
            g_logger.error('进入爱奇艺H5页面失败')
            return False
        return True

    def into_game(self):
        """
        从图标进入游戏

        Returns:
            True：进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.non_cheese_game_icon.xpath, timeout=5).click()

        except  Exception as e:
            return False
        return True

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

    def gift(self, gift_text):
        """ 点击侧边栏进入领取礼包页面
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

    def share(self, title1):
        """
        点击侧边栏进行分享
        Args:
            title1: QQ分享页面元素
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

    def qq_share(self, qq_account, qq_password):
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
                self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="请输入QQ号码或手机或邮箱"]',
                                                  timeout=5).set_text(qq_account)
                self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="密码 安全"]',
                                                  timeout=5).set_text(qq_password)
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

    def qqzone_share(self, qq_account, qq_password):
        """
        QQ空间分享-qq已经登录
        Args:
            receive: 领取礼包界面按钮显示
            receive_look：领取礼包界面查看按钮显示
        Returns:
            True：分享成功
            False：分享失败
        """
        try:
            self.device.find_element_by_id(self.conf.qq_zone_public.id, timeout=5).click()
            time.sleep(2)
        except  Exception as e:
            self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="请输入QQ号码或手机或邮箱"]',
                                              timeout=5).set_text(qq_account)
            self.device.find_element_by_xpath('//android.widget.EditText[@content-desc="密码 安全"]', timeout=5).set_text(
                qq_password)
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
            self.device.find_element_by_xpath(self.conf.sina_send.xpath, timeout=5).click()
            time.sleep(2)
        except  Exception as e:
            self.device.click_by_id('android:id/button1', timeout=5, desc="允许爱奇艺开启微博")
            self.device.find_element_by_xpath(self.conf.sina_send.xpath, timeout=5).click()
        return True

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
        except  Exception as e:
            g_logger.info("该账号身份认证过")
        return True

    def gamecenter_search(self, game_text):
        """
        游戏中心页面搜索操作
        Args:
            game_text: 搜索文本
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
                    self.device.find_element_by_id('com.qiyi.gamecenter:id/common_title_center_search', timeout=5).click()
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
            g_logger.info('search game：{} failed'.format(game_text))
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

    def guest_login(self, game_text):
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

    def mycount(self, phone, base_password):
        """ 从游戏中心点击密码登录
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
                    self.device.click_by_xpath(self.conf.myaccount.xpath, timeout=5,desc="我的按钮")
                    time.sleep(2)
                    break
                except:
                    try:
                        self.device.find_element_by_id(self.conf.base_upgrade_close.id, timeout=5).click()
                        time.sleep(1)
                        continue
                    except:
                        time.sleep(1)
                        self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                        pass
                    if i == 4:
                        return False
            try:
                time.sleep(5)
                self.device.click_by_xpath("//android.widget.TextView[@text='登录']", timeout=5,desc="登录按钮")
                try:
                    self.device.click_by_xpath(self.conf.login_password_button.xpath, timeout=5,desc="密码登录按钮")
                    self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入您的手机号']",timeout=5).set_text(phone)
                    time.sleep(3)
                    self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写密码']", timeout=5).set_text(base_password)
                    time.sleep(3)
                    self.device.click_by_id(self.conf.password_login.id, timeout=5,desc="登录按钮")
                    time.sleep(2)
                    self.device.find_element_by_id('com.qiyi.video:id/navi0', timeout=5).click()
                except Exception as e:
                    g_logger.error('账号或密码错误')
            except:
                g_logger.info("用户已登录")
                self.device.click_by_xpath(self.conf.home.xpath, timeout=5,desc="推荐按钮")
        except  Exception as e:
            return False
        return True

    def into_game_center(self):
        """从推荐页面中基线进入游戏中心
         Returns:
            True: 进入成功
            False：进入失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        time.sleep(5)
        for i in range(6):
            try:
                # self.device.find_element_by_id('com.qiyi.video:id/navi0', timeout=5).click()
                time.sleep(5)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']", timeout=5).click()
                self.device.swipe(width / 2, height * 1 / 4, width / 2, height * 3 / 4)
                time.sleep(1)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='新游']", timeout=5)
                time.sleep(2)
                g_logger.info("进入游戏中心成功")
                break
            except Exception as e:
                g_logger.info(str(e))
                # 升级提示
                try:
                    self.device.find_element_by_id(self.conf.base_upgrade_close.id, timeout=3).click()
                    time.sleep(1)
                except:
                    pass
                    if i == 5:
                        g_logger.info("进入游戏中心失败")
                        self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'],
                                                                        "into_gamecenter_{}_failed.png".format(
                                                                            g_resource['testcase_loop'])))
                        return False
            time.sleep(2)
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
        return True

    def account_display(self, account_display, game_account, game_password):
        """
        账号显示
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
                self.device.click_by_id('sidebar', timeout=5,desc="侧边栏按钮")
                time.sleep(1)
                self.device.click_by_id(self.conf.sidebar_account.id, timeout=5,desc="用户按钮")
                time.sleep(6)
            except  Exception as e:
                return False
            try:
                self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(account_display),timeout=5)
                break
            except  Exception as e:
                if i == 4:
                    return False
                self.other_login()
                self.password_login(game_account, game_password)
                self.phone_return()
                self.device.find_element_by_id('com.qiyi.gamecenter:id/pv_game_state_prompt').click()
                continue
        return True
                # 再次进入

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
            self.device.click_by_xpath('//android.view.View[@content-desc="退出游戏"]', timeout=5)
            time.sleep(2)
        except  Exception as e:
            return False
        return True

    def sms_login(self, phone_num):
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
                self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入手机号码']", timeout=10).set_text(
                    phone_num)
                # self.device.find_element_by_id(self.conf.login_sms.id, timeout=5).set_text(phone_num)
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
                    self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入短信验证码']",
                                                      timeout=5).set_text(data)

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
                g_logger.error('Sms login failed:')
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
        try:
            time.sleep(3)
            self.device.find_element_by_id('change-account', timeout=3).click()
        except  Exception as e:
            self.device.click_by_id('normal_login_btn', timeout=5, desc="其他登录方式按钮")
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

    def xm_login(self, xmi_account, xmi_password):
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

    def sidebar(self, is_tourist, is_sms, phone_num):
        """
        点击侧边栏切换账号成功
        Args:
            is_tourist: 游客登录开关
            is_sms：短信登录开关
            phone_num：手机号
        Returns:
            True：进入成功
            False：进入失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        time.sleep(3)
        for i in range(5):
            try:
                self.device.swipe(width / 2, height * 1 / 4, width / 2, height * 3 / 4)
                time.sleep(1)
                self.device.find_element_by_id('sidebar', timeout=5).click()
                time.sleep(2)
                break
            except  Exception as e:

                if i == 4:
                    return False
                continue
        # 进入侧边栏
        try:
            time.sleep(2)
            self.device.find_element_by_id(self.conf.sidebar_account.id, timeout=5).click()
            self.device.find_element_by_id(self.conf.switch_account.id, timeout=5).click()
            if is_tourist == 'TRUE':
                return self.tourist_login()
            elif is_sms == 'TRUE':
                return self.sms_login(phone_num)
            else:
                for i in range(30):
                    try:
                        self.device.find_element_by_id('normal_login_btn', timeout=5).click()
                        time.sleep(2)
                        self.device.find_element_by_id('login_btn', timeout=5)
                        break
                    except  Exception as e:
                        if i == 29:
                            return False
                        continue
        except:
            try:
                time.sleep(2)
                self.device.find_element_by_id('normal_login_btn', timeout=5).click()
                self.device.find_element_by_id('login_btn', timeout=5)
            except:
                return False
            return False
        return True

    def qq_login(self):
        """
        点击qq图标进行登录
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(2)
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(3)
            self.device.tap([(200, 1490)], duration=1, timeout=5)
            # self.device.find_element_by_xpath(self.conf.into_qq_login_page.xpath, timeout=5).click()
            # self.device.find_element_by_xpath(self.conf.qq_one_login1.xpath, timeout=5).click()
            # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
        except  Exception as e:
            return False
        return True

    def tourist_login(self):
        """
        游客登录
        Returns:
            True：进入成功
            False：进入失败
        """
        try:

            self.device.find_element_by_id(self.conf.tourist.id, timeout=5).click()
        except:
            return False
        return True

    def sina_login(self, sina_account, sina_password):
        """
        点击sina图标进行登录
        Args:
            sina_account: 新浪账号
            sina_password：新浪密码
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(2)
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_xpath('//android.view.View[@content-desc="新浪微博账号登录"]', timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_xpath(self.conf.sina_interface.xpath, timeout=5)
            g_logger.info("进入微博登录页面")
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请用微博帐号登录']", timeout=5).set_text(
                sina_account)
            time.sleep(3)
            self.device.find_element_by_id('passwd', timeout=5).send_keys(sina_password)
            self.device.find_element_by_xpath(self.conf.sina_login_button.xpath, timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_id('sidebar', timeout=5)
            g_logger.info('sina login success')
        except  Exception as e:
            g_logger.error('sina login failed:')
        return True



    def coin(self):
        """
        从小游戏页进入游戏
        Returns:
            True：进入成功
            False：进入失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        time.sleep(1)
        try:
            self.device.swipe(width / 2, height * 1 / 4, width / 2, height * 3 / 4)
            time.sleep(1)
            self.device.tap([(300, 400)], duration=1, timeout=3)
            # self.device.find_element_by_xpath(self.conf.small_game.xpath, timeout=5).click()
            try:
                time.sleep(2)
                self.device.find_element_by_xpath(self.conf.notice1.xpath, timeout=5)
                self.device.find_element_by_xpath(self.conf.return1.xpath, timeout=5).click()
                g_logger.info("进入小游戏成功")
            except  Exception as e:
                pass
        except  Exception as e:
            g_logger.info("进入小游戏失败")
            pass
        return True
















    def sidebar_tourists(self):
        """
        侧边栏游客
        Returns:
            True：登陆成功
            False：登陆失败
        """
        try:
            time.sleep(5)
            self.device.find_element_by_id('sidebar', timeout=5).click()
            self.device.find_element_by_id(self.conf.sidebar_account.id, timeout=5).click()
            self.device.find_element_by_id(self.conf.switch_account.id, timeout=5).click()
            time.sleep(2)
            self.device.find_element_by_id(self.conf.tourist.id, timeout=5).click()
        except  Exception as e:
            return False
        return True












    def other_display(self):
        """
        其他登录页面显示
        Returns:
            True：账号显示成功
            False：账号显示失败
        """
        try:
            self.device.find_element_by_xpath("//android.view.View[@content-desc='其他登录方式']", timeout=5).click()
            self.device.find_element_by_xpath("//android.view.View[@content-desc='客服']", timeout=5)
            time.sleep(2)
        except  Exception as e:
            return False
        return True

    def wechat_login(self, title,account, password):
        """
        进入游戏中心-h5-微信登录
        Args:
            account: 微信账号
            password：微信密码
        Returns:
            True: 微信登录成功
            False：微信登陆失败
        """
        try:

            self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写微信号/QQ号/邮箱']",timeout=5).send_keys(account)
            time.sleep(3)
            self.device.find_element_by_xpath("//android.widget.EditText[@text='请填写密码']", timeout=5).set_text(password)
            time.sleep(3)
            self.device.find_element_by_id(self.conf.pay_wechat_login.id, timeout=5).click()
            time.sleep(6)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            time.sleep(3)
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_id(self.conf.pay_wechat_one_click_login.id, timeout=5).click()
            time.sleep(3)
            #self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']")
            # self.device.find_element_by_xpath(self.conf.pay_wechat_one_click_login_Password.xpath, timeout=5).set_text(pay_password)
            # time.sleep(5)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
            # time.sleep(2)
            #self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺游戏充值']")
            #time.sleep(3)
            #self.device.find_element_by_id(self.conf.into_pay_wechat_login.id, timeout=5).click()
        except  Exception as e:
            return False
        return True
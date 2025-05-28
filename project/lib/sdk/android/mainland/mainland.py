"""
File Name:      mainland
Author:         xuxiaofang_sx
Create Date:    2018/7/11
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class  Mainland(Android):
    def __init__(self, target, ele_conf_name='android_sdk'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.target = target
        self.data = target.data
        self.device = target.device

    def test(self):
        """
        daluDemo测试接口
        """
        # self.device.test()
        g_logger.info("Demoapk test")

    def no_cache(self):
        """
                清除缓存
                Returns:
                    True: 清除成功
                    False：清除失败
                """
        # self.device.test()

        self.device.adb.clear_app_data("com.iqiyigame.sdk.demo")
        time.sleep(3)
        self.device.launch_app()
        # self.device.find_element_by_id('android:id/button1', timeout=5).click()

    def login(self):
        """
        进入游戏-登录界面
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        try:
            self.device.click_by_id(self.conf.base_Login.id, timeout=5,desc="点击基线登录")
            time.sleep(2)
            try:
                try:
                    # self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
                    # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                    time.sleep(3)
                    self.device.click_by_id('com.iqiyigame.sdk.demo:id/game_init_qqlogin', timeout=5)
                except Exception as e:
                    try:
                        # self.device.background_app(1, timeout=3)
                        self.device.click_by_xpath('//android.widget.TextView[@text="通知"]', timeout=5,desc="手机实名认证显示")
                        time.sleep(2)
                        self.device.click_by_id(self.conf.mobile_authentication_close.id, timeout=5,desc="点击关闭手机实名认证")
                        time.sleep(2)
                        self.device.click_by_id(self.conf.init_wetchat.id, timeout=5,desc="点击初始化微信登录")
                    except:
                        try:
                            time.sleep(2)
                            self.device.click_by_xpath('//android.widget.TextView[@text="安全实名认证"]', timeout=5,desc="身份实名认证显示")
                            time.sleep(2)
                            self.device.click_by_id(self.conf.mobile_authentication_interface_close.id, timeout=5,desc="点击关闭身份实名认证窗口")
                        except:
                            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            except Exception as e:
                return False
        except Exception as e:
            return False
        return True

    def nomobileauthentication_confirm(self):
        """
        判断是否进行过手机验证
        Returns:
            True: 手机验证
            False：进入游戏失败
        """
        try:
            #self.device.background_app(1, timeout=3)
            self.device.find_element_by_xpath('//android.widget.TextView[@text="通知"]', timeout=5)
            self.device.click_by_id(self.conf.mobile_authentication_close.id, timeout=5,desc="关闭手机实名认证页面")
            self.device.click_by_id(self.conf.init_wetchat.id, timeout=5,desc="点击初始化微信登录")
        except:
            pass
        return True

    def nomobileauthentication(self):
        """
        进入游戏-登录界面-实名认证页面
        Returns:
            True: 进入游戏成功
            False：进入游戏失败
        """
        try:
            self.device.click_by_id(self.conf.base_Login.id, timeout=5,desc="点击登录")
            try:
                self.device.find_element_by_xpath('//android.widget.TextView[@text="安全实名认证"]', timeout=5)
                self.device.click_by_id(self.conf.mobile_authentication_interface_close.id, timeout=5,desc="关闭手机实名认证页面")

            except Exception as e:
                pass
            # self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            #self.device.find_element_by_id(self.conf.back1.id, timeout=5).click()
            #time.sleep(5)
            self.device.find_element_by_xpath("//android.widget.Button[@text='立即验证']", timeout=5)
            self.device.click_by_id(self.conf.mobile_authentication_interface_close.id, timeout=5, desc="关闭手机实名认证页面")
            self.device.click_by_id(self.conf.init_wetchat.id, timeout=5, desc="点击初始化微信登录")
        except:
            return False
        return True

    def No_login(self,title):
        """
        进入游戏-手机注册登录界面
        Args:
            game_text: 登录界面
        Returns:
            True: 显示成功
            False：显示失败
        """
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(5)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
        except:
            return False
        return True

    def  NoMobile_login(self,title):
        """
        进入游戏-登录-爱奇艺登录页面
        Args:
            game_text: 登录界面
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
            time.sleep(5)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
            time.sleep(2)

        except Exception as e:
            return False
        return True

    def manual_login(self,account,password):

        try:
            self.device.tap([(120, 159)], duration=1, timeout=5)
            time.sleep(5)
            self.device.find_element_by_id(self.conf.into_logout.id, timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_id(self.conf.logout.id, timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_id(self.conf.other_log.id, timeout=5).click()
            time.sleep(3)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(account), timeout=5)
            time.sleep(3)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(password), timeout=5)
            time.sleep(3)
            self.device.find_element_by_id(self.conf.other_log_into_game.id, timeout=5).click()
            time.sleep(3)
        except:
            return False
        return True

    def account_password_login2(self,account,password):
        """
        进入游戏-侧边栏-其他登录方式—账号密码登录
        Args:
            game_text: 登录界面
        Returns:
            True: 自动登录账号显示正常
            False：自动登录失败
        """
        try:

            self.device.find_element_by_id(self.conf.old_user.id, timeout=5).set_text(account)
            self.device.find_element_by_id(self.conf.old_user_password.id, timeout=5).set_text(password)
            time.sleep(3)
            self.device.find_element_by_id(self.conf.old_user_into.id, timeout=5).click()
            time.sleep(5)
            self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
        except  Exception as e:
            return False
        return True

    def third_login_sina(self,account,password):
        """
        进入游戏-侧边栏-其他登录方式—第三方登录登录
        Args:
           account: 登录账号
           password：登录密码
        Returns:
            True: 登录成功
            False：登录失败
        """
        try:
            self.device.click_by_id(self.conf.other_log.id, timeout=5,desc="点击其他登录按钮")
            time.sleep(3)
            self.device.click_by_id(self.conf.third_login_sina.id, timeout=5,desc="点击新浪图标")
            time.sleep(5)
            self.device.find_element_by_id(self.conf.third_login_sina_account.id, timeout=5).set_text(account)
            #self.device.background_app(1, timeout=3)
            self.device.find_element_by_id('passwd', timeout=10).set_text(password)
            time.sleep(3)
            self.device.click_by_xpath('//android.view.View[@text="登录"]',timeout=5,desc="点击登录按钮")
            time.sleep(3)
            try:
                self.device.find_element_by_xpath('//android.widget.TextView[@text="安全实名认证"]', timeout=5)
                self.device.click_by_id(self.conf.mobile_authentication_interface_close.id, timeout=5,desc="关闭手机实名认证界面")
            except Exception as e:
                pass
            return self.nomobileauthentication_confirm()
        except  Exception as e:
            return False

    def third_login_baidu(self, account, password):
        """
        进入游戏-侧边栏-其他登录方式—第三方登录登录
        Args:
            game_text: 登录界面
        Returns:
            True: 登录成功
            False：登录失败
        """
        try:

            self.device.find_element_by_id(self.conf.third_login_sina.id, timeout=5).click()
            time.sleep(5)
            self.device.find_element_by_id(self.conf.third_login_sina_account.id, timeout=5).set_text(account)
            self.device.find_element_by_xpath("//android.view.View[@text='请输入密码']", timeout=10).set_text(password)
            time.sleep(5)
            self.device.find_element_by_xpath("//android.view.View[@text='登录']").click()
            time.sleep(3)
        except  Exception as e:
            return False
        return True


    def no_qq_login(self,qq,qq_password):
        """
        qq未登录-账号密码登录
        Args:

        Returns:
            True: 登录成功
            False：登录失败
        """
        try:
            self.device.find_element_by_xpath("//android.view.View[@text='QQ号/手机号/邮箱']", timeout=10).set_text(qq)
            time.sleep(5)
            self.device.find_element_by_id(self.conf.qq_password.id, timeout=5).send_keys(qq_password)
            time.sleep(5)
            self.device.find_element_by_id(self.conf.enter_qq.id, timeout=5).click()
            time.sleep(5)
        except:
            return False
        return True


    def mobile_phone_return(self):
        """
        进入游戏-侧边栏-各个功能点入口
        Args:
            game_text:侧边栏
        Returns:
            True: 弹窗正常显示
            False：进入失败
        """
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(5)
            self.device.find_element_by_xpath("// android.widget.Button[@text='更多游戏']")
            time.sleep(5)
        except:
            return False
        return True
    def cancel_payment(self):
        """
        进入游戏-返回-放弃支付
        Args:
            game_text:侧边栏
        Returns:
            True: 放弃支付成功
            False：放弃支付失败失败
        """
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_id(self.conf.cancel_pay.id, timeout=5).click()
            time.sleep(5)

        except:
            return False
        return True

    def buy_vip_game(self):
        """
        选择什么方式开通会员

        """
        try:
            # self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            # self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            # self.device.find_element__by_xpath("//android.widget.TextView[@text='季卡']",timeout=4)
            self.device.find_element_by_xpath("//android.widget.Button[@text='开通']").click()
            self.device.find_element_by_xpath("//android.widget.TextView[@text='支付中心']",timeout=4)
        except Exception as e:
            return False
        return True
        # elif self.device.find_element__by_xpath("//android.widget.TextView[@text='月卡']"):
        #     self.device.open2_by_xpath(self.conf.open2_by_xpath, timeout=2).click()
        #     self.device.payment_center_by_xpath("//android.widget.TextView[@text='支付中心']", timeout=4)
        # elif self.device.find_element__by_xpath("//android.widget.TextView[@text='年卡']"):
        #     self.device.open3_by_xpath(self.conf.open3_by_xpath, timeout=2).click()
        #     self.device.payment_center_by_xpath("//android.widget.TextView[@text='支付中心']", timeout=4)



    def game_vip_page(self):
        """
    会员卡购买页面显示正常

        Returns:
            True: 显示正常
            False：显示失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        # 滑动查找购买游戏会员
        for i in range(10):

            try:
                self.device.find_element_by_xpath("//android.widget.Button[@text='购买游戏会员']", timeout=15).click()
                time.sleep(2)
                break
            except:
                if i == 9:
                    return False

                self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
                time.sleep(1)
                continue
        #正常打开会员卡购买页面
        try:

            self.device.find_element_by_xpath("//android.widget.TextView[@text='购买游戏会员']", timeout=5)
        except:
            return False
        return True

    def learn_vip_page(self):
    #进入游戏会员介绍页

        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='了解游戏会员']", timeout=5).click()
            self.device.find_element_by_xpath("//android.widget.TextView[@text='了解游戏会员']", timeout=5)
        except Exception as e:
            return False
        return True

    def open_vip(self):
        """
        游戏会员页面显示正常
        Returns:
            True: 显示正常
            False：显示失败
        """
        # 进入游戏会员介绍页

        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='了解游戏会员']", timeout=5).click()
            self.device.find_element_by_xpath("//android.widget.TextView[@text='了解游戏会员']", timeout=5)
        except Exception as e:
            return False
        return True





    def id_verified(self,user_name,id_card,is_identify):
        try:

            self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
            try:
                self.device.find_element_by_xpath('//android.widget.TextView[@text="安全实名认证"]', timeout=5)
                if is_identify == 'TRUE':
                    self.device.find_element_by_id(self.conf.base_login_authentication_name.id, timeout=5).set_text(
                        user_name)
                    self.device.find_element_by_id(self.conf.base_login_authentication_id.id, timeout=5).send_keys(
                        id_card)
                    self.device.find_element_by_id(self.conf.base_login_confirm.id, timeout=5).click()
                    self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
            except Exception as e:
                pass
        except Exception as e:
            return True
        return True


    def mobile_real_authentication(self,phone):
        try:
            self.device.find_element_by_id(self.conf.base_Login.id, timeout=5).click()
            self.device.background_app(1, timeout=3)
            # 立即验证
            self.device.find_element_by_id(self.conf.mobile_authentication.id, timeout=5).click()
        except Exception as e:
          return True

            # 手机号
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入您的手机号']", timeout=10).send_keys(phone)
            self.device.find_element_by_id(self.conf.mobile_phone.id, timeout=5).set_text(phone)
        except Exception as e:
            pass


        # 移除日志
        self._rm_ipecker_log()
        try:
            self.device.find_element_by_id(self.conf.get_verify_code.id, timeout=10).click()
            # self.device.find_element_by_xpath("//android.widget.Button[@text='获取短信验证码']", timeout=10).click()
            time.sleep(1)
        except:
            pass
        # 切换到android输入法
        self.device.adb.adb_shell('ime set com.android.inputmethod.latin/.LatinIME')

        ret = False
        data_list = self._get_sms_from_ipecker_log()
        for data in data_list:
            g_logger.info(data)
            try:
                # for i, char in enumerate(data):
                #     id_n = "com.qiyi.video:id/enter_pwd_block%d" % (i + i)
                #     self.device.find_element_by_id(id_n).send_keys(char)
                id_e = 'com.iqiyigame.sdk:id/game_verify_code_edit_text'
                self.device.find_element_by_id(id_e).send_keys(data)
            except Exception as e:
                continue
        # 确认
        try:
            # 立即验证
            self.device.find_element_by_id(self.conf.verify_code_ok.id, timeout=5).click()
        except Exception as e:
            pass
        # 切回appium输入法
        self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
        return ret

    def Coin_DiscountWechatPay(self,num,name):
         """
        微信金币优惠支付方式
         Args:
             num:充值金额
             name:
         Returns:
            True: 进入成功
            False：进入失败
        """
         try:
             # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
             self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)

             self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
             time.sleep(5)
             self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
             self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")

             try :
                 self.device.find_element_by_xpath("//android.widget.TextView[@text='金币抵扣']", timeout=5)
                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(name), timeout=5)
                 time.sleep(2)
                 self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
                 time.sleep(2)
                 return True
             except:
                 self.device.find_element_by_xpath("//android.widget.TextView[@text='我的优惠']").click()
                 time.sleep(5)
                 self.device.find_element_by_id(self.conf.my_discount_coin_button.id, timeout=5).click()
                 time.sleep(5)
                 self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(name),timeout=5).click()
                 time.sleep(2)
                 self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
                 time.sleep(2)
         except:
             return False
         return True

    def Voucher_DiscountWechatPay(self, num, name):
        """
       微信代金券优惠支付方式
        Args:
            num:充值金额，
       """
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
            self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)

            self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
            time.sleep(5)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='代金券']", timeout=5)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(name), timeout=5).click()
                time.sleep(2)
                self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
                time.sleep(2)
                return True
            except:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='我的优惠']").click()
                time.sleep(5)
                self.device.find_element_by_id(self.conf.my_discount_coin_interface2.id, timeout=5).click()
                time.sleep(5)
                self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(name),timeout=5).click()
                time.sleep(2)
                self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
                time.sleep(2)
        except:
            return False
        return True



    def DiscountAliPay(self, num):
        """
       支付方式
        Args:
            num:充值金额，
        """

        # 支付宝优惠支付
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
            self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)
            self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
            time.sleep(5)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='支付宝钱包']").click()
            time.sleep(2)
            self.device.find_element_by_id(self.conf.discount_payment_ali.id, timeout=5).click()
            self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
            time.sleep(2)
            # self.device.find_element_by_id(self.conf.alipay_switch.id, timeout=5).click()
            # time.sleep(2)
            #self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入登录密码']", timeout=5)
            # self.device.find_element_by_xpath("//android.widget.Button[@text='手机号/邮箱/淘宝会员名']",timeout=5)
        except:
            return False
        return True

    def DiscountWechatPay(self, num):
        """
       支付方式
        Args:
            num:充值金额
        Return:
            True:
            False:
        """

        # 微信优惠支付
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
            self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)

            self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
            time.sleep(5)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='微信支付']").click()
            time.sleep(2)
            self.device.find_element_by_id(self.conf.discount_payment_ali.id, timeout=5).click()
            self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
            time.sleep(2)
            # self.device.find_element_by_id(self.conf.alipay_switch.id, timeout=5).click()
            # time.sleep(2)
            #self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入登录密码']", timeout=5)
            # self.device.find_element_by_xpath("//android.widget.Button[@text='手机号/邮箱/淘宝会员名']",timeout=5)
        except:
            return False
        return True









    def cancle_payment(self):
        """
       支付方式
        Args:
            num:充值金额，
        """

        # 微信支付
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
            self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)

            self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
            time.sleep(2)
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_id(self.conf.continue_pay.id, timeout=5).click()
            time.sleep(2)


        except:
            return False
        return True

    def pay_display(self, num,title,pay_select):
        """
       支付方式
        Args:
            num:充值金额
        Return:
            True:
            False:
        """

        # 微信支付
        try:
            # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入支付金额']", timeout=10).send_keys(num)
            self.device.find_element_by_id(self.conf.into_pay.id, timeout=5).set_text(num)

            self.device.find_element_by_id(self.conf.pay.id, timeout=5).click()
            time.sleep(2)
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            self.device.find_element_by_id(self.conf.continue_pay.id, timeout=5).click()
            time.sleep(2)
        except:
            return False
        return True

    def wechat_display(self,title):
        """ 用户退出登录
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_id(self.conf.confirm_payment.id, timeout=5).click()
            time.sleep(5)
            self.device.adb.adb_shell("input keyevent KEYCODE_MENU ")
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
            time.sleep(2)

        except:
            return False
        return True

    def base_login_out(self):
        """ 用户退出登录
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_id(self.conf.base_user.id, timeout=5).click()
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='登录']", timeout=5)
                g_logger.info("用户未登录")
            except:
                self.device.tap([(115, 350)])
                self.device.find_element_by_id(self.conf.base_user_login_setting.id, timeout=5).click()
                time.sleep(2)

                size = self.device.get_window_size()
                y = size.get('height')
                if y == 1794:
                    y_axis = self.conf.base_user_login_out_button.y_1794
                elif y == 2118:
                    y_axis = self.conf.base_user_login_out_button.y_2118
                else:
                    return False

                self.device.tap([(540, y_axis)])
                self.device.find_element_by_id(self.conf.base_user_login_out_tv_right.id, timeout=5).click()
                time.sleep(1)
                self.device.find_element_by_id(self.conf.base_user_login_back.id, timeout=5).click()
                self.device.find_element_by_id(self.conf.base_recommend.id, timeout=5).click()
                g_logger.info("退出登录")
        except:
            return False
        return True



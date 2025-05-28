# -*- coding: UTF-8 -*-

"""
File Name:      vippage
Author:         gufangmei_sx
Create Date:    2018/8/14
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.gamecenter.android.smoke.common import Common


class VipPage(Common):
    """VIP页类"""
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android')

        self.target = target
        self.data = target.data
        self.device = target.device

    def into_vip_page(self, entrance, title):
        """
        从游戏中心首页进入游戏会员页
        Args:
            entrance: 入口名
            title: 页面标题
        Returns:
            True：进入成功
            False：进入失败
        """
        try:
            time.sleep(5)
            self.device.click_by_xpath("//android.widget.TextView[@text='{}']".format(entrance), timeout=5, desc="点击游戏会员按钮")
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
        except:
            return False
        return True

    def click_carousel_map1(self, game_title):
        """
        游戏会员页-点击轮播图进入游戏详情页
        Args:
            game_title: 游戏标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            time.sleep(3)
            self.device.tap([(540, 445)])
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_title),
                                                  timeout=5)
                #self.device.find_element_by_xpath(self.conf.h5_detail_page.xpath, timeout=5)
                g_logger.info("成功进入H5活动页")
                return True
            except:
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_title),
                                                      timeout=5)
                    #self.device.find_element_by_xpath(self.conf.special_detail_page.xpath, timeout=5)
                    g_logger.info("成功进入专题详情页")
                    return True
                except:
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_title),
                                                          timeout=5)
                        g_logger.info("成功进入游戏详情页")
                        return True
                    except:
                        return False
        except:
            return False

    def click_carousel_map2(self, h5_title):
        """
        游戏会员页-点击轮播图进入H5页面
        Args:
            h5_title: H5标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            time.sleep(7)
            self.device.tap([(540, 445)])
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(h5_title),
                                                  timeout=5)
                # self.device.find_element_by_xpath(self.conf.h5_detail_page.xpath, timeout=5)
                g_logger.info("成功进入H5活动页")
                return True
            except:
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(h5_title),
                                                      timeout=5)
                    # self.device.find_element_by_xpath(self.conf.special_detail_page.xpath, timeout=5)
                    g_logger.info("成功进入专题详情页")
                    return True
                except:
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(h5_title),
                                                          timeout=5)
                        g_logger.info("成功进入游戏详情页")
                        return True
                    except:
                        return False
        except:
            return False

    def click_carousel_map3(self, special_title):
        """
        游戏会员页-点击轮播图进入专题页面
        Args:
            special_title: 专题标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            time.sleep(11)
            self.device.tap([(540, 445)])
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_title),
                                                  timeout=5)
                g_logger.info("成功进入H5活动页")
                return True
            except:
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_title),
                                                      timeout=5)
                    g_logger.info("成功进入专题详情页")
                    return True
                except:
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_title),
                                                          timeout=5)
                        g_logger.info("成功进入游戏详情页")
                        return True
                    except:
                        return False
        except:
            return False

    def click_open_icon(self):
        """
        点击开通按钮
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_xpath("//android.widget.TextView[@text='立即开通']", timeout=5, desc="点击立即开通")
            time.sleep(2)
        except:
            return False
        return True

    def click_1qibei_icon(self, order_confirm):
        """
        点击1奇贝图标
        Args:
            order_confirm: 页面标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_id(self.conf.gamecenter_game_1qibei.id, timeout=5, desc="点击1奇贝图标")
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(order_confirm))
        except:
            return False
        return True

    def click_pay_icon(self):
        """
        点击支付图标
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_id(self.conf.gamecenter_game_order_pay_button.id, timeout=5, desc="点击支付图标")
            time.sleep(5)
        except:
            return False
        return True

    def buy_vip_game(self, alipay_account, alipay_password, game_name):
        """
        开通会员，购买1奇贝游戏
        Args:
            alipay_account: 支付宝账号
            alipay_password: 支付宝密码
            game_name:游戏名
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            # self.device.tap([(949, 991)])
            self.device.tap([(540, 785)])
            time.sleep(2)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='支付']", timeout=5)
            self.device.tap([(540,1680)])
            self.device.tap([(540, 1400)])#待确认
            time.sleep(2)
            self.device.click_by_xpath("//android.widget.TextView[@text='确认付款']", timeout=5, desc="点击确认付款按钮")
            time.sleep(8)
            self.alipay_account_login(alipay_account, alipay_password)
            self.device.click_by_xpath(self.conf.gamecenter_game_pay_confirm.xpath, timeout=5, desc="点击确认按钮")
            #self.device.find_element_by_xpath(self.conf.gamecenter_game_input_password.xpath, timeout=5).set_text('')
            self.device.find_element_by_xpath(self.conf.gamecenter_game_pay_success.xpath, timeout=5)
            self.device.click_by_xpath(self.conf.gamecenter_game_pay_done.xpath, timeout=5, desc="点击完成按钮")
            time.sleep(5)
            self.device.find_element_by_id(self.conf.gamecenter_game_purchase_success.id, timeout=5)
            self.device.click_by_id(self.conf.gamecenter_game_buy_game.id, timeout=5, desc="点击购买游戏按钮")
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='订单确认']", timeout=5)
            self.device.click_by_id(self.conf.gamecenter_game_order_pay_button.id, timeout=5, desc="点击支付按钮")
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
        except:
            return False
        return True

    def alipay_account_login(self, alipay_account, alipay_password):
        """
        支付宝账号登录
        Args:
            alipay_account: 支付宝账号
            alipay_password: 支付宝密码
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_xpath("//android.widget.Button[@text='确认付款']", timeout=30)
            self.device.screen_tap(self.conf.gamecenter_alipay_account)
            time.sleep(3)
            self.device.screen_tap(self.conf.gamecenter_alipay_other_account)
            time.sleep(3)
        except Exception as e:
            pass
        self.device.click_by_xpath("//android.view.View[@text='支付宝账户登录']", timeout=5, desc="点击支付宝账户登录按钮")
        time.sleep(6)
        self.device.find_element_by_id(self.conf.gamecenter_alipay_account1.id, timeout=5).send_keys(alipay_account)
        self.device.find_element_by_id(self.conf.gamecenter_alipay_password1.id, timeout=5).send_keys(alipay_password)
        self.device.click_by_xpath("//android.widget.Button[@text='下一步']", timeout=5, desc="点击下一步按钮")
        time.sleep(3)

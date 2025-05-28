# -*- coding: UTF-8 -*-

"""
File Name:      demo
Author:         zhangwei04
Create Date:    2018/3/5
"""
import os
import time
from framework.core.resource import g_resource
from framework.logger.logger import g_logger
from project.lib.ios import IOS


class Demo(IOS):
    def __init__(self, target):
        super().__init__(target=target)
        self.target = target
        self.data = target.data
        self.device = target.device

    def into_gamecenter(self):
        for i in range(3):
            try:
                start_time = time.time()
                self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="推荐"]').click()
                # self.device.find_element_by_id('推荐').click()
                print("runtime:", time.time() - start_time)
                self.device.find_element_by_id('游戏中心').click()
                # self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="游戏中心”]').click()
                time.sleep(2)
                return True
            except Exception as e:
                if i == 2:
                    return False
                time.sleep(2)

    def into_user_info(self):
        try:
            g_logger.info('into user info')
            time.sleep(4)
            # tuijian = self.device.find_element_by_id('推荐')
            wode = self.device.find_element_by_id('我的')
            wode.click()
            # wode1= self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="我的”]')
            # self.device.find_element_by_id(' 我的').click()
            time.sleep(2)
            g_logger.info('user info end')
            return True
        except Exception as e:
            return False

    def login_passwd(self, username, passwd):
        try:
            try:
                self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="登录"]', timeout=10).click()
                time.sleep(2)
            except:
                if self.logout():
                    self.device.find_element_by_xpath('//XCUIElementTypeImage[@name="QPNavBackGreen"]').click()
                    time.sleep(1)
                self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="登录"]', timeout=10).click()
                time.sleep(2)

            try:
                self.device.find_element_by_xpath('//XCUIElementTypeTextField[@name="手机号"]', timeout=5).set_value(username)
            except Exception as e:
                pass

            # 明文和密文密码id不一样
            try:
                self.device.find_element_by_xpath('//XCUIElementTypeTextField[@name="密码"]', timeout=5).set_value(passwd)
            except Exception as e:
                self.device.find_element_by_xpath('//XCUIElementTypeSecureTextField[@name="密码"]', timeout=5).set_value(passwd)

            self.device.find_element_by_xpath('(//XCUIElementTypeButton[@name="登录"])[2]').click()
            time.sleep(4)
        except Exception as e:
            g_logger.info(e)
            start = time.time()
            self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "login_passwd_faied.png"))
            g_logger.info("screen time: {}".format(time.time() - start))
            return False

        start = time.time()
        self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "login_passwd_faied.png"))
        g_logger.info("screen time: {}".format(time.time() - start))
        return True

    def logout(self):
        try:
            self.device.reset()
            time.sleep(4)
            g_logger.info('start logout')
            self.device.find_element_by_id('我的').click()
            time.sleep(2)

            for i in range(3):
                try:
                    self.device.find_element_by_xpath('//XCUIElementTypeApplication[@name="爱奇艺"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeButton[1]').click()
                    time.sleep(2)
                    break
                except:
                    time.sleep(2)
            else:
                return False

            # self.device.find_element_by_xpath('//XCUIElementTypeImage[@name="QPUserSetting_white”]').click()
            self.device.find_element_by_xpath('(// XCUIElementTypeStaticText[@name="设置"])[2]').click()
            time.sleep(2)
            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name=" 退出登录"]').click()
            time.sleep(2)
            for i in range(3):
                try:
                    self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="退出登录"]').click()
                    time.sleep(2)
                    break
                except Exception as e:
                    time.sleep(3)
            else:
                return False

            # 通过立即登录按钮来检测退出登录是否成功
            self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="立即登录"]')
            # for i in range(5):
            #     try:
            #         self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="立即登录"]')
            #         return True
            #     except Exception as e:
            #         time.sleep(2)
            # else:
            #     return False
        except Exception as e:
            return False
        g_logger.info('logout success')
        return True

    def into_gamecenter_user_info(self):
        for i in range(3):
            try:
                # self.device.find_element_by_xpath('//XCUIElementTypeOther[@name=" 我的"]').click()    # 找不到此元素
                elements = self.device.find_elements_by_id('我的')
                for ele in elements:
                    print(ele.rect)
                    print(ele.tag_name)
                time.sleep(2)
                return True
            except Exception as e:
                time.sleep(2)
        else:
            return False

    def gamecenter_login_passwd(self):
        try:
            g_logger.info("login with password")
            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="登录”]').click()
            time.sleep(2)
            self.device.find_element_by_xpath('(//XCUIElementTypeTextField[@name="密码"])[2]').set_value('feng122772')
            self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="登录"]').click()
        except Exception as e:
            return False
        return True

    def reset_app(self):
        try:
            self.device.reset()
            return True
        except Exception as e:
            return False

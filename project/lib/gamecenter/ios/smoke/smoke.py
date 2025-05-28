# -*- coding: UTF-8 -*-

"""
File Name:      smoke
Author:         gufangmei_sx
Create Date:    2018/7/27
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.ios import IOS
from project.script.testsuite.TestsuiteNormal import *
import aircv as ac

from appium.webdriver.common.touch_action import TouchAction

class Smoke(IOS):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='ios')

        self.target = target
        self.data = target.data
        self.device = target.device

    def test(self):
        """Smoke测试接口

        """
        # self.device.test()
        g_logger.info("Demoapk test")

    def reset_app(self):
        try:
            self.device.reset()
            return True
        except Exception as e:
            return False

    def click_box(self):
        self.device.tap([(170, 400)])

    def into_ios_game_center(self):
        """从推荐页面中基线进入游戏中心
         Returns:
           True: 进入成功
           False：进入失败
         """
        time.sleep(5)
        self.device.tap([(150, 296)])
        time.sleep(2)
        try:
            self.device.click_by_xpath("//XCUIElementTypeButton[@name='我的']", timeout=20, desc = "点击基线我的tab")
            time.sleep(3)

            self.device.driver.execute_script("mobile: swipe", {"direction": "up"})
            time.sleep(2)
            self.device.click_by_xpath('//XCUIElementTypeStaticText[@name="我的游戏"]', timeout=20, desc="点击我的游戏")
            time.sleep(8)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_我的棋牌游戏"]', timeout=10)
            self.device.click_by_xpath('//XCUIElementTypeOther[@name="推荐"]', timeout=20, desc="点击推荐tab")
            time.sleep(10)
            #self.device.background_app(1, timeout=3)
            #self.device.find_element_by_xpath(self.conf.base_home_page.xpath, timeout=20).click()
            # time.sleep(2)
            # self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="游戏中心"]', timeout=10).click()
            # time.sleep(2)

        except Exception as e:
            return False
        return True

    def base_game_center(self):
        """从推荐页面中进入游戏中心
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            self.device.click_by_xpath('//XCUIElementTypeOther[@name="推荐"]', timeout=20, desc="点击推荐tab")
            time.sleep(2)
            self.device.tap([(37,322)])
            time.sleep(4)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_游戏中心"]', timeout=10)

            #self.device.find_element_by_xpath(self.conf.base_home_page.xpath, timeout=20).click()
            # time.sleep(2)
            # self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="游戏中心"]', timeout=10).click()
            # time.sleep(2)

        except Exception as e:
            return False
        return True

    def base_more_game_center(self):
        """从推荐页面more进入游戏中心
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            self.device.click_by_xpath('//XCUIElementTypeOther[@name="推荐"]', timeout=20, desc="点击推荐tab")
            time.sleep(2)
            self.device.click_by_xpath('//XCUIElementTypeButton[@name="segmentNav"]', timeout=20, desc="点击首页more")
            time.sleep(2)
            self.device.driver.execute_script("mobile: swipe", {"direction": "up"})
            time.sleep(2)
            self.device.driver.execute_script("mobile: swipe", {"direction": "up"})
            time.sleep(2)
            self.device.click_by_xpath('//XCUIElementTypeStaticText[@name="游戏中心"]', timeout=20, desc="点击游戏中心")
            time.sleep(2)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_游戏中心"]', timeout=10)
        except Exception as e:
            return False
        return True

    def base_my_game(self):
        """从游戏中心进入我的游戏
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            time.sleep(5)
            self.device.click_by_xpath('(//XCUIElementTypeOther[@name="我的"])[2]', timeout=20, desc="点击我的tab")
            time.sleep(10)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_我的棋牌游戏"]', timeout=10)
        except Exception as e:
            return False
        return True

    def click_carouse_map(self):
        """游戏中心主页-点击轮播图
        Args:
         newgame: 游戏中心新游元素
         poker: 游戏中心棋牌游戏
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            self.device.tap([(160, 140)])
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']",
                                                  timeout=5)
                g_logger.info("成功进入H5游戏")
                return True
            except:
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='活动名']",
                                                      timeout=5)
                    g_logger.info("成功进入活动页面")
                    return True
                except:
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏名']",
                                                          timeout=5)
                        g_logger.info("成功进入游戏详情页")
                        return True
                    except:
                        try:
                            self.device.find_element_by_xpath("//android.widget.TextView[@text='下载页面名']",
                                                              timeout=5)
                            g_logger.info("成功进入appstore对应的下载页面")
                        except:
                            return False
        except:
            return False

    def get_location_by_xpath(self, xpath, timeout=None):
        """
        得到元素xpath的坐标
        Args:
            xpath: 元素的xpath
        Returns:
            True: 进入成功
            False: 进入失败
        """
        try:
            obj = self.device.find_element_by_xpath(xpath)
            x = obj.location['x']
            y = obj.location['y']
            return (x, y)
        except Exception as e:
            return False

    # def matchImg(imgsrc, imgobj, confidencevalue=0.5):  # imgsrc=原始图像，imgobj=待查找的图片
    #     imsrc = ac.imread(imgsrc)
    #     imobj = ac.imread(imgobj)
    #
    #     match_result = ac.find_template(imsrc, imobj, confidencevalue)
    #     if match_result is not None:
    #         match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
    #
    #     # 匹配区域置黑
    #     start_y = match_result['rectangle'][0][0]
    #     start_x = match_result['rectangle'][0][1]
    #     end_y = match_result['rectangle'][2][0]
    #     end_x = match_result['rectangle'][1][1]
    #     for i in range(start_x, end_x):
    #         for j in range(start_y, end_y):
    #             imsrc[i, j, 0] = 255
    #             imsrc[i, j, 1] = 0
    #             imsrc[i, j, 2] = 0
    #     ac.show(imsrc)
    #
    #     return match_result

    def login_in(self, account, password):
        """
        密码登录--我的页
        Args:
            account: 用户名
            password: 密码
        Returns:
            True: 进入成功
            False：进入失败
         """
        try:

            self.device.click_by_xpath(self.conf.gamecenter_mine_login.xpath, timeout=20,desc="点击登录按钮")
            time.sleep(2)
            self.login_in_with_password(account, password)
            time.sleep(4)
        except:
              return False
        return True

    def login_in_with_password(self, account, password):
        """
        游戏中心--密码登录
        Args:
            account: 登录账号
            password:登录密码
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="密码"]', timeout=5)
            self.device.click_by_xpath('//XCUIElementTypeStaticText[@name="密码"]', timeout=5, desc="点击密码按钮")
            self.device.click_by_xpath('(//XCUIElementTypeButton[@name="切换账号"])[1]', timeout=5, desc="点击切换账号按钮")
            self.device.click_by_xpath('//XCUIElementTypeStaticText[@name="密码"]', timeout=5, desc="点击密码按钮")
            self.enter_account_password(account, password)
            return True

        except:
            try:
                self.device.find_element_by_xpath('(//XCUIElementTypeButton[@name="切换账号"])[1]', timeout=5)
                self.device.click_by_xpath('(//XCUIElementTypeButton[@name="切换账号"])[1]', timeout=5, desc="点击切换账号按钮")
                time.sleep(2)
                self.device.click_by_xpath('//XCUIElementTypeStaticText[@name="密码"]', timeout=5, desc="点击密码按钮")
                time.sleep(2)
                self.enter_account_password(account, password)
                return True
            except:
                try:
                    self.device.find_element_by_xpath('(//XCUIElementTypeTextField[@name="手机号"])[1]', timeout=5)
                    self.enter_account_password(account, password)
                    return True
                except:
                    g_logger.error("其他密码方式登录暂不支持")
                    return False

    def enter_account_password(self, account, password):
        """
        输入账号密码登录
        Args:
            account: 登录账号
            password: 密码
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_xpath('(//XCUIElementTypeTextField[@name="手机号"])[1]', timeout=20).send_keys(account)
            self.device.find_element_by_xpath('(//XCUIElementTypeTextField[@name="密码"])[1]', timeout=20).send_keys(password)
            time.sleep(3)
            self.device.click_by_xpath('//XCUIElementTypeButton[@name="登录"]', timeout=20, desc="点击登录按钮")
            time.sleep(5)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=20)
        except:
            return False
        return True

    def logout(self):
        """检查页面的标题
        Args:
            title: 页面标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            time.sleep(2)
            self.device.click_by_xpath('//XCUIElementTypeButton[@name="我的"]', timeout=20, desc="点击基线我的tab")
            time.sleep(5)
            self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="登录"]', timeout=5)
            g_logger.info("用户未登录")
            return True
        except:
            try:
                g_logger.info('start logout')
                self.device.tap([(100,93)])
                time.sleep(2)
                self.device.click_by_xpath('(//XCUIElementTypeStaticText[@name="设置"])[2]', timeout=20, desc="点击设置按钮")
                time.sleep(2)
                self.device.click_by_xpath('//XCUIElementTypeOther[@name="退出登录"]', timeout=20, desc="点击退出登录按钮")
                time.sleep(2)
                for i in range(3):
                    try:
                        self.device.click_by_xpath('//XCUIElementTypeButton[@name="退出登录"]', timeout=20, desc="点击确认退出登录按钮")
                        time.sleep(2)
                        break
                    except Exception as e:
                        time.sleep(3)
                else:
                    return False
                self.device.find_element_by_xpath('//XCUIElementTypeButton[@name="立即登录"]', timeout=20)
                self.device.click_by_xpath('//XCUIElementTypeButton[@name="title back"]', timeout=20, desc="点击返回按钮")
                g_logger.info('logout success')
            except:
                return False
        return True

    def check_event_title(self, title):
        """
        检查活动标题
        Args:
            title: 活动标题
        Returns:
           True: 进入成功
           False：进入失败
         """
        for i in range(4):
            try:
                self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="{}"]'.format(title), timeout=20)
                break
            except Exception as e:
                if i == 3:
                    g_logger.info('标题寻找失败')
                    return False
                # self.device.driver.execute_script("mobile: swipe", {"direction": "up"})
                self.device.driver.execute_script('mobile: dragFromToForDuration', {'duration': 0, 'fromX': 200, 'fromY': 250, 'toX': 200, 'toY': 100})
                continue
        return True

    def check_title(self, title):
        """
        检查活动标题
        Args:
            title: 活动标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.driver.execute_script('mobile: dragFromToForDuration', {'duration': 0, 'fromX': 200, 'fromY': 250, 'toX': 200, 'toY': 100})
            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="{}"]'.format(title), timeout=20)
            return True
        except Exception as e:
                return False

    def check_game_name(self,game1, game2, game3, game4):
        """
        检查游戏是否正常显示
        Returns:
           True: 进入成功
           False：进入失败
        """
        try:

            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="{}"]'.format(game1), timeout=10)
            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="{}"]'.format(game2), timeout=10)
            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="{}"]'.format(game3), timeout=10)
            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="{}"]'.format(game4), timeout=10)

        except:

            return False
        return True


    def check_enter_button(self):
        """检查进入按钮
        Args:
            title:
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:

            self.device.find_element_by_xpath('(//XCUIElementTypeOther[@name="进入"])[1]', timeout=10)
            self.device.find_element_by_xpath('//XCUIElementTypeOther[@name="点击即玩"]', timeout=10)
            self.device.find_element_by_xpath('(//XCUIElementTypeOther[@name="进入"])[2]', timeout=10)
            self.device.find_element_by_xpath('(//XCUIElementTypeOther[@name="进入"])[3]', timeout=10)

        except:
            return False
        return True

    def click_enter_button1(self):
        """点击每日推荐第一个进入按钮
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:

            self.device.click_by_xpath('(//XCUIElementTypeOther[@name="进入"])[1]', timeout=10,desc="点击第一个进入按钮")
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="爱奇艺游戏"]', timeout=20)
        except:
            return False
        return True

    def click_enter_button2(self):
        """点击每日推荐第二个进入按钮
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:

            self.device.click_by_xpath('(//XCUIElementTypeOther[@name="进入"])[2]', timeout=10,desc="点击第二个进入按钮")
            self.device.find_element_by_xpath('(//XCUIElementTypeOther[@name="进入"])[2]', timeout=10)
        except:
            return False
        return True

    def click_chess_area(self):
        """点击棋牌专区大图
        Args:
            title:
        Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            self.device.click_by_xpath(self.conf.gamecenter_recommend_chess_area.xpath, timeout=20, desc="点击棋牌专区按钮")
        except:
            return False
        return True

    def click_and_play(self, UID):
        """点击即玩
        Args:
            UID: 游客账号UID
         Returns:
            True: 进入成功
            False：进入失败
         """
        try:
            self.device.click_by_xpath('(//XCUIElementTypeOther[@name="点击即玩"])[1]', timeout=20, desc="点击点击即玩按钮")
            time.sleep(5)
            self.device.click_by_xpath('//XCUIElementTypeOther[@name="补充"]/XCUIElementTypeLink', timeout=20, desc="点击侧边栏")
            time.sleep(5)
            self.device.click_by_xpath('//XCUIElementTypeStaticText[@name="账号"]', timeout=10, desc="点击账号")
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="{}"]'.format(UID), timeout=10)
        except:
            return False
        return True

    def chess_area_back(self):
        """返回推荐页面
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:

            self.device.find_element_by_xpath(self.conf.gamecenter_chess_area_back.xpath, timeout=10).click()

        except:
            return False
        return True

    def enter_my_chess_area(self):
        """进入我的--棋牌专区
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            self.device.click_by_xpath(self.conf.gamecenter_mine.xpath, timeout=20, desc= "点击底部我的tab")
            time.sleep(2)
            self.device.click_by_xpath(self.conf.gamecenter_mine_poker_zone.xpath, timeout=20, desc= "点击棋牌专区")
            time.sleep(3)
        except:
            return False
        return True

    def click_and_check_gamedetail(self):
        """
        点击游戏图标并检查游戏详情页
         Returns:
            True: 进入成功
            False：进入失败
         """
        try:
            self.device.click_by_xpath('(//XCUIElementTypeButton[@name="RN_QYButton"])[2]', timeout=20, desc="点击棋牌区第二个游戏")
            time.sleep(3)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_游戏详情"]', timeout=20)
            self.device.click_by_xpath(self.conf.gamecenter_gamedetail_back.xpath, timeout=20, desc="点击返回按钮")
            time.sleep(3)
        except:
            return False
        return True

    def click_and_check_game_appstore(self):
        """点击进入按钮并检查跳转appstore页面
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            self.device.click_by_xpath(self.conf.gamecenter_my_chess_entrance.xpath, timeout=20, desc="点击进入按钮")
            time.sleep(4)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="北京爱奇艺科技有限公司"]', timeout=20)
        except:
            return False
        return True

    def click_sign_in(self, account, password):
        """
        点击进入签到按钮
         Args:
            account: 登录账号
            password: 密码
         Returns:
            True: 进入成功
            False：进入失败
         """

        self.device.tap([(337,550)])
        time.sleep(2)

        try:
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="其他方式登录"]', timeout=20)
            self.login_in_with_password(account, password)
            time.sleep(4)
            self.device.tap([(337, 550)])
        except:
            pass

        for i in range(5):
            try:
                self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_经验值"]', timeout=20)
                self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_金币"]', timeout=20)
                g_logger.info("签到成功")
                break
            except:
                if i == 4:
                    g_logger.info("今日已签到")
                time.sleep(2)
                continue
        return True

    def click_button(self, imgsrc):
        """
        点击按钮
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_xpath('(//XCUIElementTypeOther[@name="预约"])[1]', timeout=20, desc="点击首页第一个预约按钮")
            time.sleep(2)
            self.matchimg(imgsrc)
        except:
            return False
        return True

    def my_feedback(self):
        """我的反馈页
         Returns:
           True: 进入成功
           False：进入失败
         """
        try:
            self.device.click_by_xpath('//XCUIElementTypeOther[@name="反馈"]', timeout=20, desc='点击反馈按钮')
            time.sleep(2)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_帮助与反馈"]', timeout=20)
        except:
            return False
        return True

    def check_doudizhu_game(self, imgsrc):
        """
        检查斗地主显示样式
        Returns:
            True: 进入成功
            False：进入失败
        """
        self.device.driver.execute_script("mobile: swipe", {"direction": "up"})
        time.sleep(2)

        if(self.matchimg(imgsrc)):
            return True
        else:
            return False

    def matchimg(self, imgsrc):
        """
        图片匹配
        Returns:
            True: 进入成功
            False：进入失败
        """
        confidencevalue = 0.4
        img_src_path = os.path.join(g_resource['project_path'], 'conf', 'img', '1c.png')
        self.device.get_screenshot_as_file(img_src_path)
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(img_src_path)
        match_result = ac.find_template(imsrc, imobj, confidencevalue)
        if match_result:
            g_logger.info("匹配成功")
            return True
        else:
            g_logger.info("匹配失败")
            return False

    def click_doudizhu_game(self):
        """
        点击斗地主游戏的游戏行
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_xpath('(//XCUIElementTypeButton[@name="RN_QYButton"])[2]', timeout=20, desc='点击斗地主游戏的游戏行')
            time.sleep(5)
            self.device.find_element_by_xpath('//XCUIElementTypeStaticText[@name="RN_游戏详情"]', timeout=20)
            self.device.click_by_xpath(self.conf.gamecenter_gamedetail_back.xpath, timeout=20, desc="点击返回按钮")
        except:
            return False
        return True

    def click_enter_doudizhu(self, imgsrc):
        """
        点击进入斗地主游戏
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_xpath('//XCUIElementTypeButton[@name="RN_QYButton 进入"]', timeout=20, desc='点击进入斗地主游戏')
            time.sleep(15)
            self.matchimg(imgsrc)
        except:
            return False
        return True

    def click_play_now(self, imgsrc):
        """
        点击立即试玩
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_xpath('//XCUIElementTypeButton[@name="RN_QYButton 点击立即试玩"]', timeout=20, desc='点击立即试玩')
            time.sleep(15)
            self.matchimg(imgsrc)
        except:
            return False
        return True


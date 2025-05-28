# -*- coding: UTF-8 -*-

"""
File Name:      smoke
Author:         gufangmei_sx
Create Date:    2018/7/9
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class Smoke(Android):
    """Smoke类"""
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android')

        self.target = target
        self.data = target.data
        self.device = target.device

    # def test(self):
    #     """Smoke测试接口
    #
    #     """
    #     # self.device.test()
    #     g_logger.info("Demoapk test")
    #
    # def into_game_center(self, newgame, poker):
    #     """从推荐页面中基线进入游戏中心
    #     Args:
    #      newgame: 游戏中心新游元素
    #      poker: 游戏中心棋牌游戏
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     time.sleep(5)
    #     for i in range(6):
    #         try:
    #             self.device.find_element_by_id(self.conf.base_recommend.id, timeout=5).click()
    #             try:
    #                 time.sleep(5)
    #                 self.device.find_element_by_xpath(self.conf.base_recommend_gamecenter.xpath, timeout=5).click()
    #                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(newgame), timeout=5)
    #             except:
    #                 self.device.find_element_by_xpath(self.conf.base_recommend_gamecenter_plugin.xpath, timeout=5).click()
    #                 for i in range(30):
    #                     try:
    #                         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(poker), timeout=5)
    #                         break
    #                     except:
    #                         time.sleep(5)
    #                         continue
    #
    #             break
    #         except Exception as e:
    #             g_logger.info(str(e))
    #             # 升级提示
    #             try:
    #                 self.device.find_element_by_id(self.conf.base_upgrade_close.id, timeout=5).click()
    #                 time.sleep(1)
    #                 continue
    #             except:
    #                 pass
    #             if i == 5:
    #                 g_logger.error("into gamecenter failed")
    #                 self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
    #                                                                 "into_gamecenter_{}_failed.png".format(
    #                                                                     g_resource['testcase_loop'])))
    #                 return False
    #             time.sleep(3)
    #     return True
    #
    # def into_vip_page(self, title):
    #     """ 从游戏中心首页进入游戏会员页
    #     Args:
    #      title: 页面标题
    #     Returns:
    #         True：进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_game_vip.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
    #     except:
    #         return False
    #     return True


    # def into_download_manager(self):
    #     """从游戏中心首页进入下载管理器
    #     Returns:
    #         True：进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_download_manager_button.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='更新']").click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='下载']").click()
    #     except:
    #         return False
    #     return True


    # def game_center_search(self, search_text=''):
    #     """ 游戏中心页面搜索操作
    #     Args:
    #         search_text: 搜索文本
    #     Returns:
    #         True: 搜索成功
    #         False: 搜索失败
    #     """
    #     try:
    #         self.device.find_element_by_id('com.qiyi.gamecenter:id/navtitle_search_btn', timeout=5).click()
    #         time.sleep(1)
    #         self.device.find_element_by_id(self.conf.gamecenter_search_input.id,timeout=5).send_keys(
    #             search_text)
    #         time.sleep(2)
    #         self.device.hide_keyboard()
    #         self.device.find_element_by_xpath("//{}[@text='{}']".format(self.conf.gamecenter_search_game.cls, search_text),timeout=5).click()
    #
    #     except Exception as e:
    #         return False
    #     return True
    #
    # def into_game(self, game_text=''):
    #     """游戏中心-进入游戏详情界面
    #     Args:
    #         game_text: 进入的游戏名
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_text)).click()
    #     except:
    #         g_logger.info('into game：{} failed'.format(game_text))
    #         return False
    #     return True
    #
    # def into_datail_page(self):
    #     """ 游戏中心-点击焦点图进入游戏详情界面
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_focus_image.id, timeout=5).click()
    #     except:
    #         return False
    #     return True
    #
    # def click_carousel_map1(self, game_title):
    #     """ 游戏会员页-点击轮播图
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         time.sleep(2)
    #         self.device.tap([(540, 445)])
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_title),
    #                                               timeout=5)
    #             #self.device.find_element_by_xpath(self.conf.h5_detail_page.xpath, timeout=5)
    #             g_logger.info("成功进入H5活动页")
    #             return True
    #         except:
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_title),
    #                                                   timeout=5)
    #                 #self.device.find_element_by_xpath(self.conf.special_detail_page.xpath, timeout=5)
    #                 g_logger.info("成功进入专题详情页")
    #                 return True
    #             except:
    #                 try:
    #                     self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_title),
    #                                                       timeout=5)
    #                     g_logger.info("成功进入游戏详情页")
    #                     return True
    #                 except:
    #                     return False
    #     except:
    #         return False
    #
    # def click_carousel_map2(self, h5_title):
    #     """ 游戏会员页-点击轮播图
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         time.sleep(5)
    #         self.device.tap([(540, 445)])
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(h5_title),
    #                                               timeout=5)
    #             # self.device.find_element_by_xpath(self.conf.h5_detail_page.xpath, timeout=5)
    #             g_logger.info("成功进入H5活动页")
    #             return True
    #         except:
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(h5_title),
    #                                                   timeout=5)
    #                 # self.device.find_element_by_xpath(self.conf.special_detail_page.xpath, timeout=5)
    #                 g_logger.info("成功进入专题详情页")
    #                 return True
    #             except:
    #                 try:
    #                     self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(h5_title),
    #                                                       timeout=5)
    #                     g_logger.info("成功进入游戏详情页")
    #                     return True
    #                 except:
    #                     return False
    #     except:
    #         return False
    #
    # def click_carousel_map3(self, special_title):
    #     """ 游戏会员页-点击轮播图
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         time.sleep(9)
    #         self.device.tap([(540, 445)])
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_title),
    #                                               timeout=5)
    #             #self.device.find_element_by_xpath(self.conf.h5_detail_page.xpath, timeout=5)
    #             g_logger.info("成功进入H5活动页")
    #             return True
    #         except:
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_title),
    #                                                   timeout=5)
    #                 #self.device.find_element_by_xpath(self.conf.special_detail_page.xpath, timeout=5)
    #                 g_logger.info("成功进入专题详情页")
    #                 return True
    #             except:
    #                 try:
    #                     self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_title),
    #                                                       timeout=5)
    #                     g_logger.info("成功进入游戏详情页")
    #                     return True
    #                 except:
    #                     return False
    #     except:
    #         return False

    # def into_vip_game_datail_page(self,game_title):
    #     """ 游戏中心-点击焦点图进入游戏详情界面
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_title))
    #         g_logger.info("成功进入游戏详情页")
    #         time.sleep(2)
    #     except:
    #         return False
    #     return True
    #
    # def into_vip_special_datail_page(self,special_title ):
    #     """ 游戏中心-点击焦点图进入专题详情界面
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         g_logger.info("成功进入专题详情页")
    #         self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(special_title))
    #
    #     except:
    #         return False
    #     return True
    #
    # def into_vip_h5_detail_page(self, h5_title):
    #     """ 游戏中心-点击焦点图进入H5活动页
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(h5_title))
    #         g_logger.info("成功进入H5活动页")
    #     except:
    #         return False
    #     return True

    # def large_picture_into_datail_page(self, game_introduction):
    #     """游戏中心-点击大图进入游戏详情界面
    #     Args:
    #      game_introduction: 游戏中心大图详情页标语
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     for i in range(30):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_introduction), timeout=5)
    #             break
    #         except:
    #             if i == 29:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_introduction),
    #                                           timeout=5).click()
    #         time.sleep(5)
    #     except:
    #         return False
    #     return True

    # def game_detail_check(self, game_name, version, sizeof, publish_date, developer, platform):
    #     """ 游戏中心-进入游戏详情，查看详情页面信息
    #     Args:
    #      game_name: 游戏名
    #      version: 游戏版本号
    #      sizeof: 游戏大小
    #      publish_date: 游戏上线时间
    #      developer: 游戏出版商
    #      platform: 游戏系统要求
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #         time.sleep(5)
    #     except:
    #         return False
    #
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     # 滑动查找游戏详细信息
    #     for i in range(10):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(version), timeout=5)
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(sizeof), timeout=5)
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(publish_date), timeout=5)
    #             # self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(developer), timeout=5)
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(platform), timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 9:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
    #             time.sleep(1)
    #             continue
    #     return True

    # def into_my_game_module(self, my_module, tab):
    #     """ 游戏中心-我的游戏模块
    #      Args:
    #      my_module: 查看全部我的游戏
    #      tab: 玩过tab
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(my_module), timeout=5).click()
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(tab), timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def back_to_homepage(self):
    #     """ 返回游戏中心首页
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id("com.qiyi.gamecenter:id/actionBar_back", timeout=5).click()
    #     except:
    #         return False
    #     return True
    #
    # def into_small_game_module(self):
    #     """ 游戏中心-小游戏模块
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.tap([(250, 824)])
    #         time.sleep(2)
    #
    #         try:
    #             self.device.find_element_by_xpath(self.conf.base_user_login_pop_up.xpath, timeout=5).click()
    #         except:
    #             pass
    #
    #         try:
    #             self.device.find_element_by_id(self.conf.gamecenter_H5_game_sidebar.id, timeout=5).click()
    #             time.sleep(2)
    #             self.device.find_element_by_id(self.conf.gamecenter_H5_game_sidebar_libao.id, timeout=5)
    #             return True
    #         except:
    #             try:
    #                 self.device.find_element_by_xpath(self.conf.base_user_login_pop_up_X.xpath, timeout=5).click()
    #                 self.device.find_element_by_xpath(self.conf.base_user_login_pop_up.xpath, timeout=5).click()
    #                 self.device.find_element_by_id(self.conf.gamecenter_H5_game_sidebar.id, timeout=5).click()
    #                 time.sleep(2)
    #                 self.device.find_element_by_id(self.conf.gamecenter_H5_game_sidebar_libao.id, timeout=5)
    #                 return True
    #             except:
    #                 return False
    #     except:
    #          return False
    #
    #
    # def into_login_page_bought(self):
    #     """从已购买tab进入基线登录页面
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_user.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='已购买']", timeout=5).click()
    #         self.device.find_element_by_xpath("//android.widget.Button[@text='登录']", timeout=5).click()
    #     except:
    #          return False
    #     return True
    #
    # def into_login_page_reserved(self):
    #     """从已预约tab进入基线登录页面
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_user.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='已预约']", timeout=5).click()
    #         self.device.find_element_by_xpath("//android.widget.Button[@text='登录']", timeout=5).click()
    #     except:
    #          return False
    #     return True
    #
    # def into_login_page(self):
    #     """ 个人中心页上方登录模块的“登录”按钮进入基线登录页面
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_user.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='登录']", timeout=5).click()
    #     except:
    #          return False
    #     return True
    #
    # def login_in(self, account, password):
    #     """ 用户登录
    #     Args:
    #      account: 用户账号
    #      password: 密码
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         time.sleep(5)
    #         self.device.find_element_by_id(self.conf.gamecenter_user.id, timeout=5).click()
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='登录']", timeout=5).click()
    #         try:
    #             self.login_in_with_password(account, password)
    #             self.device.find_element_by_id("com.qiyi.gamecenter:id/actionBar_back", timeout=5).click()
    #         except:
    #             return False
    #     except:
    #          g_logger.info("用户已登录")
    #     return True
    #
    # def login_in_with_password(self, account, password):
    #     """游戏中心--密码登录
    #     Args:
    #         account: 登录账号
    #         password:登录密码
    #         actionBar_title: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='密码登录']", timeout=5)
    #         sms_id = self.get_location_by_xpath("//android.widget.TextView[@text='密码登录']", timeout=5)
    #         g_logger.info(sms_id)
    #         self.device.tap([sms_id])
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='切换账号']", timeout=5)
    #         self.device.tap([sms_id])
    #         self.enter_account_password(account, password)
    #         return True
    #
    #     except:
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='切换账号']", timeout=5)
    #             self.device.find_element_by_id(self.conf.gamecenter_my_game_vip_chg_login.id, timeout=5).click()
    #             sms_id = self.get_location_by_xpath("//android.widget.TextView[@text='密码登录']", timeout=5)
    #             self.device.tap([sms_id])
    #             self.enter_account_password(account, password)
    #             return True
    #         except:
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.EditText[@text='请输入您的手机号']", timeout=5)
    #                 self.enter_account_password(account, password)
    #                 return True
    #             except:
    #                 g_logger.error("其他密码方式登录暂不支持")
    #                 return False
    #
    # def enter_account_password(self, account, password):
    #     """游戏中心--短信验证码登录
    #     Args:
    #         account: 登录账号
    #         password: 密码
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_my_game_vip_login_account.id, timeout=5).send_keys(account)
    #         self.device.find_element_by_id(self.conf.gamecenter_my_game_vip_login_password.id, timeout=5).send_keys(password)
    #         time.sleep(2)
    #         self.device.find_element_by_id(self.conf.gamecenter_my_game_vip_login_in.id, timeout=5).click()
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=10)
    #     except:
    #         return False
    #     return True
    #
    # def get_location_by_id(self, id, timeout=None):
    #     try:
    #         obj = self.device.find_element_by_id(id)
    #         x = obj.location['x'] + 30
    #         y = obj.location['y'] - 110
    #         return (x, y)
    #     except:
    #         return False
    #
    # def get_location_by_xpath(self, xpath, timeout=None):
    #     try:
    #         obj = self.device.find_element_by_xpath(xpath)
    #         x = obj.location['x'] + 30
    #         y = obj.location['y'] - 110
    #         return x, y
    #     except Exception as e:
    #         return False
    #
    # def login_in_with_qq(self):
    #     """ 游戏中心--密码登录
    #     Args:
    #      account: 用户账号
    #      password: 密码
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='QQ']", timeout=5)
    #         qq_xpath = self.get_location_by_xpath("//android.widget.TextView[@text='QQ']", timeout=5)
    #         self.device.tap([qq_xpath])
    #     except:
    #
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='QQ登录']", timeout=5).click()
    #
    #     time.sleep(2)
    #     size = self.device.get_window_size()
    #     y = size.get('height')
    #     if y == 1794:
    #         y_axis = self.conf.gamecenter_qq_login.y_1794
    #     elif y == 1920:
    #         y_axis = self.conf.gamecenter_qq_login.y_1920
    #     elif y == 2118:
    #         y_axis = self.conf.gamecenter_qq_login.y_2118
    #     else:
    #         return False
    #
    #     self.device.tap([(540, y_axis)])
    #     time.sleep(2)
    #     self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=10)
    #     return True
    #
    # def login_in_with_wechat(self):
    #     """ 游戏中心--微信登录
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='微信']", timeout=5)
    #         wechat_xpath = self.get_location_by_xpath("//android.widget.TextView[@text='微信']", timeout=5)
    #         self.device.tap([wechat_xpath])
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='个人中心']", timeout=10)
    #         return True
    #     except:
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='微信登录']", timeout=5).click()
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='购买游戏会员']", timeout=10)
    #             return True
    #         except:
    #             return False
    #
    # def check_title(self, button_name):
    #     """ 检查标题
    #     Args:
    #         button_name: 按钮名
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     # 滑动查找某个按钮
    #     for i in range(50):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(button_name), timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 49:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     return True
    #
    # def check_title_xpath(self, actionBar_title):
    #     """ 检查登录后跳转的页面标题
    #     Args:
    #         actionBar_title: 按钮名
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(actionBar_title), timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def click_first_position(self, game_information):
    #     """ 点击横排游戏的第一个运营位
    #     Args:
    #         game_name: 游戏名
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.click_from_position(0.115, 0.620)
    #         self.check_title(game_information)
    #         #self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_information), timeout=5)
    #     except:
    #        return False
    #     return True
    #
    #
    # def click_game_icon(self, game_name):
    #     """ 点击游戏按钮并检查游戏名
    #     Args:
    #         game_name: 游戏名
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     # 滑动查找游戏
    #     for i in range(10):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name),timeout=5).click()
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 9:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     return True
    #
    # def click_button_by_xpath(self, button_name, text):
    #     """ 点击按钮并检查是否正确进入
    #     Args:
    #         button_name: 被点击的按钮
    #         text: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     # 滑动查找游戏详细信息
    #     for i in range(10):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(button_name),timeout=5).click()
    #             self.device.find_element_by_xpath("//android.widget.Button[@text='{}']".format(text),timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 9:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
    #             time.sleep(1)
    #             continue
    #     return True
    #
    # def click_and_check_button(self, open_icon, login_page):
    #     """ 点击图标
    #      Args:
    #         open_icon: 被点击的按钮
    #         login_page: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         # self.device.click_from_position(0.8787,0.4068)
    #         self.device.find_element_by_xpath("//android.widget.Button[@text='{}']".format(open_icon),timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(login_page),timeout=5)
    #     except:
    #         return False
    #     return True

    # def click_and_check(self, user, actionBar_title):
    #     """点击图标并查看页面标题
    #      Args:
    #         user: 被点击的按钮
    #         actionBar_title: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(user), timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(actionBar_title), timeout=5)
    #         time.sleep(5)
    #     except Exception as e:
    #         return False
    #     return True

    # def click_special_first_icon(self, button_name, special_topic):
    #     """ 点击专题推荐第一个运营位
    #
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     # 滑动查找某个按钮
    #     for i in range(5):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(button_name), timeout=5)
    #             (x, y) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(button_name), timeout=5)
    #             g_logger.info((x+100, y+300))
    #             self.device.tap([(x+100, y+300)])
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 4:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_topic), timeout=5)
    #         time.sleep(2)
    #     except:
    #         return False
    #     return True

    # def click_1qibei_icon(self, order_confirm):
    #     """点击1奇贝图标
    #     Args:
    #         order_confirm: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_game_1qibei.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(order_confirm))
    #     except:
    #         return False
    #     return True

    # def click_poker_icon(self, special_topic):
    #     """ 点击棋牌图标
    #     Args:
    #         special_topic: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_poker.id, timeout=5).click()
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_topic))
    #         time.sleep(5)
    #     except:
    #         return False
    #     return True

    # def click_configurable_entry_icon(self, special_topic):
    #     """ 点击可配置入口图标
    #     Args:
    #         special_topic: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_H5_configurable_entry.id, timeout=5).click()
    #         time.sleep(5)
    #         # self.device.find_element_by_xpath(self.conf.base_user_login_pop_up_X.xpath, timeout=5).click()
    #         # time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_topic),timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def click_pay_icon(self):
    #     """点击支付图标
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_game_order_pay_button.id, timeout=5).click()
    #         time.sleep(5)
    #     except:
    #         return False
    #     return True

    # def click_icon_find_all(self, special_topic):
    #     """ 点击游戏列表--查找全部按钮
    #      Args:
    #         special_topic: 页面标题
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     # 滑动查找列表下方信息
    #     for i in range(10):
    #         try:
    #
    #             self.device.find_element_by_id(self.conf.gamecenter_game_list_all.id, timeout=5).click()
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_topic), timeout=5)
    #             time.sleep(5)
    #             break
    #         except:
    #             if i == 9:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     return True


    # def satrt_download_game(self, remove_app_id=None):
    #     """游戏详情界面-开始下载游戏，若游戏已经安装，根据remove_app_id标志是否卸载游戏
    #     Args:
    #         remove_app_id:游戏的bundle id
    #     Returns:
    #         True: 下载成功
    #         False: 下载失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='下载']", timeout=5).click()
    #         time.sleep(10)
    #     except:
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='安装']", timeout=3)
    #             return True
    #         except:
    #             pass
    #
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='打开']")
    #             if remove_app_id:
    #                 self.device.remove_app(remove_app_id)
    #                 return self.satrt_download_game()
    #         except:
    #             return False
    #     return True

    # def buy_vip_game(self, alipay_account, alipay_password, game_name):
    #     """ 开通会员，购买1奇贝游戏
    #     Args:
    #         alipay_account: 支付宝账号
    #         alipay_password: 支付宝密码
    #         game_name:游戏名
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         #self.device.tap([(949, 781)])
    #         self.device.tap([(949, 991)])
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='支付']", timeout=5)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='确认付款']", timeout=5).click()
    #         time.sleep(8)
    #
    #         ##self.mobile_real_authentication(account)
    #         # self.device.find_element_by_xpath(self.conf.gamecenter_alipay_account_name.xpath, timeout=5).click()
    #         self.switch_alipay_account(alipay_account, alipay_password)
    #         self.device.find_element_by_xpath(self.conf.gamecenter_game_pay_confirm.xpath, timeout=5).click()
    #         #self.device.find_element_by_xpath(self.conf.gamecenter_game_input_password.xpath, timeout=5).set_text('')
    #         self.device.find_element_by_xpath(self.conf.gamecenter_game_pay_success.xpath, timeout=5)
    #         self.device.find_element_by_xpath(self.conf.gamecenter_game_pay_done.xpath, timeout=5).click()
    #         time.sleep(5)
    #         self.device.find_element_by_id(self.conf.gamecenter_game_purchase_success.id, timeout=5)
    #         self.device.find_element_by_id(self.conf.gamecenter_game_buy_game.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='订单确认']", timeout=5)
    #         self.device.find_element_by_id(self.conf.gamecenter_game_order_pay_button.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def switch_alipay_account(self, alipay_account, alipay_password):
    #     """切换支付宝账号
    #     Args:
    #         alipay_account: 支付宝账号
    #         alipay_password: 支付宝密码
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #        self.device.find_element_by_xpath(self.conf.gamecenter_game_pay_confirm.xpath, timeout=5)
    #        self.device.tap([(540,509)])
    #        time.sleep(5)
    #        self.device.find_element_by_xpath(self.conf.gamecenter_alipay_other_account.xpath, timeout=5).click()
    #        self.alipay_account_password_login(alipay_account, alipay_password)
    #     except:
    #         try:
    #             self.alipay_account_password_login(alipay_account, alipay_password)
    #         except:
    #            return False
    #     return True
    #
    # def alipay_account_password_login(self, alipay_account, alipay_password):
    #     """ 支付宝账号和密码登录
    #     Args:
    #         alipay_account: 支付宝账号
    #         alipay_password: 支付宝密码
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         time.sleep(2)
    #         self.device.find_element_by_xpath(self.conf.gamecenter_alipay_account_login.xpath, timeout=5).click()
    #         self.device.find_element_by_id(self.conf.gamecenter_alipay_account1.id, timeout=5).send_keys(alipay_account)
    #         self.device.find_element_by_id(self.conf.gamecenter_alipay_password1.id, timeout=5).send_keys(alipay_password)
    #         self.device.find_element_by_id(self.conf.gamecenter_next_step.id, timeout=5).click()
    #     except:
    #         return False
    #     return True
    #
    # def vivo_game_download_and_install(self, prompt):
    #      """vivo手机游戏下载
    #     Args:
    #     prompt: 返回安装结果
    #      Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #      pass
    #
    # def xiaomi_game_download_and_install(self, prompt):
    #     """小米手机游戏下载
    #      Args:
    #     game_name:游戏名
    #     prompt: 返回安装结果
    #        Returns:
    #            True: 进入成功
    #            False：进入失败
    #        """
    #     time.sleep(2)
    #     try:
    #         self.device.tap([(124, 1141)])
    #         self.device.find_element_by_id(self.conf.gamecenter_game_download_installation.id, timeout=5).click()
    #
    #         for i in range(120):
    #             try:
    #                 self.device.find_element_by_id(self.conf.gamecenter_game_download_xiaomi.id, timeout=5)
    #                 break
    #             except:
    #                 if i == 119:
    #                     g_logger.error("下载超时")
    #                     return False
    #                 time.sleep(5)
    #                 continue
    #
    #         self.device.find_element_by_id(self.conf.gamecenter_game_download_xiaomi_cancel.id, timeout=5).click()
    #         self.device.find_element_by_id(self.conf.gamecenter_game_download_installation_manager.id, timeout=5).click()
    #         time.sleep(2)
    #         #self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #
    #         self.device.find_element_by_id(self.conf.gamecenter_game_download_xiaomi_back.id, timeout=5).click()
    #         time.sleep(2)
    #         self.device.find_element_by_id(self.conf.gamecenter_game_download_xiaomi_install.id, timeout=5).click()
    #         self.device.find_element_by_id(self.conf.gamecenter_game_download_xiaomi.id, timeout=5).click()
    #         time.sleep(5)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(prompt), timeout=5)
    #         time.sleep(1)
    #         self.device.find_element_by_id(self.conf.gamecenter_game_download_xiaomi_lanuch_button.id, timeout=5).click()
    #         time.sleep(10)
    #     except:
    #         return False
    #     return True

    # def game_download_and_install(self, prompt):
    #     """游戏下载
    #      Args:
    #      prompt: 返回安装结果
    #      game_name: 游戏名
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     if self.device.get_manufacturer() == "HUAWEI":
    #         return self.huawei_game_download_and_install( prompt)
    #     elif self.device.get_manufacturer() == "Xiaomi":
    #         return self.xiaomi_game_download_and_install( prompt)
    #     elif self.device.get_manufacturer() == "VIVO":
    #         return self.vivo_game_download_and_install( prompt)
    #     else:
    #         g_logger.error("{}手机游戏下载暂不支持".format(self.device.get_manufacturer()))
    #         return False

    # def download_and_install_fdlm(self):
    #     """
    #     下载安装反斗联盟
    #     Args:
    #
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     time.sleep(3)
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     # 滑动查找反斗联盟游戏
    #     for i in range(10):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='反斗联盟']").click()
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 9:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
    #             time.sleep(1)
    #             continue
    #
    #     # 点击下载
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='下载']").click()
    #         time.sleep(10)
    #     except:
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='安装']")
    #         except:
    #             return False
    #
    #     # 安装游戏
    #     for i in range(20):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='安装']").click()
    #             time.sleep(5)
    #         except:
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.Button[@text='vivo帐号验证']").click()
    #                 self.device.find_element_by_id('com.bbk.account:id/dialog_input').set_text('t123456')
    #                 self.device.find_element_by_xpath("//android.widget.Button[@text='验证']").click()
    #                 time.sleep(2)
    #                 for i in range(3):
    #                     try:
    #                         self.device.tap([(540, 1660)])
    #                         # self.device.find_element_by_id('com.android.packageinstaller:id/continue_button').click()
    #                         # self.device.find_element_by_xpath("//android.widget.Button[@text='继续安装']").click()
    #                         time.sleep(1)
    #                         break
    #                     except Exception as e:
    #                         print(e)
    #                         time.sleep(2)
    #
    #                 self.device.find_element_by_id('com.android.packageinstaller:id/ok_button').click()
    #                 time.sleep(3)
    #                 self.device.find_element_by_xpath("//android.widget.Button[@text='完成']").click()
    #                 return True
    #             except Exception as e:
    #                 time.sleep(3)
    #                 pass
    #             # 下载完成后可能出现已完成界面
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.Button[@text='完成']").click()
    #             except:
    #                 pass
    #             try:
    #                 download_stat = self.device.find_element_by_id('com.qiyi.gamecenter:id/details_download_state_text')
    #                 text = download_stat.get_attribute('text')
    #                 if text == '打开':
    #                     return True
    #             except:
    #                 continue
    #     return False
    #
    # def into_user_info(self):
    #     """
    #     进入基线用户信息
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         g_logger.info('into user info')
    #         time.sleep(5)
    #         self.device.find_element_by_id('com.qiyi.video:id/navi3').click()
    #         time.sleep(2)
    #         self.device.find_element_by_id('com.qiyi.video:id/navi3').click()
    #         g_logger.info('into user info success')
    #         return True
    #     except Exception as e:
    #         g_logger.info('into user info failed')
    #         return False
    #
    # def into_small_game(self):
    #     """进入游戏中心小游戏
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     pic_path = os.path.join(g_resource['testcase_log_dir'],"into_small_game_faied_{}.png".format(g_resource['testcase_loop']))
    #
    #     try:
    #         size = self.device.get_window_size()
    #         width = size.get('width')
    #         height = size.get('height')
    #
    #         self.device.tap([(width * 0.21, height * 0.22)])
    #         time.sleep(10)
    #
    #         try:
    #             text = self.device.find_element_by_id('com.qiyi.gamecenter:id/actionBar_title').get_attribute('text')
    #             if 'H5游戏' not in text:
    #                 self.device.get_screenshot_as_file(pic_path)
    #                 return False
    #         except:
    #             self.device.get_screenshot_as_file(pic_path)
    #             return False
    #
    #         # self.device.find_element_by_id('com.qiyi.gamecenter:id/actionBar_back').click()
    #         # time.sleep(2)
    #     except:
    #         self.device.get_screenshot_as_file(pic_path)
    #         return False
    #
    # def into_bottom_H5_game(self):
    #     """进入底部栏可配置页面
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_bottom_configurable.id, timeout = 5).click()
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']", timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def H5_click_download(self, game_name, game_version):
    #     """H5页面点击下载按钮
    #     Args:
    #      game_name: 游戏名
    #      game_version: 游戏版本号
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     try:
    #         # print(self.device.driver.contexts)
    #         # self.device.driver.switch_to.context("WEBVIEW_stetho_com.qiyi.video:plugin1")
    #         #self.device.find_element_by_xpath("//download-btn download countBtn[@data-desc='立即下载按钮']", timeout=5).click()
    #         time.sleep(2)
    #         self.device.tap([(540,1520)])
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #
    #         size = self.device.get_window_size()
    #         width = size.get('width')
    #         height = size.get('height')
    #
    #         # 滑动查找某个按钮
    #         for i in range(6):
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_version),
    #                                                   timeout=5)
    #                 time.sleep(2)
    #                 break
    #             except:
    #                 if i == 5:
    #                     return False
    #
    #                 self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #                 time.sleep(1)
    #                 continue
    #
    #     except Exception as e:
    #         return False
    #     return True
    #
    # def click_reservation_button(self, game_name, promt, open_icon):
    #     """点击预约按钮
    #     Args:
    #      game_name: 游戏名
    #      promt: 提示语
    #      open_icon: 按钮名
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #     except:
    #         size = self.device.get_window_size()
    #         width = size.get('width')
    #         height = size.get('height')
    #
    #         # 滑动查找某个按钮
    #         for i in range(6):
    #             try:
    #                 self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #                 time.sleep(2)
    #                 break
    #             except:
    #                 if i == 5:
    #                     return False
    #
    #                 self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #                 time.sleep(1)
    #                 continue
    #
    #     try:
    #         (x, y) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #         self.device.tap([(x + 300, y + 110)])
    #         time.sleep(2)
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(promt), timeout=5)
    #             self.device.find_element_by_xpath("//android.widget.Button[@text='{}']".format(open_icon), timeout=5).click()
    #             g_logger.info('成功预约')
    #             return True
    #         except:
    #             g_logger.info('该游戏已预约')
    #             return True
    #     except:
    #         return False
    #
    #
    # def click_reserved_button(self, game_name, promt):
    #     """点击已预约按钮
    #     Args:
    #      game_name: 游戏名
    #      promt: 提示语
    #      Returns:
    #        True: 进入成功
    #        False：进入失败
    #      """
    #     try:
    #         (x, y) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #         self.device.tap([(x + 300, y + 110)])
    #         time.sleep(2)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(promt), timeout=5)
    #         g_logger.info('未预约成功')
    #         return False
    #     except:
    #         g_logger.info('已预约')
    #         return True


    # def game_center_into_new_game(self):
    #     """
    #     游戏中心进入新游
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_newgame.id,timeout=5).click()
    #     except:
    #         return False
    #     return True

    # def check_newgame_online_tab(self):
    #     """
    #     新游页--按顺序检查今日新游，本月新游，季度新游
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='今日新游']", timeout=5)
    #     except:
    #         return False
    #
    #     for i in range(10):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='本月新游']", timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 9:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #
    #     for i in range(30):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='季度新游']", timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 29:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     return True
    #
    # def check_latest_reservation(self, game1, game2, game3):
    #     """
    #     新游页--检查最新预约tab的上方三个游戏
    #     Args:
    #      game1: 第一款游戏名
    #      game2: 第二款游戏名
    #      game3: 第三款游戏名
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game1), timeout=5)
    #     except:
    #         return False
    #
    #     for i in range(3):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game2), timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 2:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #
    #     for i in range(5):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game3), timeout=5)
    #             time.sleep(4)
    #             break
    #         except:
    #             if i == 29:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     return True

    # def check_sealing_game(self, game1, game2):
    #     """
    #     新游页--检查封测专区tab的两款游戏
    #     Args:
    #      game1: 第一款游戏名
    #      game2: 第二款游戏名
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game1), timeout=5)
    #     except:
    #         return False
    #
    #     for i in range(3):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game2), timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 2:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     return True

    # def game_center_into_list_page(self):
    #     """
    #     游戏中心进入新游
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_bottom_List.id,timeout=5).click()
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='排行榜']", timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def check_game_order(self, game1, game2, game3):
    #     """
    #     检查游戏顺序
    #     Args:
    #      game1: 第一款游戏名
    #      game2: 第二款游戏名
    #      game3: 第三款游戏名
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game1), timeout=5)
    #         (x1,y1) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game1), timeout=5)
    #     except:
    #         return False
    #
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game2), timeout=5)
    #         (x2, y2) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game2), timeout=5)
    #     except:
    #         return False
    #
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game3), timeout=5)
    #         (x3, y3) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game3), timeout=5)
    #     except:
    #         return False
    #
    #     if(y3>y2>y1):
    #         return True
    #     else:
    #         return False
    #
    # def check_game_details(self):
    #     """
    #     显示详情、福利、圈子三个tab
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     try:
    #         self.device.tap([(124, 1340)])
    #         self.device.find_element_by_id(self.conf.gamecenter_game_title.id, timeout=5)
    #         return False
    #     except:
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='详情']", timeout=5)
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='福利']", timeout=5)
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='圈子']", timeout=5)
    #             return True
    #         except:
    #             return False
    #
    # def check_top_bar_title(self):
    #     """
    #     查看顶部栏显示标题
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     try:
    #         size = self.device.get_window_size()
    #         width = size.get('width')
    #         height = size.get('height')
    #         self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #         time.sleep(2)
    #         self.device.find_element_by_id(self.conf.gamecenter_game_title.id, timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def play_video(self, introduction):
    #     """
    #     视频播放
    #     Args:
    #      introduction: 视频一句话介绍
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     for i in range(5):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(introduction), timeout=5)
    #             self.device.find_element_by_id(self.conf.video_play.id, timeout=5)
    #             time.sleep(2)
    #             break
    #         except:
    #             if i == 4:
    #                 return False
    #
    #             self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
    #             time.sleep(1)
    #             continue
    #     try:
    #         (x, y) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(introduction), timeout=5)
    #
    #         self.device.find_element_by_id(self.conf.video_play.id, timeout=5).click()
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video.png"))
    #         self.device.tap([(x, y)])
    #         self.device.find_element_by_id(self.conf.video_play_pause.id, timeout=5).click()
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_pause.png"))
    #         time.sleep(2)
    #         self.device.find_element_by_id(self.conf.video_play_pause.id, timeout=5).click()
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_again.png"))
    #         time.sleep(3)
    #
    #         self.device.find_element_by_id(self.conf.video_play.id, timeout=5).click()
    #         self.device.find_element_by_id(self.conf.video_play_tolandscape.id, timeout=5).click()
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_tolandscape.png"))
    #         self.device.keyevent(4)
    #         # self.device.tap([(540, 900)])
    #         # self.device.find_element_by_id(self.conf.video_play_tolandscape_back.id, timeout=5).click()
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_tolandscape_back.png"))
    #         return True
    #
    #     except:
    #         return False
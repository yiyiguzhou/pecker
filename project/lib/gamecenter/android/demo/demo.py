# -*- coding: UTF-8 -*-

"""
File Name:      demo
Author:         zhangwei04
Create Date:    2018/1/9
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class Demo(Android):
    def __init__(self, target):
        super().__init__(target=target)

        self.target = target
        self.data = target.data
        self.device = target.device

    # def test(self):
    #     """
    #     Demo测试接口
    #     """
    #     # self.device.test()
    #     g_logger.info("Demoapk test")
    #
    # # def into_game_center(self):
    # #     """
    # #     从推荐页面中基线进入游戏
    # #     Returns:
    # #         True：进入成功
    # #         False：进入失败
    # #     """
    # #     time.sleep(6)
    # #     for i in range(3):
    # #         try:
    # #             self.device.find_element_by_id(self.conf.base_recommend.id, timeout=5).click()
    # #             time.sleep(2)
    # #             self.device.find_element_by_xpath(self.conf.base_recommend_gamecenter.xpath).click()
    # #             time.sleep(2)
    # #             break
    # #         except Exception as e:
    # #             g_logger.info(str(e))
    # #             # 升级提示
    # #             try:
    # #                 self.device.find_element_by_id(self.conf.base_upgrade_close.id, timeout=3).click()
    # #                 time.sleep(1)
    # #             except:
    # #                 pass
    # #             if i == 2:
    # #                 g_logger.error("into gamecenter failed")
    # #                 self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
    # #                                       "into_gamecenter_{}_failed.png".format(g_resource['testcase_loop'])))
    # #                 return False
    # #             time.sleep(3)
    # #
    # #     return True
    #
    # def game_center_find_newgame_poker(self,element1,element2):
    #     """
    #     游戏中心查找新游棋牌
    #     Returns:
    #             True: 搜索成功
    #             False: 搜索失败
    #      """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.LinearLayout[@text='{}']".format(element1), timeout=5)
    #         self.device.find_element_by_xpath("//android.widget.LinearLayout[@text='{}']".format(element2), timeout=5)
    #     except:
    #         return False
    #     return True
    #
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
    #
    # # def into_download_manager(self):
    # #     """
    # #     从游戏中心首页进入下载管理器
    # #     Returns:
    # #         True：进入成功
    # #         False：进入失败
    # #     """
    # #     try:
    # #         self.device.find_element_by_id(self.conf.gamecenter_download_manager_button.id, timeout=5).click()
    # #         time.sleep(2)
    # #         self.device.find_element_by_xpath("//android.widget.TextView[@text='更新']").click()
    # #         time.sleep(2)
    # #         self.device.find_element_by_xpath("//android.widget.TextView[@text='下载']").click()
    # #     except:
    # #         return False
    # #     return True
    #
    #
    # def game_center_new_game_search(self,game_name):
    #     """
    #     游戏中心新游查找游戏，并进入
    #     Returns:
    #             True: 搜索成功
    #              False: 搜索失败
    #     """
    #     try:
    #     #搜索游戏
    #        self.device.find_element_by_id(self.conf.gamecenter_newgame_search_button.id,timeout=5).click()
    #        self.device.find_element_by_id(self.conf.gamecenter_newgame_search_input.id,timeout=5).set_text(game_name)
    #     #进入游戏详情页面
    #        game_xpath = "//{}[@text='{}']".format(self.conf.gamecenter_newgame_search_game.cls,game_name)
    #        self.device.find_element_by_xpath(game_xpath).click()
    #     except:
    #         return False
    #     return True
    #
    #
    # def game_center_search(self, search_text=''):
    #     """
    #     游戏中心页面搜索操作
    #     Args:
    #         search_text: 搜索文本
    #     Returns:
    #         True: 搜索成功
    #         False: 搜索失败
    #     """
    #     try:
    #         self.device.find_element_by_id('com.qiyi.gamecenter:id/navtitle_search_btn', timeout=10).click()
    #         time.sleep(1)
    #         self.device.find_element_by_id(self.conf.gamecenter_search_input.id,timeout=5).send_keys(
    #             search_text)
    #         time.sleep(2)
    #         self.device.hide_keyboard()
    #         search_text = "//{}[@text='{}']".format(self.conf.gamecenter_search_game.cls,search_text)
    #         self.device.find_element_by_xpath(search_text).click()
    #         self.device.find_element_by_xpath(search_text)
    #
    #     except Exception as e:
    #         return False
    #     return True
    #
    # def into_game(self, game_text=''):
    #     """
    #     游戏中心-进入游戏详情界面
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
    #     """
    #     游戏中心-点击焦点图进入游戏详情界面
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_id(self.conf.gamecenter_focus_image.id,timeout=5).click()
    #     except:
    #         return False
    #     return True
    #
    # def game_detail_search(self, game_name, version, size, publish_date, developer, platform):
    #     """
    #     游戏中心-从焦点图进入游戏详情，查看详情页面信息
    #     Returns:
    #         True: 进入成功
    #         False：进入失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(version), timeout=5)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(size), timeout=5)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(publish_date), timeout=5)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(developer), timeout=5)
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(platform), timeout=5)
    #     except:
    #         return False
    #     return True
    #
    # def satrt_download_game(self, remove_app_id=None):
    #     """
    #     游戏详情界面-开始下载游戏，若游戏已经安装，根据remove_app_id标志是否卸载游戏
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
    #
    # def install_game_huawei_mate10(self):
    #     """
    #     游戏详情页面-安装游戏
    #     Returns:
    #         True: 安装成功
    #         False：安装失败
    #     """
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='安装']", timeout=4).click()
    #         time.sleep(1)
    #     except:
    #         pass
    #     try:
    #         self.device.find_element_by_id("com.android.packageinstaller:id/decide_to_continue", timeout=120).click()
    #         self.device.find_element_by_xpath("//android.widget.Button[@text='继续安装']", timeout=6).click()
    #         # 点击信任此应用
    #         self.device.find_element_by_id('com.android.packageinstaller:id/listItemButton', timeout=20).click()
    #         self.device.find_element_by_xpath("//android.widget.Button[@text='完成']").click()
    #     except:
    #         g_logger.error('installing game failed')
    #         return False
    #
    #     try:
    #         g_logger.info('检测游戏是否安装完成')
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='打开']", timeout=10)
    #     except:
    #         g_logger.error("check game install down failed")
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
    #                                                         "download_{}_failed.png".format(
    #                                                             g_resource['testcase_loop'])))
    #         return False
    #     path = os.path.join(g_resource['testcase_log_dir'],
    #                         "download_{}_success.png".format(g_resource['testcase_loop']))
    #     self.device.get_screenshot_as_file(path)
    #     return True
    #
    # def into_new_game(self):
    #     """
    #     游戏中心- 进入新游选项
    #     Returns:
    #
    #     """
    #     for i in range(3):
    #         try:
    #             self.device.find_element_by_xpath("//android.widget.TextView[@text='新游']").click()
    #             break
    #         except Exception as e:
    #             if i == 2:
    #                 return False
    #             time.sleep(3)
    #     return True
    #
    # def download_and_install_fdlm(self):
    #     """
    #     下载安装反斗联盟
    #     """
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
    # def remove_fdlm(self):
    #     """移除反斗联盟"""
    #     try:
    #         self.device.remove_app('com.gunnergo.kunpo.iqiyi')
    #     except Exception as e:
    #         return False
    #     return True
    #
    # def remove_game(self, app_id=''):
    #     """
    #     卸载游戏
    #     Args:
    #         app_id: 游戏bundle ID
    #     Returns:
    #         True: 卸载成功
    #         False：卸载失败
    #     """
    #     try:
    #         self.device.remove_app(app_id)
    #     except Exception as e:
    #         g_logger.error('移除游戏{}失败'.format(app_id))
    #         return False
    #     return True
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
    # def login_passwd(self, username, passwd):
    #     """
    #     使用邮箱密码方式登录
    #     Args:
    #         username: 用户名
    #         passwd: 用户密码
    #     Returns:
    #         True：登录成功
    #         False：登录失败
    #     """
    #     try:
    #         try:
    #             self.device.find_element_by_id('com.qiyi.video:id/my_main_login', timeout=10).click()
    #             time.sleep(2)
    #         except:
    #             if self.logout():
    #                 self.device.find_element_by_id('com.qiyi.video:id/title_bar_left').click()
    #                 time.sleep(1)
    #             self.device.find_element_by_id('com.qiyi.video:id/my_main_login', timeout=10).click()
    #             time.sleep(2)
    #
    #         try:
    #             self.device.find_element_by_id('com.qiyi.video:id/et_phone', timeout=5).set_text(
    #                 username)
    #             self.device.hide_keyboard()
    #         except Exception as e:
    #             pass
    #
    #         # 输入密码
    #         self.device.find_element_by_id('com.qiyi.video:id/et_pwd', timeout=5).set_text(passwd)
    #         self.device.hide_keyboard()
    #         # 点击登录
    #         self.device.find_element_by_id('com.qiyi.video:id/tv_login').click()
    #         time.sleep(4)
    #     except Exception as e:
    #         g_logger.info(e)
    #         start = time.time()
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
    #                                                         "login_passwd_faied_{}.png".format(
    #                                                             g_resource['testcase_loop'])))
    #         g_logger.info("screen time: {}".format(time.time() - start))
    #         return False
    #
    #     start = time.time()
    #     self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
    #                                                     "login_passwd_faied_{}.png".format(
    #                                                         g_resource['testcase_loop'])))
    #     g_logger.info("screen time: {}".format(time.time() - start))
    #     return True
    #
    # def logout(self):
    #     """
    #     基线退出登录
    #     Returns:
    #         True：退出登录成功
    #         False：退出登录失败
    #     """
    #     try:
    #         self.reset_app()
    #         time.sleep(4)
    #         g_logger.info('start logout')
    #         # 进入我的信息
    #         self.into_user_info()
    #         time.sleep(2)
    #         # 寻找用户图标
    #         try:
    #             self.device.find_element_by_id('com.qiyi.video:id/phone_avatar_icon').click()
    #             time.sleep(2)
    #         except Exception as e:
    #             return False
    #         # 在用户界面点击设置图标
    #         self.device.find_element_by_id('com.qiyi.video:id/title_bar_setting').click()
    #         time.sleep(2)
    #
    #         # 通过坐标点击退出登录
    #         size = self.device.get_window_size()
    #         width = size.get('width')
    #         height = size.get('height')
    #         self.device.tap([(width / 2, height * 7 / 10)])
    #         time.sleep(2)
    #         # 点击弹出的‘立即退出’确认按钮
    #         try:
    #             self.device.find_element_by_id('com.qiyi.video:id/tv_right', timeout=20).click()
    #         except Exception as e:
    #             return False
    #
    #         # 通过立即登录按钮来检测退出登录是否成功
    #         self.device.find_element_by_id('com.qiyi.video:id/pp_loading_result_go')
    #     except Exception as e:
    #         return False
    #
    #     g_logger.info('logout success')
    #     return True

    # def reset_app(self, clear_data=False):
    #     """
    #     重置app
    #     Args:
    #         clear_data:是否清除数据
    #
    #     Returns:
    #
    #     """
    #     try:
    #         if clear_data:
    #             self.device.reset()
    #         else:
    #             self.device.close_app()
    #             time.sleep(1)
    #             self.device.launch_app()
    #             time.sleep(1)
    #         return True
    #     except Exception as e:
    #         return False

    # def in_game_center_first_pos_out(self, loop_times = 1):
    #     """压测游戏中心通过坐标点击第一个运营位
    #     Args:
    #         loop_times: 压测次数
    #     """
    #     size = self.device.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #
    #     for i in range(loop_times):
    #         g_logger.info("start looptime {}".format(i + 1))
    #         try:
    #             self.device.tap([(width * 0.25, height * 0.47)])
    #             time.sleep(5)
    #             self.device.find_element_by_id('com.qiyi.gamecenter:id/actionBar_back').click()
    #             time.sleep(2)
    #
    #             ele = self.device.find_element_by_id('com.qiyi.gamecenter:id/actionBar_title', timeout=6)
    #             if '游戏中心' == ele.get_attribute('text'):
    #                 g_logger.info("success")
    #                 continue
    #
    #         except Exception as e:
    #             try:
    #                 self.device.find_element_by_id('com.qiyi.gamecenter:id/tv_recommend').click()
    #                 self.into_game_center()
    #             except:
    #                 g_logger.error("has occur not found exception")
    #                 self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
    #                                                                 "postion_passwd_faied_{}.png".format(
    #                                                                     g_resource['testcase_loop'])))
    #                 self.reset_app()
    #                 continue
    #     return True
    #
    # def into_classify_game_center(self):
    #     """进入游戏中心-分类界面"""
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='分类']", timeout=10).click()
    #         time.sleep(3)
    #     except:
    #         g_logger.error("进入分类失败")
    #         self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
    #                                                         "into_classify_faied_{}.png".format(
    #                                                             g_resource['testcase_loop'])))
    #         return False
    #     return True
    #
    # def into_small_game(self):
    #     """进入游戏中心小游戏"""
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
    # def clear_buff_data(self, path="", file_names=[], su_flag=False):
    #     """
    #     清除缓存数据
    #     Args:
    #         path: 缓存数据存放的路径
    #         file_names: 缓存数据的目录或者文件
    #         su_flag: 是否切换su模式
    #     """
    #     if not path:
    #         path = '/data/data/com.qiyi.video'
    #     if isinstance(file_names, str):
    #         file_names = [file_names]
    #
    #     for file in file_names:
    #         if su_flag:
    #             cmd = "su & cd {} & rm -rf {}".format(path, file)
    #         else:
    #             cmd = "cd {} & rm -rf {}".format(path, file)
    #         self.device.adb.adb_shell(cmd)
    #     return True
    #
    # def login_sms(self, phone):
    #     """
    #     短信方式登录
    #     Args:
    #         phone: 手机号
    #     """
    #     try:
    #         try:
    #             self.device.find_element_by_id('com.qiyi.video:id/my_main_login', timeout=10).click()
    #             time.sleep(2)
    #         except:
    #             if self.logout():
    #                 self.device.find_element_by_id('com.qiyi.video:id/title_bar_left').click()
    #                 time.sleep(1)
    #             self.device.find_element_by_id('com.qiyi.video:id/my_main_login', timeout=10).click()
    #             time.sleep(2)
    #     except:
    #         return False
    #
    #     # 手机号
    #     try:
    #         # self.device.find_element_by_xpath("//android.widget.EditText@[@text='请输入您的手机号']", timeout=10).send_keys(phone)
    #         self.device.find_element_by_id('com.qiyi.video:id/et_phone', timeout=5).send_keys(phone)
    #     except Exception as e:
    #         pass
    #
    #     self.device.adb.rm_ipecker_log_file()
    #     try:
    #         self.device.find_element_by_xpath("//android.widget.TextView[@text='获取短信验证码']", timeout=10).click()
    #         time.sleep(1)
    #     except:
    #         pass
    #
    #     # 切换到android输入法
    #     self.device.adb.adb_shell('ime set com.android.inputmethod.latin/.LatinIME')
    #     # 移除日志
    #     data_list = self._get_sms_from_ipecker_log()
    #
    #     ret = False
    #
    #     for data in data_list:
    #         g_logger.info(data)
    #         try:
    #             # for i, char in enumerate(data):
    #             #     id_n = "com.qiyi.video:id/enter_pwd_block%d" % (i + i)
    #             #     self.device.find_element_by_id(id_n).send_keys(char)
    #             id_e = 'com.qiyi.video:id/enter_pwd_edits'
    #             self.device.find_element_by_id(id_e).send_keys(data)
    #             try:
    #                 self.device.find_element_by_id('com.qiyi.video:id/my_main_vip_name')
    #                 ret = True
    #                 break
    #             except:
    #                 # 短信码不正确 继续下次验证码循环
    #                 try:
    #                     self.device.find_element_by_xpath("//android.widget.TextView[@text='验证码不匹配']")
    #                     self.device.find_element_by_id('com.qiyi.video:id/confirm_btn').click()
    #                     time.sleep(2)
    #                     ret = True
    #                     break
    #                 except:
    #                     break
    #         except Exception as e:
    #             continue
    #
    #     # 切回appium输入法
    #     self.device.adb.adb_shell('ime set io.appium.android.ime/.UnicodeIME')
    #     return ret
    #
    # def _get_sms_from_ipecker_log(self):
    #     for i in range(30):
    #         ipecker_log = '/sdcard/ipecker_log.txt'
    #         if self.device.adb.check_file_exist(ipecker_log):
    #             out = "".join(self.device.adb.adb_shell("cat {}".format(ipecker_log)))
    #             import re
    #             data_list = re.findall(r'短信验证码是(\d{6})', out)
    #             if data_list:
    #                 return data_list
    #         time.sleep(1)
    #
    # def start_ipecker_app(self):
    #     """
    #     启动ipecker app
    #     """
    #     # 安装ipecker apk
    #     if not self.device.adb.check_app_is_install('com.iqiyi.ipecker'):
    #         self.device.adb.install_ipecker_apk()
    #     # 启动ipecker apk
    #     self.device.adb.start_app('com.iqiyi.ipecker', '.MainActivity')
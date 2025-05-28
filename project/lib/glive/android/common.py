# -*- coding: UTF-8 -*-

"""
File Name:      common
Author:         zhangwei04
Create Date:    2019/6/5
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread
from appium.webdriver.common.touch_action import TouchAction
from framework.exception.exception import TimeoutException
from .producerdevice import ProducerDevice


class Common(ProducerDevice):
    """通用Common类"""

    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

        self.target = target
        self.data = target.data
        self.device = target.device

        def into_game_show(self, new_game="新游", poker=None):
            """
            从推荐页面中基线进入游戏直播中心
            Args:
                new_game: 游戏中心新游元素
                poker: 游戏中心棋牌游戏
            Returns:
                True: 进入成功
                False：进入失败
             """

            time.sleep(10)
            for i in range(3):
                try:
                    self.device.click_by_id(self.conf.base_recommend.id, timeout=5, desc="点击基线推荐tab")
                    # self.device.click_textview_text("首页", timeout=5)
                    time.sleep(3)
                    ele = self._stable_element(xpath=self.conf.base_recommend_gamecenter.xpath, timeout=30)
                    if ele:
                        ele.click()
                        time.sleep(10)
                    else:
                        # 未找到游戏中心按钮
                        continue
                    for i in range(2):
                        try:
                            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(new_game), timeout=10)
                            break
                        except:
                            ret = self._click_home_woman_known()
                            ret = self._click_home_full_screen_close() or ret
                            if ret:
                                self.gc_floating_flag = True
                                continue
                            else:
                                break

                    # 点掉首页悬浮框
                    if self.gc_floating_flag:
                        try:
                            self.device.click_by_id(self.conf.home_floating.id_close, desc="点掉首页悬浮框", timeout=2)
                            time.sleep(2)
                        except:
                            pass
                        finally:
                            self.gc_floating_flag = False
                    return True
                except Exception as e:
                    self.gc_floating_flag = True  # 进入游戏中心首页失败，需要点掉首页悬浮框
                    if self.device.click_textview_text("同意并继续", timeout=3):
                        time.sleep(5)
                        if self.device.get_manufacturer() == 'xiaomi':
                            try:
                                self.device.click_by_xpath(self.conf.common_button.xpath_allow, timeout=5)
                                time.sleep(1)
                                continue
                            except:
                                pass
                        continue
                    if self.device.get_manufacturer() == 'xiaomi':
                        try:
                            self.device.click_by_xpath(self.conf.common_button.xpath_allow, timeout=5)
                            time.sleep(1)
                            continue
                        except:
                            pass

                    try:
                        self.device.click_by_xpath(self.conf.base_recommend_gamecenter_plugin.xpath, timeout=5, desc="点击游戏中心安装插件")
                        time.sleep(5)
                    except:
                        pass
                    try:
                        self.device.click_by_xpath("//android.widget.TextView[@text='点击进入']", timeout=5, desc="点击进入按钮")
                        time.sleep(3)
                        continue
                    except:
                        pass
                    try:
                        self.device.click_by_xpath("//android.widget.TextView[@text='安装']", timeout=5, desc="点击安装TextView插件")
                        time.sleep(5)
                        ret = self._click_home_woman_known(timeout=30)
                        ret = self._click_home_full_screen_close() and ret
                        if ret:
                            time.sleep(2)
                            return True
                        else:
                            continue
                    except:
                        try:
                            self.device.click_by_xpath("//android.widget.Button[@text='安装']", timeout=2, desc="点击安装Button插件")
                            time.sleep(5)
                            ret = self._click_home_woman_known(timeout=30)
                            ret = self._click_home_full_screen_close() and ret
                            if ret:
                                time.sleep(2)
                                return True
                            else:
                                continue
                        except:
                            pass
                    # 升级提示
                    try:
                        self.device.click_by_xpath(self.conf.base_upgrade_close.xpath, timeout=5, desc="点击暂不升级按钮")
                        time.sleep(1)
                        continue
                    except:
                        pass
                    # 点掉开启推送通知
                    try:
                        self.device.click_textview_text("暂时不要", timeout=5)
                        time.sleep(1)
                        continue
                    except:
                        pass
            else:
                g_logger.error("into gamecenter failed")
                self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "into_gamecenter_{}_failed.png".format(g_resource['testcase_loop'])))
                return False
            return True

        def _stable_element(self, xpath=None, id=None, timeout=30):
            """
            确认元素是稳定的，返回元素
            Args:
                xpath: 查找元素的xpath
                id: 查找元素的id
                timeout: 超时
            Returns:
                ele: 元素， False: 查找失败
            """
            if not xpath and not id:
                g_logger.error("函数：_stable_element，请输入xpath或者id")
                return False
            last_location = None
            time_start = time.time()
            while timeout > time.time() - time_start:
                try:
                    if xpath:
                        ele = self.device.find_element_by_xpath(xpath, timeout=5)
                    else:
                        ele = self.device.find_element_by_id(id, timeout=5)
                    if ele.location == last_location:
                        return ele
                    else:
                        last_location = ele.location
                    time.sleep(3)
                except:
                    pass
            return False

        def into_download_manager(self):
            """
            从游戏中心首页进入下载管理器
            Returns:
                True：进入成功
                False：进入失败
            """
            try:
                self.device.click_by_id(self.conf.gamecenter_download_manager_button.id, timeout=5, desc="点击下载管理器按钮")
                time.sleep(2)
            except:
                return False
            return True

        def back_to_homepage(self, timeout=120):
            """
            返回游戏中心首页
            Args:
                timeout: 超时
            Returns:
                True: 进入成功
                False：进入失败
            """
            time_start = time.time()
            while timeout > time.time() - time_start:
                if self.target.HomePage.check_ui(10):
                    return True
                try:
                    self.device.click_by_id("com.qiyi.gamecenter:id/common_title_back", timeout=10, desc="点击返回按钮")
                    time.sleep(1)
                except:
                    return False
            return False

        def get_location_by_xpath(self, xpath, timeout=5):
            """
            得到元素xpath的坐标
            Args:
                xpath: 元素的xpath
            Returns:
                True: 进入成功
                False: 进入失败
            """
            try:
                obj = self.device.find_element_by_xpath(xpath, timeout=timeout)
                x = obj.location['x']
                y = obj.location['y']
                return x, y
            except Exception as e:
                raise e

        def _swipe_down_check_text(self, text, timeout=5):
            """
            向下滑动检查文本信息,通过TextView对象xpath查找
            Args:
                text: 文本描述
            Returns:
                True: 进入成功
                False：进入失败
            """
            time.sleep(3)
            size = self.device.get_window_size()
            width = size.get('width')
            height = size.get('height')

            # 滑动查找某个按钮
            time_start = time.time()
            while timeout > time.time() - time_start:
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(text), timeout=2)
                    time.sleep(2)
                    return True
                except:
                    self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                    time.sleep(1)
            return False

        def check_title(self, title, timeout=120):
            """
            检查标题, 有一个满足要求就返回成功
            Args:
                title: 标题名
            Returns:
                True: 进入成功
                False：进入失败
            """
            time.sleep(3)
            size = self.device.get_window_size()
            width = size.get('width')
            height = size.get('height')

            title_list = title if isinstance(title, list) else [title]
            # 滑动查找某个按钮
            time_start = time.time()

            while timeout > time.time() - time_start:
                for te in title_list:
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(te), timeout=3)
                        time.sleep(2)
                        return True
                    except:
                        pass
                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                time.sleep(1)
            return False

        def check_web_view_by_id(self, webview_id):
            """
            通过webView的ID检测web是否存在
            Args:
                webview_id: webView的ID
            Returns:
                True: 找到webview的ID， False: 没有找到
            """
            for i in range(3):
                try:
                    self.device.find_element_by_id(webview_id, timeout=5)
                    return True
                except:
                    time.sleep(2)

            return False

        def check_h5_web_side(self):
            """
            通过游戏中心WebView的id检查是否进入H5页面
            Returns:
                True: 进入， False: 没有进入
            """
            return self.check_web_view_by_id(self.conf.gamecenter_game_webview.id)

        def check_title_xpath(self, action_bar_title):
            """
            检查登录后跳转的页面标题
            Args:
                action_bar_title: 按钮名
            Returns:
                True: 进入成功
                False：进入失败
            """
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(action_bar_title), timeout=5)
            except:
                return False
            return True

        def click_and_check_button(self, button_name, text):
            """
            点击图标
            Args:
                button_name: 被点击的按钮
                text: 页面标题
            Returns:
                True: 进入成功
                False：进入失败
            """
            try:
                self.device.click_by_xpath("//android.widget.Button[@text='{}']".format(button_name), timeout=5)
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(text), timeout=5)
            except:
                return False
            return True

        def click_title(self, title):
            """
           点击标题
            Args:
                title: 被点击的标题
            Returns:
                True: 进入成功
                False：进入失败
            """
            try:
                time.sleep(2)
                self.device.click_by_xpath("//android.widget.TextView[@text='{}']".format(title), timeout=5)
                time.sleep(2)
            except Exception as e:
                return False
            return True

        def click_and_check(self, user, actionBar_title):
            """点击图标并查看页面标题
             Args:
                user: 被点击的按钮
                actionBar_title: 页面标题
            Returns:
                True: 进入成功
                False：进入失败
            """
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(user), timeout=5).click()
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(actionBar_title), timeout=5)
                time.sleep(3)
            except Exception as e:
                return False
            return True

        def click_right_arrow(self, text):
            """
            点击图标并查看页面标题
            Args:
                text: 页面标题
            Returns:
                True: 进入成功
                False：进入失败
            """
            try:
                time.sleep(2)
                self.device.click_by_id("com.qiyi.gamecenter:id/vip_info_gold_right_arrow", timeout=5)
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(text), timeout=5)
            except Exception as e:
                return False
            return True

        def push_gamecenter_apk(self, apk_path=""):
            """
            将游戏中心apk push到手机sdcard目录下
            Args:
                apk_path: apk路径
            Returns:
                True: push成功
                False：push失败
            """
            pak_name = 'com.qiyi.gamecenter.apk'
            log_name = 'com.qiyi.gamecenter.log'
            if not os.path.exists(apk_path):
                # 没有传入apk路径则从project/app_pkg目录下查找apk
                apk_path = os.path.join(g_resource['project_path'], "app_pkg", pak_name)
            self.device.adb.push_file(apk_path, "/sdcard/{}".format(pak_name))

            log_path = os.path.join(g_resource['project_path'], "app_pkg", log_name)
            if not self.device.adb.check_file_exist(log_name, '/sdcard'):
                self.device.adb.push_file(log_path, '/sdcard/{}'.format(log_name))

            # 获取游戏中心插件版本号
            version = self.get_app_version_from_apk(apk_path)
            g_resource['aml_data']['environment']['gc_version'] = version if version else ""

        def ansy_catch_ad(self):
            """异步方式抓取广告，找至游戏中心"""
            self._thread_ad = IpeckerThread()
            self._start_thread_flag = True
            self._thread_ad.start(self.ansy_click_ad)

        def stop_catch_ad(self):
            if self._thread_ad:
                self._start_thread_flag = False

        def ansy_click_ad(self):
            """ 异步方式点掉广告页，点击到游戏中心"""
            base_install_agree = False  # 同意并运行
            gc_add_to_desktop_flag = False  # 游戏中心添加到桌面
            gc_woman_known_flag = False  # 女生版切换弹窗
            gc_full_screen_flag = False  # 全屏弹窗
            gc_floating_flag = False  # 首页悬浮窗

            while self._start_thread_flag:
                # 点掉安装时允许隐私政策安装
                if not base_install_agree:
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='同意并继续']", timeout=2).click()
                        # base_install_agree = True # 会有弹出2次的情况，此行注释掉
                    except:
                        pass
                if self.device.get_manufacturer() == 'xiaomi':
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_allow, timeout=5)
                        time.sleep(1)
                    except:
                        pass
                # 处理页面无法捕获到的
                # pic_tmp_path = os.path.join(self.conf_img_dir, "screen.png")
                # student_vip_path = os.path.join(self.conf_img_dir, "student_vip.png")
                # self.device.get_screenshot_as_file(pic_tmp_path)
                # if self.match_image(student_vip_path, pic_tmp_path):
                #     # 匹配到 学生VIP活动页面，使用坐标方式点掉
                #     self.device.tap([(540, 1650)])

                # 添加快捷方式到桌面
                if not gc_add_to_desktop_flag:
                    if self.device.get_manufacturer() == 'google':
                        xpath_add = "//android.widget.Button[@text='自动添加']"
                        try:
                            self.device.click_by_xpath(xpath_add, timeout=5)
                            gc_add_to_desktop_flag = True
                        except:
                            pass
                    else:
                        gc_add_to_desktop_flag = self._click_add_to_desktop()  # 更换成图像匹配方式
                    time.sleep(3)

                # 首页处理弹出女生版知道了
                if not gc_woman_known_flag:
                    gc_woman_known_flag = self._click_home_woman_known()  # 图像匹配方式，防止捕获元素卡死

                # 首页匹配弹出全屏
                if not gc_full_screen_flag:
                    try:
                        self.device.find_element_by_id(self.conf.ad_frame_full_image.id, timeout=2)
                        self.device.find_element_by_id(self.conf.ad_frame_close_button.id, timeout=2).click()
                        gc_full_screen_flag = True
                    except:
                        pass
            g_logger.info("stop catch ad thread")

        def _click_home_woman_known(self, timeout=5):
            """
            图像匹配方式点掉女生弹窗知道了
            Args:
                timeout: 超时
            Returns:
                True: 点击掉成功, False: 点击掉失败
            """
            height = self.device.get_window_height()
            if height == 1280:
                woman_pic = "woman_known_1280.png"
            elif height in (2712, 2880):
                woman_pic = "woman_known_2880.png"
            else:
                woman_pic = "woman_known.png"
            woman_known_path = os.path.join(self.conf_img_dir, woman_pic)
            return self._click_screen_from_pic(woman_known_path, timeout=timeout)

        def _click_home_full_screen_close(self):
            try:
                time.sleep(2)
                g_logger.info("查找全屏弹窗全屏id")
                # self.device.find_element_by_id(self.conf.ad_frame_full_image.id, timeout=2)
                self.device.click_by_id(self.conf.ad_frame_close_button.id, desc="点击全屏弹窗关闭", timeout=2)
                time.sleep(1)
                return True
            except:
                g_logger.info("查找全屏弹窗全屏id失败")
                return False

        def _click_add_to_desktop(self, timeout=5):
            """
            图像匹配方式点掉添加至桌面
            Args:
                timeout: 超时
            Returns:
                True: 点击掉成功, False: 点击掉失败
            """
            if self.device.get_manufacturer() == "google":
                add_desktop_path = os.path.join(self.conf_img_dir, "google_add_desktop.png")
            else:
                add_desktop_path = os.path.join(self.conf_img_dir, "huawei_add_desktop.png")
            return self._click_screen_from_pic(add_desktop_path, timeout=timeout)

        def install_base_apk(self, timeout=120):
            """安装基线apk"""
            self.push_gamecenter_apk()
            # 清空残留文件
            self.device.adb.adb_shell("rm -rf /storage/emulated/0/.qiyi/*", console=False)
            self.device.adb.adb_shell("rm -rf /storage/emulated/0/qiyivideo_local/*")

            # 安装基线版本号
            manu = self.device.get_manufacturer()
            if manu == 'vivo':
                if not self.vivo_install_apk("iqiyi.apk", uninstall_flag=True, timeout=timeout):
                    return False
                self.device.adb.start_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")
                self._vivo_click_apk_authority()
                self.key_event("KEYCODE_HOME")
                self.device.adb.start_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")
                time.sleep(2)
            elif manu == 'oppo':
                if not self.oppo_install_apk("iqiyi.apk", uninstall_flag=True, timeout=timeout):
                    return False

                self.device.adb.start_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")
                for i in range(1):
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_allow, desc='点击允许按钮', timeout=5)
                        time.sleep(1)
                    except:
                        break
            elif manu == 'xiaomi':
                if not self.xiaomi_install_apk("iqiyi.apk", uninstall_flag=True, timeout=240):
                    return False
                self.device.adb.start_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")
                time.sleep(1)

            else:  # 华为、google等手机
                self.install_apk("iqiyi.apk", uninstall_flag=True)
                self.device.adb.start_app("com.qiyi.video", "com.qiyi.video.WelcomeActivity")

            apk_path = os.path.join(g_resource['project_path'], "app_pkg", "iqiyi.apk")
            version = self.get_app_version_from_apk(apk_path)
            g_resource['aml_data']['environment']['base_version'] = version if version else ""

        def base_search_and_play_video(self, search_content):
            """
            基线寻找视频，并播放视频
            Args:
                search_content: 查找的视频关键字

            Returns:
                True: 查找成功 False: 查找失败
            """
            time.sleep(10)
            try:
                self.device.find_element_by_id(self.conf.base_search_text.id, timeout=10).click()
                self.device.find_element_by_id(self.conf.base_search_into_text.id, timeout=10).set_text(search_content)
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(search_content), timeout=10).click()
                time.sleep(2)
                self.device.find_element_by_xpath(self.conf.base_video_play_button.xpath, timeout=5).click()
                time.sleep(2)
                return True
            except:
                return False

        def _base_video_ad_find_game(self, xpath):
            # self.conf.base_game_download_button.xpath
            try:
                # 获取元素的坐标位置
                ele = self.device.find_element_by_id(self.conf.base_video_play_ad_recycler.id)
                coordinate = ele.location
                size = ele.size

                y = coordinate['y'] + size['height'] / 2
                x_start = (coordinate['x'] + size['width']) * 3 / 4
                x_end = (coordinate['x'] + size['width']) * 1 / 4
                self.device.slide_timeout_find_element_by_xpath(xpath, x_start, x_end, y, y, timeout=30)
                return True
            except Exception as e:
                g_logger.error("基线视频广告位查找游戏失败")
                return False

        def base_video_ad_view_download_game(self):
            self._base_video_ad_find_game(self.conf.base_game_download_button.xpath)
            try:
                self.device.find_element_by_xpath(self.conf.base_game_download_button.xpath, timeout=5).click()
            except:
                g_logger.error("未找到游戏下载按钮")
                return False
            return self.huawei_install_app()

        def base_video_ad_detail_download_game(self, game_title):
            xpath = "//android.widget.TextView[@text='{}']".format(game_title)
            self._base_video_ad_find_game(xpath)
            try:
                self.device.find_element_by_xpath(xpath, timeout=5).click()
                self.device.find_element_by_id(self.conf.base_game_detail_download_button, timeout=5).click()
            except:
                g_logger.error("游戏详情页下载游戏失败")
                return False

            return self.huawei_install_app()

        def back_page(self):
            self.device.adb.adb_shell("input keyevent 4")
            time.sleep(2)

        def click_installed_confirm_guide(self, open_game=False, timeout=60):
            """
            安装完成时，游戏中心会弹出确认界面，6.11.0加入此功能
            Args:
                open_game: 是否是打开游戏,默认点击“我知道了”不打开游戏
                timeout: 查找标题的超时，一般是游戏的安装时间
            Returns:
                True:找到元素并点击， False：未找到元素
            """
            time_start = time.time()

            mobile_product = self.device.get_manufacturer()

            if mobile_product == 'vivo':
                # vivo 点击系统打开页面
                xpath = self.conf.common_button.xpath_open if open_game else self.conf.common_button.xpath_done
                while timeout > time.time() - time_start:
                    try:
                        self.device.click_by_xpath(xpath=xpath, timeout=10)
                        time.sleep(2)
                        break
                    except Exception as e:
                        continue
                else:
                    g_logger.error("vivo查找xpath失败：{}".format(xpath))
                    return False
            else:
                while timeout > time.time() - time_start:
                    try:
                        self.device.find_element_by_xpath(self.conf.game_installed_guide.title_xpath, timeout=2)
                        break
                    except Exception as e:
                        continue  # 继续查找元素
                else:
                    g_logger.error("查找标题失败：{}".format(self.conf.game_installed_guide.title_xpath))
                    return False

                # 通过元素id点击"我知道了"或者"打开游戏"
                id_path = self.conf.game_installed_guide.open_id if open_game else self.conf.game_installed_guide.confirm_id
                try:
                    self.device.click_by_id(id_path, timeout=10)
                    time.sleep(2)
                except Exception as e:
                    g_logger.error("查找id失败：{}".format(id_path))
                    return False

            if open_game:  # 打开游戏
                time.sleep(3)  # 等待3秒游戏载入
                if mobile_product == "xiaomi":
                    ui_version = self.device.get_ui_version()
                    if ui_version > '6.0.1':
                        try:
                            self.device.click_by_xpath(self.conf.game_download_xiaomi_permit.xpath, timeout=30)
                        except:
                            g_logger.warning("小米手机打开游戏 未找到允许按钮")
                            # TODO 小米手机安装好游戏之后，打开游戏，没有找到允许按钮，可能会有异常需要处理
                            # 第一次安装游戏需要权限，后面不需要
                            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "not_found_permit.png"))
                    else:
                        for i in range(4):
                            try:
                                self.device.click_by_xpath(self.conf.common_button.xpath_allow, timeout=10)
                                time.sleep(2)
                            except:
                                break

                elif mobile_product in ("huawei", "google"):
                    for i in range(5):
                        try:
                            self.device.click_by_id(self.conf.game_download_huawei_permit.id_allow_button, timeout=5)
                        except:
                            break
                elif mobile_product in ("vivo"):
                    for i in range(2):
                        try:
                            self.device.click_by_xpath(self.conf.common_button.xpath_allow, desc='点击允许', timeout=5)
                            time.sleep(2)
                        except:
                            break
            else:  # 不打开游戏，点掉系統完成页面
                if mobile_product in ("huawei", "google", 'xiaomi'):
                    self.cmd_back()
                elif mobile_product == 'oppo':
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_done, desc='点击系统安装完成页面完成按钮', timeout=5)
                        time.sleep(2)
                    except:
                        pass

            return True

        def clear_app_data(self, package="com.qiyi.video", launch_app=False, app_name='爱奇艺'):
            """
            清除app数据，清除后授权
            Args:
                package: app包名
                launch_app: 是否加载App
                app_name: app名称
            Returns:
                True: 清除数据成功， False: 清除数据失败
            """
            self.device.adb.clear_app_data(package)
            time.sleep(1)
            self.device.adb.grant(package=package)  # iqiyi默认授权：申请存储、位置和手机相关的权限
            time.sleep(1)
            if launch_app:
                self.device.launch_app()
                time.sleep(2)
                self.device.click_textview_text("同意并继续", timeout=5)
            return True

        def into_game_center_without_check(self):
            """
            进入游戏中心，不检测游戏中心UI
            Returns:
                True:进入游戏中心(未检测)， False: 查找游戏中心按钮失败
            """
            clicke_allow = self.device.click_textview_text("同意并继续", timeout=10)
            if self.device.get_manufacturer() == 'xiaomi':
                for i in range(3):
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_allow, timeout=5)
                        time.sleep(1)
                    except:
                        break
                if not clicke_allow:
                    self.device.click_textview_text("同意并继续", timeout=5)
                g_logger.info("小米手机 先睡眠20秒")
                time.sleep(20)

            g_logger.info("等待20秒，待游戏中心插件加载结束")
            time.sleep(20)

            try:
                g_logger.info("向下滑动，刷新首页，若有弹窗则此步骤无效")
                self.device.swipe_screen(rate=0.1, direction='down')
                time.sleep(2)
            except:
                pass
            ele = self._stable_element(xpath=self.conf.base_recommend_gamecenter.xpath, timeout=30)
            if ele:
                ele.click()
                time.sleep(5)
            else:
                g_logger.error("点击游戏中心失败")
                return False

            if self.device.click_textview_text("点击进入", timeout=5):
                time.sleep(6)

            self._click_add_to_desktop()
            # self._add_shortcut_desktop_into_gc()

            # 增加遗留完成界面点击
            # self._click_leave_installed_page()
            return True

        def _add_shortcut_desktop_into_gc(self):
            """
            点掉添加至桌面，再进入游戏中心
            Returns:

            """
            # 点掉添加至桌面
            self._click_add_to_desktop()
            # try:
            #     self.device.find_element_by_xpath(self.conf.gamecenter_add_to_desktop_title.xpath, timeout=5)
            #     self.device.find_element_by_xpath(self.conf.gamecenter_add_to_desktop_button.xpath, timeout=2).click()
            #     time.sleep(2)
            # except:
            #     return True
            try:
                self.device.click_by_xpath(self.conf.base_recommend_gamecenter.xpath, timeout=10)
                time.sleep(5)
            except:
                pass

            return True

        def _click_leave_installed_page(self, timeout=30):
            """
            点击掉前面安装完成的遗留界面
            Returns:
                True: 点击掉成功, False: 点击掉失败
            """
            manu = self.device.get_manufacturer()
            if manu == "huawei":
                time_start = time.time()
                while timeout > time.time() - time_start:
                    if self.device.check_textview_text("安装成功", timeout=10):
                        try:
                            self.device.click_by_xpath("//android.widget.Button[@text='完成']", timeout=5)
                            time.sleep(1)
                        except:
                            g_logger.warning("点掉安装完成遗留界面：检测到安装完成，但未找到完成按钮")
                            return False
                    else:
                        break

            return True

        def game_install(self, game_name: str, open_game=False, confirm_guide=True, click_last_installed=True, close_game=True, button_xpath=None,
                         button_id=None, timeout=240):
            """
            游戏下载, 同一手机不能异步同时调用此方法，会导致包名和游戏名不匹配
             Args:
                game_name: 游戏名称，用于添加游戏映射
                open_game: 安装完成后是否打开游戏
                confirm_guide: 安装完成后是否有游戏中心弹窗
                click_last_installed: 是否点击掉前面遗留的安装完成页面
                close_game: 是否关闭游戏， 需要open_game为True时才判断执行
                button_xpath: 安装按钮xpath
                button_id: 安装按钮id
                timeout: 下载超时
             Returns:
               True: 进入成功
               False：进入失败
             """
            set1 = set(self.device.adb.adb_shell('pm list packages', log=False))

            mobile_product = self.device.get_manufacturer()
            if mobile_product == "huawei":
                if not self.huawei_game_download_and_install(timeout=timeout, click_last_installed=click_last_installed):
                    return False
            elif mobile_product == "xiaomi":
                self.xiaomi_game_download_and_install(timeout=timeout)
            elif mobile_product == 'vivo':
                if not self.vivo_game_download_and_install(timeout=timeout, button_id=button_id, button_xpath=button_xpath):
                    return False
            elif mobile_product == 'oppo':
                if not self.oppo_game_download_and_install(timeout=timeout, button_id=button_id, button_xpath=button_xpath, ):
                    return False
            elif mobile_product == 'google':
                if not self.google_game_download_and_install(timeout=timeout):
                    return False
            else:
                g_logger.error("{}手机游戏下载暂不支持".format(mobile_product))
                return False
            if confirm_guide:
                self.click_installed_confirm_guide(open_game)  # 点击游戏中心插件弹出的完成界面

            set2 = set(self.device.adb.adb_shell('pm list packages', log=False))

            self.update_installed_app_name(set1, set2, game_name)
            if open_game:
                self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "{}_open.png".format(game_name)))
                time.sleep(5)
                if close_game:
                    self.close_installed_app(game_name)

            return True

        def update_installed_app_name(self, set1, set2, game_name):
            """
            获取安装的app名称
            Args:
                set1: app安装前设备的全部package集合
                set2: app安装后设备的全部package集合
            Returns:
                app列表， False: 失败
            """
            se = set1 ^ set2
            if len(se) != 1:
                g_logger.info("游戏已安装:{}".format(game_name))
                return False
            game_app_pkg_info = se.pop().split(":")[1]
            self.installed_app_dict[game_name] = game_app_pkg_info
            return True

        def close_installed_app(self, game_name):
            """
            关闭刚下载的app
            Args:
                game_name: app安装前设备的全部package集合
            Returns:
                True: 进入成功
                False：进入失败
            """
            self.device.adb.stop_app(self.installed_app_dict.get(game_name, game_name))

        def game_detail_download(self):
            """
            游戏详情页-游戏下载
            Returns:
                True:点击了游戏下载，False: 未找到下载按钮
            """
            time.sleep(2)
            try:
                self.device.click_by_id(self.conf.gamecenter_game_download_installation.id, timeout=10, desc="点击下载按钮")
                time.sleep(5)
                return True
            except:
                g_logger.info("查找下载按钮id超时")
                return False

        def uninstall_game(self, game_name):
            """根据游戏名卸载游戏，需要传入游戏名调用过安装app的接口"""
            return self.uninstall_app(app_name=game_name)

        def uninstall_app_from_conf(self, app_name):
            """
            卸载app，从游戏配置文件里面读取游戏包
            Args:
                app_name: app名，对应配置文件里面的section名
            Returns:
                True: 卸载成功
            """
            app_pkg = self.app_conf.get(app_name, "package")
            if app_pkg and self.device.adb.check_app_is_install(app_pkg):
                self.uninstall_app(app_pkg=app_pkg)
            return True

        def uninstall_game_from_conf(self, game_name):
            """
            卸载游戏，从游戏配置文件里面读取游戏包
            Args:
                game_name: 游戏名，对应配置文件里面的section名
            Returns:
                True: 卸载成功
            """
            return self.uninstall_app_from_conf(game_name)

        def uninstall_app(self, app_pkg=None, app_name=None, all_flag=False):
            """
            卸载app，若传入app参数，先查找是否是自动化安装的app，若是则在installed_app_list移除
            Args:
                app_pkg: app安装至手机后的名称
                app_name: app名称，如游戏中心的游戏名
                all_flag: 是否移除自动化全部安装的apk
            Returns:
            """
            if all_flag:
                for key_app_name in self.installed_app_dict:
                    self.device.adb.uninstall_app(self.installed_app_dict[key_app_name])
                self.installed_app_dict.clear()

            if app_pkg:
                for key_app_name in self.installed_app_dict:
                    if app_pkg == self.installed_app_dict[key_app_name]:
                        self.installed_app_dict.pop(key_app_name)
                self.device.adb.uninstall_app(app_pkg)

            if app_name:
                app_pkg = self.installed_app_dict.get(app_name, None)
                if app_pkg:
                    self.device.adb.uninstall_app(app_pkg)

            return True

        def check_click_video_template_play_button(self, game_name):
            """
            检测视频模板运营位的播放按钮,并点击
            Args:
                game_name: 带视频游戏名
            Returns:
                True: 检测成功
                False: 检测失败
            """
            video_xpath = self.conf.gamecenter_video.xpath.format(game_name)
            video_play_xpath = self.conf.video_play.xpath.format(game_name)
            if not self.device.swipe_down_find_ele(xpath=video_xpath, timeout=60):
                g_logger.error("查找游戏视频失败")
                return False
            for i in range(20):
                try:
                    ele = self.device.find_element_by_xpath(video_play_xpath, timeout=2)  # 若不是自动播放，则会有播放按钮
                    g_logger.info("找到视频模块播放按钮，点击")
                    self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video.png"))
                    location = ele.location
                    size = ele.size
                    g_logger.info("元素位置：{}".format(location))
                    x, y = location['x'] + size['width'] / 2, location['y'] + size['height'] / 2
                    # ele.click()
                    self.device.tap([(x, y)])
                    time.sleep(2)
                    # self.device.tap([(x, y)])

                    return True
                except:
                    # if i == 0:
                    #     seconds = self.get_video_play_time(video_xpath=video_xpath)
                    #     if not seconds:
                    #         return False
                    #     else:
                    #         time.sleep(seconds)
                    time.sleep(5)
            else:
                return False

        def get_video_play_time(self, video_xpath=None, video_id=None):
            """
            获取视频的时长
            Args:
                video_xpath: 视频模块的窗口xpath，用于点击调起底部栏
                video_id: 视频模块的窗口id，用于点击调起底部栏
            Returns:
                seconds: 视频时长(单位：秒)， False: 查找时长失败
            """
            if not video_xpath and not video_id:
                g_logger.warning("请传video_xpath或者video_id")
                return False
            for i in range(2):
                seconds = self._get_video_duration_seconds(self.conf.video_duration_time.id)
                if seconds:
                    return seconds
                else:
                    # 未找到视频时间，需点击视频区域，调起底部栏
                    try:
                        if video_xpath:
                            self.device.click_by_xpath(video_xpath, timeout=5)
                        else:
                            self.device.click_by_id(video_id, timeout=5)
                        time.sleep(0.5)
                    except:
                        g_logger.error("点击视频模块失败")
                        return False

        def _get_video_duration_seconds(self, ele_id, duration_str=None):
            """
            视频播放时长字符串转化为的播放秒数, 若传入了duration_str,则不查找元素，直接处理duration_str字符串
            Args:
                ele_id: 视频时长元素id
                duration_str: 播放时长字符串
            Returns:
                秒数
            """
            # 查找视频时间
            if not duration_str:
                try:
                    duration_time_ele = self.device.find_element_by_id(ele_id, timeout=2)
                    duration_str = duration_time_ele.get_attribute("text")
                except Exception as e:
                    return None

            duration_time_list = duration_str.split(":")
            seconds = 0
            for i, t in enumerate(reversed(duration_time_list)):
                t = int(duration_time_list.pop()) * (60 ** i)
                seconds += t
            return seconds

        def back_common_title(self):
            """
            通用返回按钮
            Returns:
                True: 返回成功， False: 返回失败
            """
            try:
                self.device.click_by_id("com.qiyi.gamecenter:id/common_title_back", desc="点击返回通用返回按钮", timeout=10)
                time.sleep(1)
                return True
            except:
                return False

        def back_gamecenter_title(self):
            """
            游戏中心的返回按钮
            Returns:
                True: 返回成功， False: 返回失败
            """
            try:
                self.device.click_by_id("com.qiyi.gamecenter:id/back", desc="点击游戏中心的返回按钮", timeout=10)
                time.sleep(1)
                return True
            except Exception as e:
                return False

        def click_huge_image(self, image_desc):
            """点击大图"""
            img_desc_xpath = self.conf.huge_image.xpath_desc.format(image_desc)
            ele = self.device.swipe_down_find_ele(xpath=img_desc_xpath, timeout=60)
            if ele:
                ele.click()
                time.sleep(3)
                return True
            else:
                g_logger.error("查找大图：{}失败".format(image_desc))
                return False

        def check_topic_ui(self, topic_title, topic_desc=None):
            """
            检测专题UI
            Args:
                topic_title:
                topic_desc:

            Returns:
                True: 检测成功， False: 检测失败
            """
            try:
                ele = self.device.find_element_by_id("com.qiyi.gamecenter:id/topic_detail_title")
                text = ele.get_attribute("text")
                if text != topic_title:
                    g_logger.error("专题标题匹配失败，期望值：{}，实际值：{}".format(topic_title, text))
                    return False
                g_logger.error("专题标题匹配成功，期望值：{}，实际值：{}".format(topic_title, text))
            except:
                g_logger.error("查找专题标题：{}失败".format(topic_title))
                return False

            if topic_desc:
                try:
                    ele = self.device.find_element_by_id("com.qiyi.gamecenter:id/topic_detail_desc")
                    text = ele.get_attribute("text")
                    if text != topic_desc:
                        g_logger.error("专题描述匹配失败，期望值：{}，实际值：{}".format(topic_desc, text))
                        return False
                    g_logger.error("专题描述匹配成功，期望值：{}，实际值：{}".format(topic_desc, text))
                except:
                    g_logger.error("查找专题描述：{}失败".format(topic_desc))
                    return False

            return True

        def check_horizontal_game_index_in_last(self, title, game_name):
            """
            检测横排游戏在横排的最后面或者不显示
            Args:
                title: 横排标题
                game_name: 游戏名字
            Returns:
                True: 检测成功， False: 检测失败
            """
            game_list = self.horizontal_get_game_list(title)
            try:
                game_index = game_list.index(game_name)
            except:
                if len(game_list) == 10:
                    g_logger.info("横排{}没有找到对应的{}游戏,游戏显示数量为10个".format(title, game_name))
                    return True
                else:
                    g_logger.error("横排{}显示的游戏个数为{}个，且没有找到对应的{}游戏".format(title, len(game_list), game_name))
                    return False
            return game_index == len(game_list) - 1

        def horizontal_get_game_list(self, title):
            game_list = []
            if not self.horizontal_full_on_screen(title):
                return game_list
            time.sleep(5)  # 等待2秒，待页面加载完成
            ele_xpath = self.conf.horizontal_game.title_xpath.format(title)
            swipe_xpath = self.conf.horizontal_game.swipe_ele_xpath.format(title)

            game_list = []
            last_list = []
            for i in range(10):
                eles = self.device.find_elements_by_xpath(ele_xpath, timeout=10)
                if eles:
                    current_list = [ele.get_attribute("text") for ele in eles]
                    game_list.extend([game for game in current_list if game not in game_list])
                    if last_list == current_list:
                        break
                    else:
                        last_list = current_list
                self.device.swipe_ele(swipe_xpath=swipe_xpath, rate=0.6, direction='left')
                time.sleep(5)
            g_logger.info("横排游戏列表：{}".format(", ".join(game_list)))
            return game_list

        def horizontal_into_game_detail(self, title, game_name):
            """
            进入横排游戏的游戏系详情页
            Args:
                title: 横排游戏标题
                game_name: 游戏名
            Returns:
                True: 进入成功， False: 进入失败
            """
            if not self.horizontal_full_on_screen(title):
                return False

            find_xpath = self.conf.horizontal_game.game_name_xpath.format(title, game_name)
            swipe_xpath = self.conf.horizontal_game.swipe_ele_xpath.format(title)
            time.sleep(2)  # 等待页面加载结束
            ele = self.device.swipe_ele_find_ele(swipe_xpath=swipe_xpath, find_xpath=find_xpath, direction="left", stable_ele=True, timeout=40)
            if not ele:
                g_logger.error("{}横排查找{}游戏失败".format(title, game_name))
                return False
            else:
                g_logger.info("横排游戏位置：{}".format(ele.location))
                ele.click()
                time.sleep(3)

            return True

        def horizontal_full_on_screen(self, title):
            """
            滑动到横排游戏列表上下端全部显示出来
            Args:
                title: 横排标题
            Returns:
                True: 全部显示成功， False: 全部显示失败
            """
            if not self.device.check_textview_text(title, swipe=True, timeout=120):
                g_logger.error("查找横排标题：{} 失败".format(title))
                return False

            size = self.device.get_window_size()
            width = size.get('width')
            height = size.get('height')
            for i in range(3):
                try:
                    self.device.find_element_by_xpath(self.conf.horizontal_game.game_download_xpath.format(title), timeout=10)
                    break
                except:
                    self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 2 / 5)
                    time.sleep(2)
            else:
                g_logger.error("横排{}全部显示失败".format(title))
                return False
            return True

        def check_video(self, game_name=None):
            """
            检测视频播放
            Args:
                game_name: 视频游戏名称
            Returns:
                True: 搜索成功
                False: 搜索失败
            """
            # video_xpath = self.conf.video_play.xpath.format(introduction)
            full_screen_flag = False
            try:
                try:
                    self.device.click_by_id(self.conf.video_play_tolandscape.id, timeout=5, desc="点击全屏按钮")
                    time.sleep(0.5)
                except:
                    g_logger.info("底部栏消失，通过坐标点击方式调起底部栏")
                    self.device.tap([(540, 100)])
                    self.device.click_by_id(self.conf.video_play_tolandscape.id, timeout=5, desc="点击全屏按钮")

                full_screen_flag = True

                self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_tolandscape.png"))
                try:
                    self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击暂停按钮")
                except:
                    g_logger.info("底部栏消失，通过坐标点击方式调起底部栏")
                    self.device.tap([(540, 540)])
                    self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击暂停按钮")

                time.sleep(1)
                self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_pause.png"))
                try:
                    self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击播放按钮")
                except:
                    g_logger.info("底部栏消失，通过坐标点击方式调起底部栏")
                    self.device.tap([(540, 540)])
                    # time.sleep(0.2)
                    self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击播放按钮")
                # 退出全屏视频播放
                time.sleep(0.5)
                self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_again.png"))
                self.device.keyevent(4)
                time.sleep(1)
                self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_tolandscape_back.png"))
                return True
            except:
                return full_screen_flag

        def uninstall_gc_app(self):
            """
            adb方式卸载分发app
            Returns:
                True
            """
            return self.uninstall_app(app_pkg=self.conf.gd_gc_app.package)

        def check_desktop_gc(self):
            """
            检测桌面创建了游戏中心快捷方式
            Returns:
            """
            return self.desktop_check_app("爱奇艺游戏中心")

        def check_gc_installed(self):
            """
            命令行检测游戏中心分发app是否已经安装
            Returns:
                True: 已经安装， False: 尚未安装
            """
            return self.check_app_installed("com.qiyi.gcapp")

        def check_gc_update(self):
            """
            检测app更新
            Returns:
            """
            manu = self.device.get_manufacturer()
            if self.check_gc_app_is_installed():
                g_logger.info("检测到已安装分发app, 卸载分发app，安装旧版本的app")
                self.uninstall_gc_app()
            g_logger.info("安装上一个版本的apk")
            self.install_app('com.qiyi.gcapp_last.apk')
            time.sleep(2)
            self.device.adb.stop_app(self.app_conf.iqiyi_base.package)
            time.sleep(1)
            for i in range(2):
                g_logger.info("启动上一个版本的apk")
                self.device.adb.start_app(self.conf.gd_gc_app.package, self.conf.gd_gc_app.activity)
                if manu:
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_allow, timeout=10)
                    except:
                        pass
                time.sleep(6)
                g_logger.info("检测更新提示")
                if self.device.check_textview_text("更新提示", timeout=20):
                    try:
                        self.device.click_by_id('com.qiyi.gamecenter:id/pb_gamebutton', desc="点击立即更新(安装）按钮", timeout=5)
                        time.sleep(3)
                        break
                    except:
                        return False
                else:
                    self.device.adb.stop_app(self.app_conf.iqiyi_base.package)
                    time.sleep(2)
                    self.device.adb.stop_app(self.conf.gd_gc_app.package)
                    time.sleep(2)
            else:
                g_logger.warning("检测更新提示弹窗失败")
                return False

            for i in range(2):
                if self.game_install(game_name=self.conf.gd_gc_app.desc, click_last_installed=False, open_game=False, confirm_guide=False, timeout=30):
                    break

                image_path = os.path.join(self.conf_img_dir, "{}_gc_app_install_button.png".format(self.device.get_window_size().get("height")))
                if not self.cmd_back_and_click_image(image_path):
                    self.desktop_into_app(self.conf.gd_gc_app.name)
                    try:
                        self.device.click_by_id('com.qiyi.gamecenter:id/pb_gamebutton', desc="点击立即更新(安装）按钮", timeout=5)
                        time.sleep(3)
                    except:
                        pass
            if manu == 'xiaomi':
                g_logger.info("小米手机back一步，关闭系统弹出的安装成功页面")
                try:
                    self.device.click_by_xpath(self.conf.common_button.xpath_done, timeout=10)
                    time.sleep(1)
                except:
                    pass

            self.device.adb.stop_app(self.app_conf.iqiyi_base.package)
            time.sleep(1)
            self.device.adb.start_app(self.conf.gd_gc_app.package, self.conf.gd_gc_app.activity, stop_flag=True)
            time.sleep(5)
            try:
                g_logger.info("通过检测新游查看是否处于首页")
                self.device.find_element_by_xpath(self.conf.gamecenter_newgame.xpath, timeout=20)
            except:
                g_logger.info("gc app通过检测新游查看是否处于首页失败")
                g_logger.info("命令行装最新apk包 com.qiyi.gcapp.apk")
                return False

            return True

        def desktop_into_gc(self):
            """
            桌面进入游戏中心app
            Returns:
            """
            return self.desktop_into_app("游戏中心")

        def check_gc_app_is_installed(self):
            """
            adb方式检测app是否安装
            Returns:
                True: 已安装, False: 未安装
            """
            return self.device.adb.check_app_is_install(self.conf.gd_gc_app.package)

        def close_main_app(self):
            """
            关闭主App
            Returns:
                True
            """
            self.device.close_app()
            return True

        def desktop_check_app(self, app_name, timeout=60):
            """
            桌面检查app
            Args:
                app_name: 显示的桌面名称
                timeout: 查找超时

            Returns:
                ele: 查找成功， None:查找失败
            """

            for i in range(2):
                self.device.adb.adb_shell('input keyevent KEYCODE_HOME')
                time.sleep(2)
            app_desktop_xpath = "//android.widget.TextView[@text='{}']".format(app_name)
            if self.device.get_manufacturer() == 'google':
                ele = self.device.up_swipe_find_ele_by_xpath(app_desktop_xpath, rate=0.5, timeout=timeout)
            else:
                ele = self.device.left_swipe_find_ele_by_xpath(app_desktop_xpath, rate=0.7, timeout=timeout)
            return ele

        def desktop_into_app(self, app_name, timeout=30):
            """
            充桌面进入app
            Args:
                app_name: app桌面显示的名称
                timeout: 查找超时
            Returns:
                True: 点击成功, False: 点击失败
            """
            ele = self.desktop_check_app(app_name, timeout=timeout)
            if ele:
                ele.click()
                time.sleep(3)
                return True
            else:
                return False

        def _get_games_from_vertical_game(self, game_name_list, eles_id=None, eles_xpath=None, swipe_xpath=None, swipe_id=None, timeout=120):
            """
            读取纵向列表游戏，并进行比较
            Args:
                game_name_list: 期望游戏列表
                eles_xpath: 查找元素的xpath
                swipe_xpath: 滑动元素的xpath
                swipe_id: 滑动元素的swipe_id
                timeout: 超时
            Returns:
                list: 包含期望游戏里列表的游戏列表 None: 读取失败
            """
            game_name_list = [game_name_list] if isinstance(game_name_list, str) else list(game_name_list)
            time_start = time.time()
            found_game_list = []
            while timeout > time.time() - time_start:
                if eles_xpath:
                    ele_game_list = self.device.find_elements_by_xpath(eles_xpath)
                elif eles_id:
                    ele_game_list = self.device.find_elements_by_id(eles_id)
                else:
                    g_logger.warning("查找列表的eles_xpath失败")
                    break
                if not ele_game_list:
                    break
                else:
                    get_game_list = [ele.get_attribute("text") for ele in ele_game_list]
                found_game_list.extend(get_game_list)
                inters_set = set(get_game_list).intersection(set(game_name_list))  # 交集
                if inters_set:
                    for game_name in inters_set:
                        game_name_list.remove(game_name)
                if not game_name_list:
                    break
                if swipe_xpath or swipe_id:
                    self.device.swipe_ele(swipe_xpath=swipe_xpath, swipe_id=swipe_id, direction="up")
                else:
                    self.device.swipe_screen(direction="up", sleep_time=3)
            return sorted(set(found_game_list), key=found_game_list.index)

        def _get_all_game_from_vertical_game(self, eles_xpath=None, eles_id=None, swipe_xpath=None, swipe_id=None, timeout=150):
            """
            读取纵向列表全部游戏
            Args:
                eles_xpath: 查找元素的xpath
                swipe_xpath: 滑动元素的xpath
                swipe_id: 滑动元素的swipe_id
                timeout: 超时
            Returns:
                list: 全部游戏列表 None: 读取失败
            """
            time_start = time.time()
            found_game_list = []
            refresh_times = 0
            while timeout > time.time() - time_start:

                if eles_xpath:
                    ele_game_list = self.device.find_elements_by_xpath(eles_xpath)
                elif eles_id:
                    ele_game_list = self.device.find_elements_by_id(eles_id)
                else:
                    g_logger.warning("查找列表的eles_xpath失败")
                    break
                if not ele_game_list:
                    break
                else:
                    get_game_list = [ele.get_attribute("text") for ele in ele_game_list]
                    if self._check_list_is_sub(get_game_list, found_game_list):
                        if refresh_times < 3:
                            refresh_times += 1
                        else:
                            break
                    else:
                        refresh_times = 0
                        for game in get_game_list:
                            if game not in found_game_list:
                                found_game_list.append(game)
                if swipe_xpath or swipe_id:
                    self.device.swipe_ele(swipe_xpath=swipe_xpath, swipe_id=swipe_id, direction="up")
                else:
                    self.device.swipe_screen(direction="up", rate=0.2, sleep_time=3)
            return found_game_list

        @staticmethod
        def _check_list_is_sub(src_list, des_list):
            """
            检测ser_list元素是否都在des_list中
            Args:
                src_list: 原列表
                des_list: 目标列表
            Returns:
                True: src_list里面元素包含于des_list
            """
            return set(src_list).issubset(set(des_list))

        def check_game_play(self):
            """
            检测是否在游戏打开页面，使用游戏引擎封装过的游戏
            Returns:
                True: 检测成功, False: 检测失败
            """
            try:
                self.device.find_element_by_xpath(self.conf.play_game_view.xpath, timeout=20)
                return True
            except:
                return False

        def cmd_back_and_find_ele(self, xpath=None, id=None, timeout=60):
            """
            命令行回退,并查找元素
            Args:
                xpath: 查找xpath
                id: 元素查找的id
                timeout: 超时
            Returns:
                ele: 查找到的元素, none:查找失败
            """
            if not xpath and not id:
                g_logger.warning("请传入xpath或者id才进行查找")
                return None
            elif xpath and id:
                g_logger.warning("xpath和id均传入，默认使用xpath查找")

            time_start = time.time()
            while timeout > time.time() - time_start:
                try:
                    if xpath:
                        ele = self.device.find_element_by_xpath(xpath, timeout=5)
                    else:
                        ele = self.device.find_element_by_id(id, timeout=5)
                    return ele
                except:
                    self.key_event("KEYCODE_BACK")
            else:
                g_logger.info("查找超时")
                return False

        def cmd_back_and_click_image(self, image_path, timeout=60):
            """
            命令行返回并点击图片
            Args:
                image_path:图片路径
                timeout: 查找超时
            """
            screen_path = os.path.join(g_resource['testcase_log_dir'], "back_screen.png")
            time_start = time.time()
            while timeout > time.time() - time_start:
                self.device.get_screenshot_as_file(screen_path)
                result = self.match_image(screen_path, image_path, confidence=0.8)
                if result:
                    self.device.tap([result['result']])
                    time.sleep(3)
                    return True
                else:
                    self.cmd_back()
            return False

        def install_app(self, apk_name, uninstall_flag=True):
            """
            安装app
            Args:
                apk_name: apk包名
                uninstall_flag: 是否要卸载
            Returns:

            """
            manu = self.device.get_manufacturer()
            if manu == 'vivo':
                # self.install_apk(apk_name, uninstall_flag=uninstall_flag)
                # return self._vivo_install_input_password()
                # return self.game_install(apk_name, uninstall_flag=uninstall_flag)

                return self.vivo_install_apk(apk_name, uninstall_flag=uninstall_flag)
            elif manu == 'oppo':
                return self.oppo_install_apk(apk_name, uninstall_flag=uninstall_flag)
            elif manu == 'xiaomi':
                return self.xiaomi_install_apk(apk_name, uninstall_flag=uninstall_flag)
            else:
                return self.install_apk(apk_name, uninstall_flag=uninstall_flag)

        def start_ipecker_app(self):
            """
            启动ipecker app
            """
            # 安装ipecker apk
            if not self.device.adb.check_app_is_install(self.app_conf.ipecker.package):
                # self.device.adb.install_ipecker_apk()
                self.install_app('ipecker.apk')
            # 授权
            self.device.adb.grant(permission=["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.READ_EXTERNAL_STORAGE",
                                              "android.permission.READ_PHONE_STATE"], package=self.app_conf.ipecker.package)
            # 启动ipecker apk
            self.device.adb.start_app(self.app_conf.ipecker.package, self.app_conf.ipecker.activity)

        def click_sys_installed_page(self):
            """
            点掉系统安装完成页面
            Returns:
                True
            """
            manu = self.device.get_manufacturer()
            if manu == 'xiaomi':
                try:
                    self.device.click_by_xpath(self.conf.common_button.xpath_done, timeout=10)
                    time.sleep(2)
                except:
                    pass
            return True

# -*- coding: UTF-8 -*-

"""
File Name:      ProducerDevice
Author:         zhangwei04
Create Date:    2019/1/22
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from framework.utils.threads import IpeckerThread
from appium.webdriver.common.touch_action import TouchAction
from framework.exception.exception import TimeoutException


class ProducerDevice(Android):
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.conf_img_dir = os.path.join(g_resource['project_path'], 'conf', 'img', 'gamecenter', 'android')
        self.target = target
        self.data = target.data
        self.device = target.device

        self._async_install_flag = False

    def huawei_install_app(self):
        # 循环等待游戏安装
        for i in range(30):
            try:
                self.device.find_element_by_xpath(self.conf.install_huawei_install_game.xpath, timeout=5).click()
            except:
                time.sleep(5)
                if i == 29:
                    g_logger.error("查找华为手机安装页面安装按钮失败")
                    return False
        # 查找按成安装按钮
        for i in range(10):
            try:
                self.device.find_element_by_xpath(self.conf.install_huawei_done_game.xpath, timeout=5).click()
            except:
                time.sleep(2)
                if i == 9:
                    g_logger.error("查找华为手机安装页面安装成功按钮失败")
                    return False

        return True

    def huawei_click_download_page(self, timeout=60):
        """
        华为手机点掉安装完成页面
        Args:
            timeout:
        Returns:
             True: 点掉成功
        """
        done_xpath = self.conf.common_button.xpath.format("完成")
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                self.device.click_by_xpath(done_xpath, timeout=5)
                time.sleep(1)
            except:
                break
        return True

    def huawei_game_download_and_install(self, timeout=120, click_last_installed=True):
        """
        华为手机游戏下载与安装
        Args：
            timeout: 超时
            click_last_installed: 是否需要点击前面遗留安装完成页面
        Returns:
            True: 进入成功
            False：进入失败
        """
        ui_version = self.device.get_ui_version()
        try:
            if ui_version >= '8.0':
                time_start = time.time()
                while timeout > time.time() - time_start:
                    try:
                        self.device.click_by_xpath("//android.widget.Button[@text='允许']", timeout=5)
                        break
                    except:
                        if click_last_installed:
                            self._huawei_click_last_time_installed_and_install()
                        else:
                            time.sleep(2)
                        continue
                else:
                    g_logger.error("未弹出允许")
                    return False
                # 图像识别继续安装
                continue_img_path = os.path.join(self.conf_img_dir, "huawei_continue_install.png")
                screen_img_path = os.path.join(self.conf_img_dir, "screen.png")
                time_start = time.time()
                while timeout > time.time() - time_start:
                    self.device.get_screenshot_as_file(screen_img_path)
                    cmp_result = self.match_image(screen_img_path, continue_img_path)
                    if cmp_result:
                        self.device.tap([cmp_result['result']], duration=500)
                        time.sleep(5)
                        return True
                    else:
                        time.sleep(3)
                        continue
                else:
                    g_logger.error("未找到继续安装按钮")
                    return False
            else:  # emui版本小于8.0
                time_start = time.time()
                while timeout > time.time() - time_start:
                    try:
                        self.device.click_by_id("com.android.packageinstaller:id/decide_to_continue", timeout=5)
                        time.sleep(2)
                        break
                    except:
                        if click_last_installed:
                            self._huawei_click_last_time_installed_and_install()
                        else:
                            time.sleep(2)
                        continue
                else:
                    g_logger.error("未找到确认风险选项")
                    return False
                # 点掉风险提示，继续安装
                try:
                    self.device.click_by_xpath("//android.widget.Button[@text='继续安装']", desc="继续安装", timeout=10)
                except Exception as e:
                    g_logger.error("点掉风险提示 失败")
                    return False
                # 游戏中心弹出已安装成功页面，点击知道了或者打开
        except Exception as e:
            g_logger.error("点击安装按钮失败")
            return False

        return True

    def _huawei_click_last_time_installed_and_install(self):
        """
        华为手机，点击下载后，会弹出上一次上一次安装完成页面，需要点掉所有安装完成界面，再点击安装按钮
        """
        while True:
            try:
                self.device.click_by_xpath(self.conf.gamecenter_game_download_done.xpath, timeout=3)
                time.sleep(1)
                try:
                    self.device.click_by_id(self.conf.gamecenter_game_download_installation.id, timeout=2, desc="点击下载按钮")
                    time.sleep(3)
                    break
                except:
                    time.sleep(1)
            except:
                break

        return True

    def huawei_installed_confirm(self):
        """安装完成后，会弹出游戏中心的完成和打开界面，此功能界面与游戏中心弹出的界面功能相同，需要确认是否不要
        """
        # 安装成功，授权和点出完成按钮
        for i in range(2):
            try:
                self.device.click_by_xpath("//android.widget.TextView[@text='信任该应用']", desc='点击信任该应用', timeout=5)
                self.device.click_by_xpath("//android.widget.TextView[@text='后台运行']", desc='点击后台运行', timeout=5)
                self.device.click_by_xpath("//android.widget.Button[@text='完成']", desc='点击完成按钮', timeout=5)
                time.sleep(1)
                break
            except Exception as e:
                time.sleep(3)
        else:
            g_logger.error("未找到完成按钮，安装游戏失败")
            return False

        return True

    def xiaomi_game_download_and_install(self, timeout=120):
        """
        小米手机游戏下载
         Args:
        Returns:
            True: 进入成功
            False：进入失败
           """

        # time.sleep(2)
        time_start = time.time()
        ui_version = self.device.get_ui_version()
        if ui_version > '6.0.1':
            while timeout > time.time() - time_start:
                    try:
                        self.device.find_element_by_id(self.conf.gamecenter_game_download_xiaomi.id, timeout=5)
                        time.sleep(5)
                    except:
                        pass
                    try:
                        self.device.click_by_id(self.conf.gamecenter_game_download_xiaomi.id, timeout=5)
                        time.sleep(5)
                        return True
                    except Exception as e:
                        return False
            else:
                g_logger.error("下载超时")
                return False
        else:
            while timeout > time.time() - time_start:
                try:
                    self.device.find_element_by_xpath(self.conf.common_button.xpath_install, timeout=5)
                    time.sleep(3)
                    self.device.click_by_xpath(self.conf.common_button.xpath_install, timeout=5)
                    time.sleep(3)
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_continue_install, timeout=5)
                    except:
                        pass
                    time.sleep(10)
                    break
                except:
                    time.sleep(1)
                    continue
            else:
                g_logger.error("下载超时")
                return False
        return True

    def vivo_install_apk(self, apk_name, uninstall_flag=True, str_flag=False, timeout=120):
        """
        vivo手机命令行方式安装apk
        Args:
            apk_name: 安装apk包名
            uninstall_flag: 是否卸载apk
            str_flag: 命令以字符串方式传入执行
            timeout: 超时
        Returns:
        """
        apk_path = os.path.join(g_resource['project_path'], "app_pkg", apk_name)
        if uninstall_flag:
            self.device.adb.uninstall_app(package=self.get_app_package_from_apk(apk_name))

        _install_thread = IpeckerThread()
        _install_thread.start(self._cmd_async_install, apk_path, str_flag)
        time.sleep(2)
        try:
            self.device.find_element_by_xpath(self.conf.vivo_install.xpath_continue, timeout=15)
            ret_flag = self._vivo_common_part_install()
        except:
            ret_flag = self._vivo_install_input_password()

        if ret_flag:
            time_start = time.time()
            while timeout > time.time() - time_start:
                try:
                    self.device.click_by_xpath(self.conf.vivo_install.xpath_done, desc='点击完成按钮', timeout=5)
                    time.sleep(1)
                    break
                except:
                    time.sleep(1)
            else:
                _install_thread.stop()
                return False
        else:
            _install_thread.stop()
            return False
        for i in range(3):
            if self._async_install_flag:
                return True
            time.sleep(2)
        else:
            _install_thread.stop()
            return False

    def _cmd_async_install(self, apk_path, str_flag):
        """
        vivo线程方式执行adb install命令，否则会阻塞
        Args:
            apk_path: apk路径
            str_flag: 命令以字符串方式传入执行
        """
        self._async_install_flag = False
        self.device.adb.install_apk(apk_path, str_flag=str_flag)
        self._async_install_flag = True

    def _vivo_common_part_install(self, timeout=120):
        """
        vivo 通用安装apk部分流程，包含继续安装、安装
        Returns:
            True:通用流程执行完成，False:执行失败
        """
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                self.device.click_by_xpath(self.conf.vivo_install.xpath_continue, desc="点击继续安装按钮", timeout=5)
                time.sleep(3)
                break
            except:
                time.sleep(2)
        else:
            return False

        try:
            self.device.click_by_xpath(self.conf.vivo_install.xpath_install, desc="点击安装按钮", timeout=20)
            time.sleep(3)
        except:
            return False

        return True

    def _vivo_click_apk_authority(self, timeout=120):
        """
        vivo 启动apk时，会弹出授权相关东西，点掉授权页面
        Returns:
            True: 点击成功或没有弹出授权页
        """
        # time_start = time.time()
        # while timeout > time.time() - time_start:
        #     time.sleep(2)
        #     try:
        #         self.device.click_by_xpath(self.conf.vivo_install.xpath_allow_button, desc="点击权限允许按钮", timeout=5)
        #     except:
        #         break
        #
        # return True
        for i in range(2):
            try:
                self.device.click_by_xpath(self.conf.vivo_install.xpath_allow_button, desc="点击权限允许按钮", timeout=5)
            except:
                break
        return True

    def vivo_game_download_and_install(self, timeout=120, button_xpath=None, button_id=None):
        """
        Vivo手机游戏下载与安装
        Args：
            timeout: 超时
            click_last_installed: 是否需要点击前面遗留安装完成页面
            button_xpath: 点击安装的xpath
            button_id： 点击安装的id
        Returns:
            True: 进入成功
            False：进入失败
        """
        # 检测是否是第一次安装
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                self.device.find_element_by_id(self.conf.vivo_first_install.id_msg, timeout=5)
                if not self._vivo_first_install_game():
                    g_logger.warning("第一次安装app时，进行安装授权失败")
                    return False
                if button_id:
                    try:
                        self.device.click_by_id(button_id, desc="再次点击下载/安装按钮", timeout=5)
                        time.sleep(2)
                    except:
                        return False
                elif button_xpath:
                    try:
                        self.device.click_by_xpath(button_xpath, desc="再次点击下载/安装按钮", timeout=5)
                        time.sleep(2)
                    except:
                        return False
            except:
                try:
                    self.device.find_element_by_xpath(self.conf.vivo_install.xpath_input_password, timeout=3)
                    break
                except:
                    try:
                        self.device.find_element_by_xpath(self.conf.vivo_install.xpath_done, timeout=3)
                        self._vivo_click_last_installed(check_xpath=button_xpath, check_id=button_id)
                    except:
                        pass
        else:
            return False
        # 点击输入密码
        return self._vivo_install_input_password()

    def _vivo_install_input_password(self):
        """
        vivo 安装输入密码流程
        Returns:

        """
        try:
            self.device.find_element_by_xpath(self.conf.vivo_install.xpath_input_password, timeout=20).set_text(self.account_conf.common.passwd)
            time.sleep(1)
            self.device.click_by_xpath(self.conf.common_button.xpath_ok, desc="点击输入密码确认按钮", timeout=5)
            time.sleep(5)
            # 需要等待安装完成, 图像匹配方式防止卡死
            # self.device.click_by_xpath(self.conf.vivo_install.xpath_continue, desc='点击继续安装', timeout=120)
            if self._click_screen_from_pic(os.path.join(self.conf_img_dir, "1920_vivo_continue_install.png"), timeout=60):
                time.sleep(3)
            else:
                g_logger.error("图像匹配继续安装失败")
                raise TimeoutError("图像匹配超时")
            self.device.click_by_xpath(self.conf.vivo_install.xpath_install, desc='点击安装', timeout=20)
            time.sleep(5)
            return True
        except Exception as e:
            g_logger.error("点击输入密码失败")
            return False

    def _vivo_click_last_installed(self, check_xpath=None, check_id=None, timeout=120):
        """
        Vivo手机下载调起安装时点掉弹出的页面
        Args:
            check_xpath: 检测元素的xpath
            check_id: 检测元素的id
        Returns:
            True: 点掉成功，False: 点掉失败
        """
        if not check_id and not check_xpath:
            g_logger.warning("vivo点掉已安装完成页面未传入id和xpath，不进行点击回退")
            return False

        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                self.device.click_by_xpath(self.conf.vivo_install.xpath_done, timeout=3)
                time.sleep(1.5)
            except:
                try:
                    if check_xpath:
                        self.device.click_by_xpath(check_xpath, timeout=5)
                        time.sleep(3)
                        break
                    elif check_id:
                        self.device.click_by_id(check_id, timeout=5)
                        time.sleep(3)
                        break

                except:
                    break
        else:
            return False
        return True

    def _vivo_first_install_game(self):
        """
        vivo 第一次安装游戏时，授权处理流程
        Returns:
            True: 第一次安装app权限授予成功， False: 授予失败
        """
        try:
            self.device.click_by_xpath(self.conf.vivo_first_install.xpath_go_setting, desc='点击去设置按钮', timeout=5)
            time.sleep(2)
        except:
            return False

        try:
            self.device.click_by_xpath(self.conf.vivo_first_install.xpath_open_author, desc='点击打开权限开关', timeout=5)
            self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "打开权限开关.png"))
            time.sleep(2)
        except:
            return False

        self.key_event("KEYCODE_BACK")
        time.sleep(2)
        return True

    # def _vivo_grant_app_install_author(self, app_name, timeout=120):
    #     """
    #     Vivo手机给app授安装权限
    #     Args:
    #         app_name: app名称
    #     Returns:
    #         True: 授权成功, False: 授权失败
    #     """
    #     # 调起权限设置页面
    #     self.device.adb.start_app("com.vivo.permissionmanager", ".activity.PurviewTabActivity")
    #     time.sleep(2)
    #     time_start = time.time()
    #     while timeout > time.time() - time_start:
    #         try:
    #             self.device.click_by_xpath("//android.widget.Button[@text='权限']", desc="点击权限tab", timeout=5)
    #             time.sleep(2)
    #         except:
    #             try:
    #                 self.device.click_by_xpath(self.conf.vivo_setting.xpath_back_button, desc="点击回退按钮", timeout=5)
    #                 time.sleep(2)
    #             except:
    #                 self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "授权失败截图.png"))
    #                 return False
    #
    #     try:
    #         self.device.swipe_down_find_ele(xpath="//android.widget.TextView[@text='安装应用']", desc='点击安装应用标签', rate=0.5, timeout=30)
    #         time.sleep(2)

    def oppo_game_download_and_install(self, timeout=120, button_xpath=None, button_id=None):
        """
        oppo 游戏下载与安装
        Args：
            timeout: 超时
            click_last_installed: 是否需要点击前面遗留安装完成页面
            button_xpath: 点击安装的xpath
            button_id： 点击安装的id
        Returns:
        """
        try:
            self.device.find_element_by_id(self.conf.oppo_install.id_app_suggest_switch, timeout=5)
            g_logger.info("第一次安装游戏，点掉安全应用推荐")
            self.device.click_by_id(self.conf.oppo_install.id_app_suggest_switch, timeout=5)
            time.sleep(0.5)
            self.device.click_textview_text("以后都允许", timeout=5)
            time.sleep(2)
        except:
            pass
        return self._oppo_common_part_install()

    def oppo_install_apk(self, apk_name, uninstall_flag=True, str_flag=False, timeout=120):
        """
        oppo 命令行方式安装apk
        Args:
            apk_name: apk名称
            uninstall_flag:
            str_flag:
            timeout:
        Returns:
            True: 安装成功, False: 安装失败
        """
        apk_path = os.path.join(g_resource['project_path'], "app_pkg", apk_name)
        if uninstall_flag:
            self.device.adb.uninstall_app(package=self.get_app_package_from_apk(apk_name))

        _install_thread = IpeckerThread()
        _install_thread.start(self._cmd_async_install, apk_path, str_flag)
        time.sleep(2)
        # try:
        #     self.device.find_element_by_xpath(self.conf.vivo_install.xpath_continue, timeout=10)
        #     ret_flag = self._vivo_common_part_install()
        # except:
        #     ret_flag = self._vivo_install_input_password()

        if self._oppo_common_part_install():
            time_start = time.time()
            while timeout > time.time() - time_start:
                try:
                    self.device.click_by_xpath(self.conf.common_button.xpath_done, desc='点击完成按钮', timeout=5)
                    time.sleep(1)
                    break
                except:
                    time.sleep(1)
            else:
                _install_thread.stop()
                return False
        else:
            _install_thread.stop()
            return False
        for i in range(3):
            if self._async_install_flag:
                return True
            time.sleep(2)
        else:
            _install_thread.stop()
            return False

    def _oppo_common_part_install(self):
        """oppo 部分安装的相同流程
        Args:
            need_input_password: 是否需要输入密码
        """
        try:
            self.device.find_element_by_id(self.conf.oppo_install.id_input, timeout=20).set_text(self.account_conf.common.passwd)
            time.sleep(1)
            self.device.click_by_xpath(self.conf.common_button.xpath_install, desc='点击密码框安装按钮', timeout=10)
            time.sleep(3)
        except:
            g_logger.warning("密码输入框页面失败， 查看是否是安装页面")

        try:
            # 图像方式匹配安装按钮
            g_logger.info("图像方式点击安装页安装按钮")
            if self._click_screen_from_pic(os.path.join(self.conf_img_dir, "2280_oppo_sys_install_button.png"), timeout=60):
                g_logger.info("图像方式点击成功")
                time.sleep(3)
            else:
                g_logger.error("图像匹配安装失败")
                raise TimeoutError("图像匹配超时")
        except Exception as e:
            g_logger.warning("oppo 用于安装流程失败")
            return False
        return True

    def _oppo_phone_manager_gant(self, grant_name, app_name="爱奇艺", page_type='text'):
        """
        oppo 手机管家页面方式授权
        Args:
            grant_name: 权限名称
            app_name: 应用名称
            page_type: 授权页面流程类型：text:文本弹出方式选择， switch: 开关点击方式选择
            quit: 授权结束后是否退出手机管家
        Returns:
            True: 授权成功, False: 授权失败
        """
        self.device.adb.start_app("com.coloros.phonemanager", ".FakeActivity", stop_flag=True)
        time.sleep(3)
        if not (self.device.click_textview_text("权限隐私", timeout=10)
                and self.device.click_textview_text("应用权限", timeout=5)
                and self.device.click_textview_text(grant_name, swipe=True, timeout=120)):
            self.device.adb.stop_app("com.coloros.phonemanager")
            return False

        if page_type == 'text':
            if not (self.device.click_textview_text(app_name, swipe=True, timeout=60)
                    and self.device.click_textview_text("允许", timeout=5)):
                self.device.adb.stop_app("com.coloros.phonemanager")
                return False
        elif page_type == 'switch':
            switch_xpath = "//android.widget.TextView[@resource-id='android:id/title' and @text='{}']/../..//android.widget.Switch".format(app_name)
            try:
                self.device.click_by_xpath(switch_xpath, desc="点击{}授权开关".format(app_name), timeout=10)
                time.sleep(2)
            except:
                self.device.adb.stop_app("com.coloros.phonemanager")
                return False
        else:
            g_logger.warning("oppo手机管家授权弹出页面类型不是文本选择或者开关")
            self.device.adb.stop_app("com.coloros.phonemanager")
            return False

        self.device.adb.stop_app("com.coloros.phonemanager")
        return True

    def google_game_download_and_install(self, timeout=120, click_last_installed=True):
        """
        华为手机游戏下载与安装
        Args：
            timeout: 超时
            click_last_installed: 是否需要点击前面遗留安装完成页面
        Returns:
            True: 进入成功
            False：进入失败
        """
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                self.device.click_by_xpath(self.conf.common_button.xpath_install, timeout=5)
                time.sleep(5)
                return True
            except:
                if self.device.check_textview_text("出于安全考虑，已禁止您的手机安装来自此来源的未知应用。", timeout=5):  # 点击首次安装未知应用授权流程
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_setting, desc="点击设置按钮", timeout=5)
                        time.sleep(2)
                        self.device.click_by_xpath("//android.widget.TextView[@text='允许来自此来源的应用']/../..//android.widget.Switch",
                                                   desc='点击允许来自此来源的应用开关', timeout=10)
                        time.sleep(2)
                        self.cmd_back()
                        continue
                    except:
                        g_logger.info("安装页面出现授权安装未知应用，点击此流程失败")
        else:
            return False

    def xiaomi_install_apk(self, apk_name, uninstall_flag=True, str_flag=False, timeout=120):
        """
        小米命令行方式安装apk
        Args:
            apk_name: apk包名，在project/app_pkg目录下的apk
            uninstall_flag: 是否卸载apk
            str_flag: adb后部分命令是否用字符串包装出来
            timeout: 安装超时

        Returns:
            True: 安装成功, False: 安装失败
        """
        apk_path = os.path.join(g_resource['project_path'], "app_pkg", apk_name)
        if uninstall_flag:
            self.device.adb.uninstall_app(package=self.get_app_package_from_apk(apk_name))

        _install_thread = IpeckerThread()
        _install_thread.start(self._cmd_async_install, apk_path, str_flag)
        time.sleep(2)

        time_start = time.time()
        clicked_install_flag = False    # 已经点过安装按钮
        while timeout > time.time() - time_start:
            if not clicked_install_flag:
                try:
                    self.device.click_by_xpath(self.conf.common_button.xpath_continue_install, desc='点击继续安装按钮', timeout=5)
                    clicked_install_flag = True
                    time.sleep(1)
                except Exception as e:
                    continue
            else:
                if self._async_install_flag:
                    return True
                else:
                    time.sleep(1)
        else:
            g_logger.info("命令行安装apk:{}超时".format(apk_name))
            return False




















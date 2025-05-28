# -*- coding: UTF-8 -*-

"""
File Name:      android
Author:         zhangwei04
Create Date:    2018/5/21
"""
import os
import time
from .base_interface import BaseInterface
from framework.core.resource import g_resource
from framework.logger.logger import g_logger
from project.conf.elements_conf.configure import ElementConfig, AccountConfig

key_event_code_dict = {
    "KEYCODE_UNKNOWN": 0,
    "KEYCODE_MENU": 1,
    "KEYCODE_SOFT_RIGHT": 2,
    "KEYCODE_HOME": 3,
    "KEYCODE_BACK": 4,
}


class Android(BaseInterface):
    def __init__(self, target, ele_conf_name=None):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.installed_app_dict = dict()    # 自动化过程中，安装的app
        self.conf_img_dir = os.path.join(g_resource['project_path'], 'conf', 'img')
        self._window_size = None
        self.app_conf = ElementConfig("app")
        self.account_conf = AccountConfig()     # 账户配置文件

    def init(self):
        """初始化操作"""
        pass

    def _rm_ipecker_log(self):
        """移除ipecker日志
        """
        self.device.adb.rm_ipecker_log_file()
        return True

    def _get_sms_from_ipecker_log(self, msg_desc="验证码是"):
        """从ipecker apk 的log里获取短信验证码
            ps: 在点击发送验证码按钮前，需要调用start_ipecker_app()函数
        Return
            短信验证码列表
        """
        for i in range(30):
            ipecker_log = '/sdcard/ipecker_log.txt'
            if self.device.adb.check_file_exist(ipecker_log):
                out = "".join(self.device.adb.adb_shell("cat {}".format(ipecker_log)))
                import re

                data_list = re.findall(r'%s(\d{6})' % msg_desc, out)
                if data_list:
                    return data_list
            time.sleep(1)
        g_logger.warning("获取短信验证码失败")
        return []

    def clear_buff_data(self, path="", file_names=[], su_flag=False):
        """
        清除缓存数据
        Args:
            path: 缓存数据存放的路径
            file_names: 缓存数据的目录或者文件
            su_flag: 是否切换su模式
        """
        if not path:
            path = '/data/data/com.qiyi.video'
        if isinstance(file_names, str):
            file_names = [file_names]

        for file in file_names:
            if su_flag:
                cmd = "su & cd {} & rm -rf {}".format(path, file)
            else:
                cmd = "cd {} & rm -rf {}".format(path, file)
            self.device.adb.adb_shell(cmd)
        return True

    def reset_app(self, pkg=None, activity=None, clear_data=False):
        """
        重置app，若没有传入包名和activity，则重置默认的app
        Args:
            pkg: 包名
            activity：启动的activity
            clear_data:是否清除数据
        Returns:
            重置是否成功
        """
        if pkg and activity:
            if clear_data:
                cmd = "pm clear {}".format(pkg)
                self.device.adb.adb_shell(cmd)
            restart_cmd = "am start -S {}/{}".format(pkg, activity)
            self.device.adb.adb_shell(restart_cmd, str_flag=False)
            return True

        else:
            try:
                if clear_data:
                    self.device.reset()
                else:
                    self.device.close_app()
                    time.sleep(1)
                    self.device.launch_app()
                    time.sleep(1)
                return True
            except Exception as e:
                return False

    def key_event(self, key_code, sleep_time=2):
        """adb  shell 关键字时间
        Args:
            key_code: 按键事件码
            sleep_time: 点击后等待时间
        """
        if isinstance(key_code, str):
            if key_code in key_event_code_dict:
                key_code = key_event_code_dict.get(key_code)
        cmd = "input  keyevent {}".format(key_code)
        self.device.adb.adb_shell(cmd)
        time.sleep(sleep_time)
        return True

    def install_apk(self, apk_name=None, uninstall_flag=False, str_flag=False):
        """
        安装apk
        Args:
            apk_name: apk包名
            uninstall_flag: 是否要卸载
            str_flag: 命令已字符串方式传入执行
        """
        apk_path = os.path.join(g_resource['project_path'], "app_pkg", apk_name)
        if uninstall_flag:
            self.device.adb.uninstall_app(package=self.get_app_package_from_apk(apk_name))

        return self.device.adb.install_apk(apk_path, str_flag=str_flag)

    def sidebar_game_out(self):
        """侧边栏退出游戏
        """
        if self.device.find_element_by_id('sidebar', timeout=5):
            self.device.find_element_by_id('sidebar', timeout=5).click()
            self.device.find_element_by_id('quit', timeout=5).click()
            self.device.find_element_by_id('exit_game_sure', timeout=5).click()
            time.sleep(2)
        else:
            return False

    def get_app_package_from_apk(self, apk_name):
        """通过apk获取包名，apk目录project/app_pkg下
        Args:
            apk_name: 包名
        Returns:
            app名字
        """
        apk_path = os.path.join(g_resource['project_path'], "app_pkg", apk_name)
        return self.device.adb.get_app_name_from_apk(apk_path)

    def get_app_activity_from_apk(self, apk_name):
        """通过apk获取activity，apk目录project/app_pkg下
        Args:
            apk_name: apk包名
        Returns:
            启动进入的activity名字
        """
        apk_path = os.path.join(g_resource['project_path'], "app_pkg", apk_name)
        return self.device.adb.get_app_activity_from_apk(apk_path)

    def get_app_version_from_apk(self, apk_name):
        """通过apk获取activity，apk目录project/app_pkg下
        Args:
            apk_name: apk包名
        Returns:
            启动进入的activity名字
        """
        apk_path = os.path.join(g_resource['project_path'], "app_pkg", apk_name)
        outs, errs = self.device.adb.get_app_line_from_apk(apk_path, "versionName")
        import re
        parttern = re.compile(r".*versionName='(\d{1,3}\.\d{1,3}\.\d{1,3})")
        if not outs:
            g_logger.warning(errs)
            return None
        g = parttern.match("".join(outs))
        g_logger.info("version: {}".format(g.groups()[0] if g else ""))
        return g.groups()[0] if g else None

    def click_from_position(self, x_rate, y_rate, sleep_time=2):
        """通过坐标点击
        Args:
            x_rate: 若x_rate大于1，则表示绝对坐标点，否者为位置比例
            y_rate: 若y_rate大于1，则表示绝对坐标点，否者为位置比例
            sleep_time: 点击后睡眠时间
        """
        x_rate = float(x_rate)
        y_rate = float(y_rate)

        if x_rate > 1 and y_rate > 1:
            pass
        else:
            width, height = self.device.adb.get_window_size()
            x_rate = x_rate if x_rate > 1 else width * x_rate
            y_rate = y_rate if y_rate > 1 else height * y_rate

        self.device.adb.tap(x_rate, y_rate)
        time.sleep(sleep_time)

    def get_conf_and_click_position(self, session):
        width, height = self.device.adb.get_window_size()
        if isinstance(session, str):
            session = getattr(self.conf, session)

        self.click_from_position(getattr(session, "x_{}".format(width)), getattr(session, "y_{}".format(height)))

    def setting_proxy(self, host, port=8888):
        brand = self.device.get_manufacturer().lower()
        if brand == "huawei":
            return self._setting_proxy_huawei(host, port)

    def _setting_proxy_huawei(self, host, port, net_work=None):
        # ToDo 暂未完成此功能
        """华为手机设置代理"""
        # 返回桌面主页面
        for i in range(2):
            self.device.adb.adb_shell("input keyevent {}".format(key_event_code_dict.get("KEYCODE_HOME")))
            time.sleep(1)

        try:
            self.device.slide_find_element_by_id("设置", direct="left").click()
            time.sleep(2)
            self.device.click_by_xpath("//com.android.settings[@text='WLAN']").click()
            if net_work is None:
                self.device.slide_find_element_by_id("//android.widget.TextView[@text='已连接']", direct="up")
        except:
            pass

    def match_any_image_to_screen(self, des_pic_path, timeout=10):
        """
        截图比较目标图片
        Args:
            des_pic_path: 目标图片路径（列表,有一个满足即可）
            timeout: 匹配超时
        Returns:
            True: 匹配成功, False: 匹配失败
        """
        if isinstance(des_pic_path, str):
            des_pic_path = [des_pic_path]
        screen_path = os.path.join(self.conf_img_dir, "screen.png")
        time_start = time.time()
        while timeout > time.time() - time_start:
            self.device.adb.screen_shot(screen_path)
            for pic in des_pic_path:
                result = self.match_image(screen_path, pic, confidence=0.8)
                if result:
                    return result
            time.sleep(1)

        return False

    @staticmethod
    def cron_img(src_img_path, save_path, start_x, start_y, end_x, end_y):
        """
        克隆图片区域
        Args:
            src_img_path: 原图片路径
            save_path: 保存路径
            start_x: 区域开始(左上角)横坐标
            start_y: 区域开始(左上角)纵坐标
            end_x: 区域结束(右下角)横坐标
            end_y: 区域结束(右下角)纵坐标
        Returns:

        """
        if not os.path.exists(src_img_path):
            g_logger.error("文件{}不存在，请检测文件是否存在".format(src_img_path))
            return False
        try:
            from PIL import Image
        except:
            g_logger.error("PIL 库没有安装，请使用命令：pip install pillow进行安装")
            return False

        try:
            img = Image.open(src_img_path)
            img.crop((start_x, start_y, end_x, end_y)).save(save_path)
            return True
        except Exception as e:
            g_logger.error(str(e))
            return None

    def check_app_installed(self, package):
        """
        检测app是否安装
        Args:
            package: app名称
        Returns:
            True: 已经安装， False: 没有安装
        """
        return self.device.adb.check_app_is_install(package)

    def check_game_installed(self, game_name):
        """
        检测游戏是否安装，游戏信息需要配置在prject/conf/elements_conf/game.conf文件中
        Args:
            game_name: 游戏名，对应game.conf里面的section
        Returns:
            True: 游戏已经安装, False: 游戏未安装
        """
        return self.check_app_installed(self.app_conf.get(game_name, "package"))

    def check_desktop_app(self, app_name, timeout=30):
        """
        检测桌面app名
        Args:
            app_name: app桌面图标显示的名称
        Returns:
            True: 检测成功, False: 检测失败
        """
        for i in range(2):
            self.device.adb.adb_shell("input keyevent {}".format(key_event_code_dict.get("KEYCODE_HOME")))
            time.sleep(2)

        time_start = time.time()
        while timeout > time.time() - time_start:
            if self.device.check_textview_text(app_name, timeout=3):
                return True

            self.device.swipe_screen(rate=0.6, direction='left')
        else:
            g_logger.error("桌面查找app:{}失败".format(app_name))
            return False

    def into_desktop_app(self, app_name, need_back_home=False, timeout=60):
        """
        从桌面进入app
        Args:
            app_name: app名称
            need_back_home: 需要回退到桌面home页
            timeout: 查找超时
        Returns:
            True: 进入成功, False: 进入失败
        """
        if need_back_home:
            for i in range(2):
                self.device.adb.adb_shell("input keyevent {}".format(key_event_code_dict.get("KEYCODE_HOME")))
                time.sleep(2)

        time_start = time.time()
        while timeout > time.time() - time_start:
            if self.device.click_textview_text(app_name, timeout=5):
                g_logger.info('点击桌面图标：{} 成功'.format(app_name))
                return True
            self.device.swipe_screen(rate=0.6, direction='left')
        else:
            g_logger.error("桌面查找app:{}失败".format(app_name))
            return False

    def _click_screen_from_pic(self, pic_path, timeout=10):
        screen_path = os.path.join(self.conf_img_dir, "screen.png")
        time_start = time.time()
        while timeout > time.time() - time_start:
            # self.device.get_screenshot_as_file(screen_path)   # 此接口可能会卡主
            self.device.adb.screen_shot(screen_path)
            time.sleep(1)
            result = self.match_image(screen_path, pic_path, confidence=0.9)
            if result:
                # self.device.tap([(result.get("result"))]) # 此接口可能会卡主
                self.device.adb.tap(result.get("result")[0], result.get("result")[1])
                time.sleep(1)
                return True
        return False

    def cmd_back(self, sleep_time=2):
        """命令行方式回退
        Args:
            sleep_time: 等待时间
        """
        self.key_event("KEYCODE_BACK", sleep_time=sleep_time)
        return True


# -*- coding: UTF-8 -*-

"""
File Name:      polymerized
Author:         zhangwei04
Create Date:    2018/7/6
"""

import time
from framework.logger.logger import g_logger
from project.lib.android import Android
from framework.utils.threads import IpeckerThread


class Polymerized(Android):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='polymerized_sdk')
        self.target = target
        self.data = target.data
        self.device = target.device
        self._data = None
        self._package_name = ""
        self._activity_main = ""
        self.__thread_stop_flag = False
        self.__thread = None

    def set_data(self, data):
        self._data = data

    def install_and_start_channel_apk(self):
        """安装通道apk，若已安装，则需要卸载重装"""
        self._package_name = self.get_app_package_from_apk(self._data.apk_name)
        self._activity_main = self.get_app_activity_from_apk(self._data.apk_name)

        self.uninstall_channel_apk()

        self.install_apk(self._data.apk_name, uninstall_flag=True, str_flag=False)
        self.device.start_activity(self._package_name, self._activity_main)

        # 等待30秒动画播放
        g_logger.info("等待3分钟，播放动画")
        time.sleep(60 * 3)
        self.device.adb.stop_app(self._package_name)
        self.device.start_activity(self._package_name, self._activity_main)

    @property
    def channel(self):
        """渠道"""
        # TODO 后续添加环境变量获取
        return self._data.channel.lower() if self._data else ""

    # 登录
    def login(self):
        # 游戏登录待添加
        # self.__asyn_game_to_sdk_login()
        login_obj = self.__getattribute__("_{}_login".format(self.channel))
        return login_obj(getattr(self._data, "{}_user".format(self.channel)), getattr(self._data, "{}_passwd".format(self.channel)))

    # 退出登录
    def login_out(self):
        login_out_obj = self.__getattribute__("_{}_login_out".format(self.channel))
        return login_out_obj(getattr(self._data, "{}_user".format(self.channel)), getattr(self._data, "{}_passwd".format(self.channel)))

    # 切换账号
    def switch_account(self):
        switch_account_obj = self.__getattribute__("_{}_switch_account".format(self.channel))
        return switch_account_obj(getattr(self._data, "{}_user".format(self.channel)), getattr(self._data, "{}_passwd".format(self.channel)))

    """
        coolpad 渠道
    """
    def _coolpad_login(self, username, passwd):
        try:
            self.device.find_element_by_xpath(self.conf.coolpad_login_user.xpath).set_text(username)
            self.device.find_element_by_xpath(self.conf.coolpad_login_passwd.xpath).set_text(passwd)
            self.device.find_element_by_xpath(self.conf.coolpad_login_button.xpath).click()
            time.sleep(3)
            return self._coolpad_check_is_login()
        except:
            g_logger.error("coolpad login failed")
            return False

    def _coolpad_login_out(self, username, passwd):
        pass

    def _coolpad_switch_account(self, username, passwd):
        try:
            # 确认是否侧边栏已经打开
            self.device.find_element_by_id(self.conf.huawei_base_user_icon.id, timeout=5)
        except:
            # 侧边栏没有打开需要打开
            self._coolpad_open_side()
            try:
                self.device.find_element_by_id(self.conf.huawei_base_user_icon.id, timeout=5)
            except:
                g_logger.error('coolpad 侧边栏没有打开')
                return False
        try:
            # 点击切换账号
            self.device.find_element_by_xpath(self.conf.coolpad_user_switch_account.xpath).click()
            # 登录
            self._coolpad_login(username, passwd)
            return True
        except:
            g_logger.error('coolpad 登录失败')
            return False

    def _coolpad_check_is_login(self):
        self._coolpad_open_side()
        try:
            self.device.find_element_by_id(self.conf.huawei_base_user_icon.id)
        except:
            return False
        # 点掉侧边栏
        self.click_from_position(0.9, 0.9)
        return True

    def _coolpad_open_side(self):
        self.click_from_position(x_rate=0.02083, y_rate=0.5648, sleep_time=0.5)
        self.click_from_position(x_rate=0.02083, y_rate=0.5648, sleep_time=1)
        self.click_from_position(x_rate=0.04687, y_rate=0.5833)
        time.sleep(1)

    """
        华为渠道
    """
    def _huawei_login(self, username, passwd):
        try:
            user_status_ele = self.device.find_element_by_id(self.conf.huawei_user_status.id)
            if user_status_ele.get_attribute("text") == "登录华为账号":
                user_status_ele.click()
        except:
            pass

        try:
            self.device.find_element_by_id(self.conf.huawei_login_user.id).set_text(username)
            self.device.find_element_by_id(self.conf.huawei_login_passwd.id).set_text(passwd)
            self.device.find_element_by_id(self.conf.huawei_login_button.id).click()
        except:
            return False

        return self._huawei_check_is_login()

    def _huawei_login_out(self, username, passwd):
        try:
            # 若用户首页已经打开，则直接进入
            self.device.find_element_by_id(self.conf.huawei_base_user_icon.id).click()
        except:
            self._huawei_open_side()
            self.device.find_element_by_id(self.conf.huawei_base_user_icon.id).click()

        try:
            self.device.find_element_by_id(self.conf.huawei_my_tab.id).click()
            self.device.find_element_by_xpath(self.conf.huawei_my_user_icon.xpath).click()
            time.sleep(3)

            size = self.device.get_window_size()
            width = size.get('width')
            height = size.get('height')
            self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
            self.device.find_element_by_xpath(self.conf.huawei_logout_user.xpath).click()
            self.device.find_element_by_id(self.conf.huawei_logout_passwd.id).set_text(passwd)
            self.device.find_element_by_xpath(self.conf.huawei_logout_ensure.xpath).click()
            return self.device.find_element_by_id(self.conf.huawei_user_status.id).get_attribute('text') == "登录华为帐号"
        except:
            return False

    def _huawei_switch_account(self, username, passwd):
        return self._huawei_login_out(passwd) and self._huawei_login(username, passwd)

    def _huawei_check_is_login(self):
        self._huawei_open_side()
        try:
            self.device.find_element_by_id(self.conf.huawei_base_user_icon.id)
        except:
            return False

        return True

    def _huawei_open_side(self):
        self.click_from_position(x_rate=0.014, y_rate=0.5)


    """
        爱奇艺渠道
    """
    def _iqiyi_login(self, username, passwd, timeout=1800):
        # 清除缓存
        self.device.adb.adb_shell(" rm -rf /sdcard/iqiyigame/.data/*")
        self.device.adb.adb_shell("rm -rf /sdcard/Android/data/com.iqiyigame.sdk/.data/*")

        # self.__asyn_game_to_sdk_login()
        # 打开侧边栏
        self._iqiyi_open_side()
        # 通过获取短信验证码按钮，检测是否登录
        try:
            time_start = time.time()
            while True:
                try:
                    self.device.find_element_by_id(self.conf.iqiyi_login_get_msg_code.id, timeout=10)
                    self.__thread_stop_flag = True
                    break
                except:
                    if time.time() - time_start > timeout:
                        g_logger.warning("查找侧边栏超时")
                        return False
            # 切换至账号密码方式登录
            self.device.find_element_by_id(self.conf.iqiyi_other_style_login.id, timeout=10).click()
            self.device.find_element_by_id(self.conf.iqiyi_login_user.id, timeout=10).set_text(username)
            self.device.find_element_by_id(self.conf.iqiyi_login_passwd.id, timeout=10).set_text(passwd)
            self.device.find_element_by_id(self.conf.iqiyi_login_button.id, timeout=3).click()
            time.sleep(2)
            return True
        except:
            # 查找用户是否登录
            self.device.find_element_by_id(self.conf.iqiyi_user_icon.id)
            g_logger.warning("SDK已经登录")
            # 关闭侧边栏按钮
            self.device.find_element_by_id(self.conf.iqiyi_side_close.id).click()
            return True

    def _iqiyi_login_out(self, username, passwd):
        self._iqiyi_open_side()
        try:
            # 判断是否登录
            try:
                self.device.find_element_by_id(self.conf.iqiyi_login_get_msg_code.id, timeout=10)
                return True
            except:
                pass
            # 进入个人中心
            self.device.find_element_by_id(self.conf.iqiyi_user_icon.id, timeout=10).click()
            self.device.find_element_by_id(self.conf.iqiyi_logout.id, timeout=5).click()
            return True
        except:
            return False

    def _iqiyi_switch_account(self, username, passwd):
        ret = self._iqiyi_login_out(username, passwd) and self._iqiyi_login(username, passwd, timeout=30)
        ret = ret and self._iqiyi_check_is_login()
        return ret

    def _iqiyi_check_is_login(self):
        self._iqiyi_open_side()
        try:
            self.device.find_element_by_id(self.conf.iqiyi_user_icon.id, timeout=10)
            # 点掉侧边栏
            self.device.find_element_by_id(self.conf.iqiyi_side_close.id, timeout=10).click()
            return True
        except:
            g_logger.warning("iqiyi侧边栏打开失败")
            return False

    def _iqiyi_open_side(self):
        self.click_from_position(x_rate=0.0052, y_rate=0.5)

    """
        联想渠道
    """
    def _lenovo_login(self, username, passwd):
        self._lenovo_open_side()
        try:
            self.device.find_element_by_id(self.conf.levono_login_user.id).set_text(username)
            self.device.find_element_by_id(self.conf.levono_login_passwd).set_text(passwd)
            self.device.find_element_by_id(self.conf.levono_login_button).click()
            # 确认是否登录，或者切换账号
            pass
            return True
        except:
            return False

    def _lenovo_open_side(self):
        self.click_from_position(x_rate=0.026, y_rate=0.0463)

    def _lenovo_login_out(self, username, passwd):
        pass

    def _lenovo_switch_account(self, username, passwd):
        pass

    """
        魅族渠道
    """
    def _meizu_login(self, username, passwd):
        try:
            self.device.find_element_by_id(self.conf.meizu_login_user).set_text(username)
            self.device.find_element_by_id(self.conf.meizu_login_passwd).set_text(passwd)
            self.device.find_element_by_id(self.conf.meizu_login_button).click()
        except:
            g_logger.error("未找到登录信息")
            return False

        return True

    def _meizu_login_out(self, username, passwd):
        pass

    def _meizu_switch_account(self, username, passwd):
        pass

    def _meizu_check_is_login(self):
        self._meizu_open_side()
        try:
            self.device.find_element_by_id(self.conf.meizu_base_charge.id)
        except:
            return False

        return True

    def _meizu_open_side(self):
        self.click_from_position(x_rate=0.988, y_rate=0.1481, sleep_time=0.5)
        self.click_from_position(x_rate=0.9323, y_rate=0.1481)

    """
        oppo渠道
    """
    def _oppo_login(self, username, passwd):
        try:
            self.device.find_element_by_id(self.conf.oppo_login_user.id).set_text(username)
            self.device.find_element_by_id(self.conf.oppo_login_passwd.id).set_text(passwd)
            self.device.find_element_by_id(self.conf.oppo_login_button.id).click()
            time.sleep(5)
            return self._oppo_check_is_login()
        except:
            g_logger.error("oppo 登录失败")
            return False

    def _oppo_login_out(self, username, passwd):
        pass

    def _oppo_switch_account(self, username, passwd):
        pass

    def _oppo_check_is_login(self):
        self._oppo_open_side()
        try:
            game_id_ele = self.device.find_element_by_id(self.conf.oppo_user_game_id.id)
            return True
            # return "游戏ID" in game_id_ele.get_attribute('text')
        except:
            g_logger.error("oppo 检测账户登录失败")
            return False

    def _oppo_open_side(self):
        self.click_from_position(x_rate=0.01823, y_rate=0.176, sleep_time=0.3)
        self.click_from_position(x_rate=0.03646, y_rate=0.1944)


    """
        奇虎360渠道
    """
    def _qihoo_login(self, username, passwd, timeout=1800):
        # 从侧边栏登录
        # self._qihoo_open_side()
        try:
            # self.device.find_element_by_id(self.conf.qihoo_login_register.id).click()
            time_start = time.time()
            while True:
                try:
                    self.device.find_element_by_id(self.conf.qihoo_login_user.id, timeout=10)
                    self.__thread_stop_flag = True
                    break
                except:
                    if time.time() - time_start > timeout:
                        return False
            try:
                self.device.find_element_by_id(self.conf.qihoo_login_account_passwd.id, timeout=5).click()
                time.sleep(2)
            except:
                pass
            self.device.find_element_by_id(self.conf.qihoo_login_user.id).set_text(username)
            self.device.find_element_by_id(self.conf.qihoo_login_passwd.id).set_text(passwd)
            self.device.find_element_by_id(self.conf.qihoo_login_user_experience.id).click()
            time.sleep(2)
            self.device.find_element_by_id(self.conf.qihoo_login_button.id).click()
            time.sleep(2)
            # 点击后可能跳出未接受用户协议，需要重新点一次
            try:
                self.device.find_element_by_id(self.conf.qihoo_plain_ensure_button.id, timeout=5).click()
                time.sleep(2)
                self.device.find_element_by_id(self.conf.qihoo_login_button.id).click()
            except:
                pass
            time.sleep(5)
            ret = self._qihoo_check_is_login()
            # 点掉侧边栏
            self.click_from_position(0.9, 0.9)
        except:
            g_logger.error("360渠道登录失败")
            return False

        return ret

    def _qihoo_login_out(self, username, passwd):
        return True

    def _qihoo_switch_account(self, username, passwd):
        self._qihoo_open_side()
        try:
            # 通过左边点击切换账号
            time.sleep(2)
            self.get_conf_and_click_position(self.conf.qihoo_exchange_user)
            time.sleep(3)
            return self._qihoo_login(username, passwd, timeout=30)

        except:
            g_logger.error("360渠道 切换账号失败")
            return False

    def _qihoo_check_is_login(self):
        self._qihoo_open_side()
        try:
            e = self.device.find_element_by_id(self.conf.qihoo_user_name.id, timeout=10)
            if e.get_attribute("text") == "":
                g_logger.error("oppo 检测账户登录失败")
                return False
            else:
                g_logger.error("oppo 检测账户登录成功")
                return True
        except:
            g_logger.error("未找个人首页用户名文本框")
            return True

    def _qihoo_open_side(self):
        self.click_from_position(x_rate=0.01302, y_rate=0.3102)

    """
        uc渠道
    """
    def _uc_login(self, username, passwd, timeout=1800):
        try:
            while True:
                start_time = time.time()
                time.sleep(3)
                try:
                    login_title_ele = self.device.find_element_by_id(self.conf.uc_login_title.id, timeout=10)
                    self.__thread_stop_flag = True
                    break
                except:
                    if time.time() - start_time > timeout:
                        return False
            text = login_title_ele.get_attribute('text')
            g_logger.info(text)
            if "UC号登录" not in text:
                try:
                    # 若出现切换登录方式图标需要点击，才能显示UC账号图标
                    self.device.find_element_by_xpath(self.conf.uc_login_switch_style.xpath, timeout=5).click()
                    time.sleep(3)
                    self.device.find_element_by_xpath(self.conf.uc_login_style_icon.xpath1, timeout=10).click()
                except:
                    self.device.find_element_by_xpath(self.conf.uc_login_style_icon.xpath, timeout=10).click()
                time.sleep(3)
            # UC 账号登录
            self.device.find_element_by_id(self.conf.uc_login_user.id, timeout=10).set_text(username)
            self.device.find_element_by_id(self.conf.uc_login_passwd.id, timeout=10).set_text(passwd)
            self.device.find_element_by_id(self.conf.uc_login_button.id, timeout=10).click()
            time.sleep(3)
            return self._uc_check_is_login()
        except:
            g_logger.error('UC渠道登录失败')
            return False

    def _uc_login_out(self, username, passwd):
        g_logger.warning("uc渠道暂无退出按钮")
        return True

    def _uc_switch_account(self, username, passwd):
        g_logger.warning("uc渠道暂无切换账号按钮")
        return True

    def _uc_check_is_login(self):
        self._uc_open_side()
        try:
            self.device.find_element_by_xpath(self.conf.uc_my_text.xpath, timeout=10)
            return True
        except:
            return False

    def _uc_open_side(self):
        # self.click_from_position(x_rate=0.010416, y_rate=0.0787)
        self.get_conf_and_click_position(self.conf.uc_side_icon)

    """
        vivo渠道
    """
    def _vivo_login(self, username, passwd):
        try:
            self.device.find_element_by_id(self.conf.vivo_login_user.id, timeout=20).set_text(username)
            self.device.find_element_by_id(self.conf.vivo_login_passwd.id, timeout=10).set_text(passwd)
            self.device.find_element_by_id(self.conf.vivo_login_button.id, timeout=10).click()
            time.sleep(5)
        except:
            return False

        return True

    def _vivo_login_out(self, username, passwd):
        pass

    def _vivo_switch_account(self, username, passwd):
        pass

    def _vivo_check_is_login(self):
        self._vivo_open_side()
        time.sleep(2)
        self.click_from_position(x_rate=0.1354, y_rate=0.389)
        try:
            persion_title_ele = self.device.find_element_by_id(self.conf.vivo_persion_center_title.id, timeout=10)
            if persion_title_ele.get_attribute('text') == "个人中心":
                return True
        except:
            g_logger.error("vivo 没有找到个人中心页")
            pass
        return False

    def _vivo_open_side(self):
        self.click_from_position(x_rate=0.026, y_rate=0.0463)

    """
        小米渠道
    """
    def _xiaomi_login(self, username, passwd):
        pass

    def _xiaomi_login_out(self, username, passwd):
        pass

    def _xiaomi_switch_account(self, username, passwd):
        pass

    def __asyn_game_to_sdk_login(self):

        self.__thread = IpeckerThread()
        x_set = (0.5, 0.9, 0.7, 0.95)
        y_set = (0.8, 0.7, 0.9, 0.6, 0.03)
        self.__thread.start(self.__ansy_random_click, x_set=x_set, y_set=y_set)

    def __asyn_random_click(self, x_set, y_set):
        self.key_event("KEYCODE_BACK")
        time.sleep(10)
        # 一些提示需要点掉
        while True:
            for x_axis in x_set:
                for y_axis in y_set:
                    time.sleep(5)
                    if not self.__thread_stop_flag:
                        g_logger.info("click postion : {} {}".format(x_axis, y_axis))
                        time_start = time.time()
                        self.click_from_position(x_axis, y_axis, sleep_time=0.5)
                        g_logger.info("run: {}".format(time.time() - time_start))
            if self.__thread_stop_flag:
                break

    def uninstall_channel_apk(self):
        if not self._package_name:
            self._package_name = self.get_app_package_from_apk(self._data.apk_name)

        self.device.adb.adb("uninstall {}".format(self._package_name), str_flag=False)




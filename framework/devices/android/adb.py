# -*- coding: UTF-8 -*-

"""
File Name:      adb
Author:         zhangwei04
Create Date:    2018/1/16
"""
import os
import time
from framework.logger.logger import g_logger, g_framework_logger
from framework.core.resource import g_resource, const
from framework.utils.threads import IpeckerPopen
from framework.exception.exception import DeviceNotFound, DeviceUnauthorized

PERMISSIONS = {"write": "android.permission.WRITE_EXTERNAL_STORAGE", "read": "android.permission.READ_EXTERNAL_STORAGE",
               "fine_location": "android.permission.ACCESS_FINE_LOCATION", "coarse_loaction": "android.permission.ACCESS_COARSE_LOCATION",
               "read_phone": "android.permission.READ_PHONE_STATE", "shortcut": "com.android.launcher.permission.INSTALL_SHORTCUT",
               "shortcut2": "com.android.launcher3.permission.INSTALL_SHORTCUT"}
            # "shortcut1": "com.android.launcher2.permission.INSTALL_SHORTCUT",


class Adb(object):
    """adb 通讯方式类
    """
    def __init__(self, sn=None):
        """
        Args:
            sn: 设备sn号
        """
        self.__sn = sn

    def adb(self, cmd, timeout=None, shell=None, console=False, log=True, log_type="case", str_flag=True):
        """adb命令接口
        Args:
            cmd: adb命令
            timeout: 命令超时
            shell: 是否使用shell方式
            console: 是否打印到控制台
            log: 是否写入日志文件中
            log_type: 打印的日志类型
            str_flag: 是否使用字符串包装起命令
        Returns:
            命令执行后返回信息
        """
        if not shell:
            shell = True if g_resource['system'] == const.SYSTEM_LINUX else False
        if str_flag:
            adb_cmd = 'adb -s {} "{}"'.format(self.__sn, cmd) if self.__sn else 'adb {}'.format(cmd)
        else:
            adb_cmd = 'adb -s {} {}'.format(self.__sn, cmd) if self.__sn else 'adb {}'.format(cmd)

        if log_type == 'framework':
            logger = g_framework_logger
        else:
            logger = g_logger
        logger.info(adb_cmd, console=console)

        p = IpeckerPopen(adb_cmd, timeout=timeout, shell=shell)
        outs, errs = p.execute()
        if log:
            if outs:
                logger.info(outs.replace('\r\n', '\n'), console=console)
            if errs:
                logger.warning(errs.replace('\r\n', '\n'), console=console)
        return self.__split_lines(outs)

    def adb_shell(self, cmd, timeout=None, shell=False, log=True, console=False, log_type="case", str_flag=True):
        """adb shell命令接口
        Args:
            cmd: adb shell 命令
            timeout: 命令超时
            log: 是否打印日志
            log_type: 打印的日志类型
            console:是否打印到控制台
            shell: 是否使用shell方式
            str_flag: 是否使用字符串包装起命令
        Returns:
            命令执行后返回信息列表
        """
        if not shell:
            shell = True if g_resource['system'] == const.SYSTEM_LINUX else False

        if str_flag:
            adb_shell_cmd = 'adb -s {} shell "{}"'.format(self.__sn, cmd) if self.__sn else 'adb shell "{}"'.format(cmd)
        else:
            adb_shell_cmd = 'adb -s {} shell {}'.format(self.__sn, cmd) if self.__sn else 'adb shell {}'.format(cmd)

        if log_type == 'framework':
            logger = g_framework_logger
        else:
            logger = g_logger
        logger.info(adb_shell_cmd, console=console)

        p = IpeckerPopen(adb_shell_cmd, timeout=timeout, shell=shell)
        outs, errs = p.execute()
        if log:
            if outs:
                logger.info(outs.replace('\r\n', '\n'), console=console)
            if errs:
                logger.warning(errs.replace('\r\n', '\n'), console=console)
        return self.__split_lines(outs)

    def get_device_list(self):
        """
        获取设备sn号
        Returns:
            设备sn号列表
        """
        ret_msg = self.adb('devices')
        return ret_msg

    def check_device(self):
        """
        检查设备状态是否正常
        Returns:
            True：设备状态正常， False：设备状态异常
        """
        device_list = self.get_device_list()
        if self.__sn is None:
            return True
        for line in device_list:
            if self.__sn in line:
                if line.endswith('unauthorized'):
                    raise DeviceUnauthorized(self.__sn)
                elif line.endswith('device'):
                    return True
                else:
                    continue
        return False

    def get_release_version(self):
        """
        获取设备aandroid发行版本号
        Returns:
            设备版本号
        """
        ret_msg = []
        try:
            ret_msg = self.adb_shell('getprop ro.build.version.release')
        except Exception as e:
            g_logger.warning(str(e))
        if ret_msg:
            return ret_msg[0]
        return None

    def get_sdk_version(self):
        """
        获取设备android sdk版本号
        Returns:
            设备sdk版本号
        """
        return self.adb_shell('getprop ro.build.version.sdk')[0].strip()

    def kill_process(self, pid):
        """
        根据进程id杀进程
        Args:
            pid: 进程ID
        Returns:
            命令执行后返回信息
        """
        if isinstance(pid, (str, set)):
            cmd = "kill {}".format(" ".join(pid))
        elif not isinstance(pid, int):
            cmd = "kill {}".format(self.pid)
        else:
            pass
        return self.adb_shell(cmd)

    def get_pid(self, pname, log_type="case"):
        """
        根据进程名获取设配进程id
        Args:
            pname: 进程名
        Returns:
            进程集合
        """
        if pname:
            cmd = "ps | grep '{}'".format(pname)
        outs = self.adb_shell(cmd, log_type=log_type)
        pid_set = set()
        for line in outs:
            if line and "grep {}".format(pname) not in line:
                split_msg = line.split()
                if len(split_msg) > 2 and split_msg[1].isdigit():
                    pid_set.add(split_msg[1])
        return pid_set

    def get_app_uid(self, pname, log_type="case"):
        """获取app的uid"""
        pid_set = self.get_pid(pname, log_type=log_type)
        if pid_set:
            ret_msg = self.adb_shell("cat /proc/{}/status | grep Uid".format(pid_set.pop()), log_type=log_type)
            # return "Uid:    12801   12801   12801   12801"
            if ret_msg:
                return ret_msg[0].split()[1]
        return ""

    def reboot(self):
        """
        重启设备
        """
        self.adb('reboot')
        self.adb('wait-for-device')

    def clear_app_data(self, package='com.qiyi.video'):
        """
        清除app数据
        Args:
            package: 安装后的包名
        Returns:
            True:清除成功， False：清除失败
        """
        cmd = "pm clear {}".format(package)
        return self.adb_shell(cmd) == 'Success'

    def check_file_exist(self, file, path=""):
        """
        检测文件是否存在
        Args:
            file: 文件名
            path: 文件路径
        Returns:
            按行拆分的列表
        """
        # 路径为空，则取出文件参数里面的路径
        file_path, file_name = os.path.split(file)

        path = file_path if file_path.startswith('/') else "{}/{}".format(path, file_path)

        for line in self.adb_shell('cd {} && ls -l | grep {}'.format(path, file_name)):
            if file_name in line:
                return True
        return False

    def install_apk(self, apk_package, str_flag=True):
        """
        安装apk
        Args:
             apk_package: apk包路径
             str_flag: 字符串封装参数
        Returns:
             安装命令返回信息
        """
        apk_abs_path = os.path.abspath(apk_package)
        self.adb("install -g {}".format(apk_abs_path), console=False, str_flag=str_flag)
        return True

    def uninstall_app(self, package=None, apk_package_path=None):
        if package:
            self.adb("uninstall {}".format(package), str_flag=False)
        if apk_package_path:
            app_name = self.get_app_name_from_apk(apk_package_path)
            if self.check_app_is_install(app_name):
                self.adb("uninstall {}".format(app_name), str_flag=False)
        return True

    def get_app_name_from_apk(self, apk_package_path):
        return self.get_app_info_from_apk(apk_package_path)

    def get_app_activity_from_apk(self, apk_package_path):
        return self.get_app_info_from_apk(apk_package_path, filter_key='activity')

    def get_app_info_from_apk(self, apk_package_path, filter_key='package', start_flag="'", end_flag="'"):
        outs, errs = self.get_app_line_from_apk(apk_package_path, filter_key)
        if outs:
            start_index = outs.find(start_flag) + len(start_flag)
            end_index = outs.find(end_flag, start_index)
            return outs[start_index:end_index]
        return ""

    def get_app_line_from_apk(self, apk_package_path, filter_key=None):
        apk_package_path = os.path.abspath(apk_package_path)
        if g_resource['system'] == const.SYSTEM_WINDOWS:
            shell = True
            aapt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tools", "aapt_windows.exe"))
            if filter_key:
                cmd = "{} dump  badging {} | findstr {}".format(aapt_path, apk_package_path, filter_key)
            else:
                cmd = "{} dump  badging {}".format(aapt_path, apk_package_path)
        else:
            shell = True
            aapt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tools", "aapt"))
            if filter_key:
                cmd = "{} dump  badging {} | grep {}".format(aapt_path, apk_package_path, filter_key)
            else:
                cmd = "{} dump  badging {}".format(aapt_path, apk_package_path)
        outs, errs = IpeckerPopen(cmd, timeout=5, shell=shell).execute()
        return outs, errs

    def check_app_is_install(self, package):
        """
        检测app是否安装
        Args:
            package: app包名
        Returns:
            True:已经安装，False：未安装
        """
        cmd = "pm list package | grep {}".format(package)
        for line in self.adb_shell(cmd):
            if package in line:
                return True
        return False

    def start_app(self, package, activity, stop_flag=False):
        """
        启动app
        Args:
             package: 包名
             activitiy：活动名
             stop_flag: 若app已启动，是否强制停止后再启动
        Return:
            发送命令的返回信息
        """
        if stop_flag:
            cmd = "am start -W -S -n {}/{}"
        else:
            cmd = "am start -W -n {}/{}"
        return self.adb_shell(cmd.format(package, activity))

    def stop_app(self, package):
        """
        强制停止app
        Args:
            package: 包名
        Returns:
            命令执行后信息
        """
        return self.adb_shell("am force-stop {}".format(package))

    def __split_lines(self, outs):
        """
        拆分行函数，将adb命令的返回结果拆分成行
        Args:
            outs: 命令返回结果
        Returns:
            按行拆分的列表
        """
        ret_list = []
        if not outs:
            return ret_list

        out_list = outs.splitlines()
        for line in out_list:
            line_striped = line.strip()
            if line_striped:
                ret_list.append(line_striped)
        return ret_list

    # ipecker apk 相关
    def rm_ipecker_log_file(self):
        """
        移除手机中ipecker app 日志文件
        """
        self.adb_shell('rm -rf /sdcard/ipecker_log.txt')

    def check_ipecker_log_exist(self):
        """
        检测 ipecker app 短信日志文件是否捕获到
        """
        return self.check_file_exist('ipecker_log.txt', '/sdcard/')

    def install_ipecker_apk(self):
        """安装ipecker apk
        Returns:
            安装命令返回信息
        """
        return self.install_apk(os.path.join(os.path.dirname(__file__), 'ipecker.apk'), str_flag=False)

    def tap(self, x: float, y: float):
        """根据元素点按压
        Args:
            x: 横坐标
            y: 纵坐标
        """
        self.adb_shell("input tap {} {}".format(x, y))

    def get_window_size(self):
        """获取当前窗口分辨率"""
        ret = self.adb_shell("dumpsys window displays | grep init=", str_flag=True)
        ret_line_split = "".join(ret).split()
        for key_value in ret_line_split:
            if 'cur=' in key_value:
                value = key_value.strip().split("=")[1]
                x, y = value.split("x")
                return int(x), int(y)
        return None, None

    def push_file(self, src_file_path, des_file_path):
        """
        push 文件至设备中
        Args:
            package: app包名
        Returns:
            True:已经安装，False：未安装
        """
        if not os.path.exists(src_file_path):
            g_logger.error("not found file {}".format(src_file_path))
        return self.adb("push {} {}".format(src_file_path, des_file_path), str_flag=False)

    def pull_file(self, src_file_path, des_file_path):
        """
        从设备中pull出来
        Args:
            src_file_path: 手机中的图片路径
            des_file_path: 本地保存的路径
        Returns:
            True:已经安装，False：未安装
        """
        return self.adb("pull {} {}".format(src_file_path, des_file_path), str_flag=False, log=False)

    def grant(self, permission=None, package='com.qiyi.video'):
        """
        app授权
        Args:
            permission: 权限，若为None，则申请存储、位置和手机相关的权限，否则按照传过来的权限授权
            package: 授权的app包名
        Returns:
            False: 参数传递失败，True: 执行完授权命令
        """
        if not permission:
            pers = PERMISSIONS.values()
        elif isinstance(permission, str):
            pers = [permission]
        elif isinstance(permission, (list, tuple)):
            pers = list(permission)
        else:
            return False
        for per in pers:
            self.adb_shell("pm grant {} {}".format(package, per))
            time.sleep(0.5)
        return True

    def grant_shortcut(self, package='com.qiyi.video'):
        """
        添加快捷方式
        Args:
            package: app包名

        Returns:

        """
        pers = ["com.android.launcher.permission.INSTALL_SHORTCUT", "com.android.launcher2.permission.INSTALL_SHORTCUT",
                "com.android.launcher3.permission.INSTALL_SHORTCUT"]
        return self.grant(pers, package=package)

    def screen_shot(self, screen_path):
        """
        手机截图
        Args:
            screen_path: 图片本地保存路径
        Returns:
            True
        """
        sdcard_path = "/sdcard/1.png"
        self.adb_shell("screencap {}".format(sdcard_path), str_flag=False, log=False)
        self.pull_file(sdcard_path, screen_path)
        return True


if __name__ == '__main__':
    adb = Adb()
    out = adb.get_window_size()
    out = adb.adb_shell("cat /sdcard/ipecker_log.txt")
    print(adb.install_apk("ipecker.apk"))
    is_install = adb.check_app_is_install("com.iqiyi.ipecker")
    print(adb.check_ipecker_log_exist())
    devices = adb.get_device_list()
    print(devices)

    print(adb.get_release_version())
    print(adb.get_sdk_version())

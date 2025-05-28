# -*- coding: UTF-8 -*-

"""
File Name:      appium
Author:         zhangwei04
Create Date:    2018/1/9
"""
import time
import platform
from framework.core.resource import g_resource, const
from framework.utils.threads import IpeckerThread
from framework.utils.sys_shell import kill_process, get_pid, is_port_used
from framework.logger.logger import g_framework_logger


class AppiumServer(object):
    """
    Appium Server类
    """
    __port = 4723

    def __init__(self, log_file):
        self.__log_file = log_file
        self.timeout = 600
        self.__server_thread = None

        self.__pid = None
        self.__address = '127.0.0.1'
        self.__port = None

    def __del__(self):
        if self.__server_thread and not self.__server_thread.is_stop:
            self.__server_thread.stop()

    @property
    def pid(self):
        """
        Returns:
            Appium Server 进程ID
        """
        return self.pid

    @property
    def port(self):
        """
        Returns:
            Appium Server 端口号
        """
        return self.__port

    @property
    def url(self):
        """
        Returns:
            Appium Server URL
        """
        return "http://{}:{}/wd/hub".format(self.__address, self.__port)

    def start(self):
        """
        启动Appium Server
        """
        # 找到空闲端口
        for i in range(100):
            self.__port = AppiumServer.__port
            AppiumServer.__port += 2
            if not is_port_used(self.__port):
                break

        pre_pid = get_pid('node.exe' if g_resource['system'] == const.SYSTEM_WINDOWS else 'appium')

        # 待区分android和ios端口
        if g_resource['system'] == const.SYSTEM_MAC:
            cmd = "appium -a {} -p {} --webdriveragent-port {} --command-timeout {} --pre-launch"
        else:
            cmd = "appium -a {} -p {} -bp {}  --command-timeout {} --pre-launch"
        cmd = cmd.format(self.__address, self.__port, self.__port + 1, self.timeout)

        g_framework_logger.info("start appium server: {}".format(cmd))
        self.__server_thread = IpeckerThread(cmd, log_file=self.__log_file, shell=True)
        self.__server_thread.start()
        time.sleep(5)
        after_pid = get_pid('node.exe' if g_resource['system'] == const.SYSTEM_WINDOWS else 'appium')

        pid_set = after_pid - pre_pid
        if pid_set:
            self.__pid = pid_set.pop()
        pass

    def stop(self):
        """
        停止Appium Servere
        """
        g_framework_logger.info("stop appium server")
        self.__server_thread.stop()
        # window下待添加杀掉node进程流程
        if platform.system() == 'Windows':
            kill_process(pname='node.exe', pid=self.__pid)
        else:
            kill_process(pname='appium', pid=self.__pid)


if __name__ == '__main__':
    a = AppiumServer(log_file='appium1_log.txt')
    b = AppiumServer(log_file='appium2_log.txt')
    a.start()
    b.start()
    time.sleep(5)

    a.stop()
    b.stop()

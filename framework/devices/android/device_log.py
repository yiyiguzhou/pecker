# -*- coding: UTF-8 -*-

"""
File Name:      device_log
Author:         zhangwei04
Create Date:    2018/2/8
"""
import time
from framework.utils.sys_shell import get_pid, kill_process
from framework.core.resource import g_resource, const
from framework.utils.threads import IpeckerThread
from framework.devices.android.adb import Adb


class Logcat(object):
    """logcat日志捕获类"""
    def __init__(self, adb=None, dev_id=None):
        self.__thread = None
        self.__id = dev_id
        self.__cmd = ["adb"]
        self.__pid = None
        self.__adb = adb if adb else Adb(dev_id)

    def start(self, log_path=None, param=None, clear_buffer=True):
        """
        开启logcat日志
        Args:
            log_path: 日志存放路径，包含文件名
            param: 日志捕获时参数
            clear_buffer: 是否清楚buffer
        """
        if clear_buffer:
            self.__adb.adb("logcat -c", str_flag=False)

        cmd = self.__cmd
        if self.__id:
            cmd.append("-s %s" % self.__id)

        cmd.extend(["logcat", param]) if param else cmd.append("logcat")

        cmd = " ".join(cmd)
        back_id_set = self.__adb.get_pid('logcat')

        self.__thread = IpeckerThread(cmd, log_file=log_path, time_interval=0.01,
                                      shell=g_resource['system'] == const.SYSTEM_LINUX)
        self.__thread.start()
        time.sleep(1)
        self.__pid = self.__adb.get_pid('logcat') - back_id_set

    def stop(self):
        """停止日志捕获"""
        if self.__thread:
            self.__thread.stop()
        # 通过手机测杀掉线程
        if self.__pid:
            self.__adb.kill_process(self.__pid)


if __name__ == '__main__':
    logcat_list = []
    for i in range(3):
        logcat = Logcat()
        logcat.start('logcat_{}_log.txt'.format(i + 1))
        logcat_list.append(logcat)
    time.sleep(1)
    with open('logcat_1_log.txt', 'r') as fp:
        for i in range(300):
            print("current time: %d" % (i + 1))
            for line in fp:
                if "CHECK_INTERVAL" in line:
                    print(line)
                    break
            time.sleep(0.1)
    for logcat in logcat_list:
        logcat.stop()

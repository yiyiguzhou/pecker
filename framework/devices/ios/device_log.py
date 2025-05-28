# -*- coding: UTF-8 -*-

"""
File Name:      device_log
Author:         wzhang
Create Date:    2018/3/9
"""
import time
from framework.utils.threads import IpeckerThread
from framework.core.resource import g_resource, const
from framework.utils.sys_shell import get_pid


class IdeviceSysLog(object):
    def __init__(self, dev_id=None):
        self.__therad = None
        self.__id = dev_id
        self.__pid = None
        self.__cmd = "idevicesyslog"

    def start(self, log_path=None, param=None):
        """
        开启IOS设备系统日志
        Args:
            log_path:
            param:

        Returns:

        """
        if self.__id:
            self.__cmd = "idevicesyslog -u {}".format(self.__id)

        back_id_set = get_pid(self.__cmd)
        self.__therad = IpeckerThread(self.__cmd, log_file=log_path, time_interval=0.01,
                                      shell=g_resource['system'] == const.SYSTEM_MAC)
        self.__therad.start()
        time.sleep(1)
        self.__pid = get_pid(self.__cmd) - back_id_set

    def stop(self):
        if self.__therad:
            self.__therad.stop()


if __name__ == '__main__':
    device_log_list = []
    for i in range(3):
        idevlog = IdeviceSysLog()
        idevlog.start('idevice_{}_log.txt'.format(i + 1))
        time.sleep(10)
        device_log_list.append(idevlog)

    for idevlog in device_log_list:
        idevlog.stop()
# -*- coding: UTF-8 -*-

"""
File Name:      performance
Author:         zhangwei04
Create Date:    2018/5/29
"""
import os
import time
from framework.core.resource import g_resource, const
from framework.utils.threads import IpeckerRepeatThread, IpeckerPopen


class Performance(object):
    """性能数据捕获类，用于捕获CPU 内存及流量信息"""
    def __init__(self, device=None):
        self._device = device

        self.__cpu_catch_thread = None
        self.__mem_catch_thread = None
        self.__rcv_net_flow_catch_thread = None
        self.__snd_net_flow_catch_thread = None

        self.__shell = g_resource['system'] == const.SYSTEM_LINUX
        self.__cath_flow_flag = False

    def start_catch(self, log_dir, app_package, time_interval=1):
        """开始数据性能捕获"""
        log_path_module = os.path.join(log_dir, "{}_{}_{}_log.txt")
        self.catch_cpu(app_package, log_path_module.format(self._device.target.name,
                                                          self._device.id, "cpuinfo"), time_interval=time_interval)
        self.catch_mem(app_package, log_path_module.format(self._device.target.name,
                                                           self._device.id, "meminfo"), time_interval=time_interval)
        self.catch_net_flow(app_package, log_path_module.format(self._device.target.name,self._device.id, "flow_snd"),
                            log_path_module.format(self._device.target.name, self._device.id, "flow_rcv"), time_interval=time_interval)

    def stop(self):
        """停止性能数据捕获"""
        if self.__cpu_catch_thread:
            self.__cpu_catch_thread.stop()
        if self.__mem_catch_thread:
            self.__mem_catch_thread.stop()
        if self.__rcv_net_flow_catch_thread:
            self.__rcv_net_flow_catch_thread.stop()
        if self.__snd_net_flow_catch_thread:
            self.__snd_net_flow_catch_thread.stop()

        self.__cath_flow_flag = False

    def catch_cpu(self, app_package, log_path, time_interval=1):
        """捕获app 使用CPU信息
        Args:
            app_package: app 包名
            log_path: 数据存放文件
            time_interval: 抓取时间间隔
        """
        self.__cpu_catch_thread = self.__run_dumpsys_thread(app_package, "cpuinfo", log_path, time_interval=time_interval)

    def catch_mem(self, app_package, log_path, time_interval=1):
        """捕获app 使用内存信息信息
        Args:
            app_package: app 包名
            log_path: 数据存放文件
            time_interval: 抓取时间间隔
        """
        self.__mem_catch_thread = self.__run_dumpsys_thread(app_package, "meminfo", log_path, time_interval=time_interval)

    def catch_net_flow(self, app_package, log_snd_path, log_rcv_path, time_interval=1):
        """捕获app 使用CPU信息
        Args:
            app_package: app 包名
            log_snd_path: 发送数据存放文件
            log_rcv_path: 接受数据文件
            time_interval: 抓取时间间隔
        """
        self.__cath_flow_flag = True
        self.__rcv_net_flow_catch_thread = IpeckerRepeatThread()
        self.__snd_net_flow_catch_thread = IpeckerRepeatThread()
        self.__rcv_net_flow_catch_thread.start(self._start_snd_flow_thread, app_package=app_package, log_file=log_rcv_path, time_interval=time_interval)
        self.__snd_net_flow_catch_thread.start(self._start_rcv_flow_thread, app_package=app_package, log_file=log_snd_path, time_interval=time_interval)

    def _start_snd_flow_thread(self, app_package=None, log_file=None, time_interval=None):
        """
        开启发送流量捕获线程
        Args:
            app_package: app 包名
            log_file: 线程输出文件名
            time_interval: 捕获间隔，单位：秒
        """
        self.__run_flow_thread(app_package, log_file, time_interval, "tcp_snd")

    def _start_rcv_flow_thread(self, app_package=None, log_file=None, time_interval=None):
        """
        开启接收流量捕获线程
        Args:
            app_package: app 包名
            log_file: 线程输出文件名
            time_interval: 捕获间隔，单位：秒
        """
        self.__run_flow_thread(app_package, log_file, time_interval, "tcp_rcv")

    def __run_flow_thread(self, app_package, log_file, time_interval, catch_tpye):
        """
        执行流量线程
        Args:
            app_package: app 包名
            log_file: 线程输出文件名
            time_interval: 捕获间隔，单位：秒
            catch_tpye: 捕获类型，tcp_snd，tcp_rcv
        """
        with open(log_file, "a+") as fp:
            uid = None
            while self.__cath_flow_flag:
                if not uid:
                    uid = self._device.adb.get_app_uid(app_package, log_type="framework")
                    time.sleep(time_interval)
                    if not uid:
                        continue
                    if self._device.id:
                        cmd = "adb -s {} shell  cat /proc/uid_stat/{}/{}".format(self._device.id, uid, catch_tpye)
                    else:
                        cmd = "adb shell cat /proc/uid_stat/{}/{}".format(uid, catch_tpye)
                fp.writelines(IpeckerRepeatThread.get_time_stamp())
                fp.flush()
                with IpeckerPopen(cmd, stdout=fp, shell=self.__shell):
                    time.sleep(time_interval)

    def __run_dumpsys_thread(self, app_package, cathe_type, log_path, time_interval=1):
        """执行dumpsys命令
        Args:
            app_package: app包名
            cathe_type: 捕获信息类型，如meminfo、cpuinfo
            log_path: 数据写入文件
            time_interval: 抓取时间间隔
        """
        cmd = ["adb "]
        if self._device.id:
            cmd.append("-s {}".format(self._device.id))
        cmd.append('shell "dumpsys {} | grep {}"'.format(cathe_type, app_package))
        thread = IpeckerRepeatThread(" ".join(cmd), log_file=log_path, time_interval=time_interval, shell=self.__shell)
        thread.start()
        return thread

    def get_app_start_time(self, app_package):
        pass
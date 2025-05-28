# -*- coding: UTF-8 -*-

"""
File Name:      sys_shell
Author:         zhangwei04
Create Date:    2018/1/16
"""
import re
import platform
from framework.utils.threads import IpeckerPopen
from framework.exception.exception import DeviceNotFound, DeviceUnauthorized

_plat = platform.system()
_shell = False if _plat == 'Windows' else True


def kill_process(pid=None, pname=None):
    """
    根据进程名或者进程ID杀掉进程
    Args:
        pid: 进程ID
        pname: 进程名

    Returns:
        执行命令返回的信息
    """
    if not pid and not pname:
        return None

    if pid and isinstance(pid, (set, list)):
        pid = " /PID ".join(pid) if _plat == 'Windows' else " ".join(pid)

    if _plat == 'Windows':
        if pid:
            cmd = "taskkill /PID {} /F".format(pid)
        else:
            cmd = "taskkill /IM {} /F".format(pname)
    elif _plat == 'Linux':
        cmd = "ps -ef"
        for key in (pid, pname):
            if key:
                cmd = "{} | grep {}".format(cmd, key)
        cmd = "kill -9 `%s | awk '{print $2}'`" % cmd
    else:   # MAC
        if pid:
            cmd = "kill -9 %s" % pid
        else:
            pid_set = get_pid(pname)
            cmd = "kill -9 %s" % " ".join(pid_set)
    p = IpeckerPopen(cmd, timeout=3, shell=_shell)
    return p.execute()


def get_pid(pname, all_flag=True):
    """
    根据进程名获取进程id
    Args:
        pname: 进程名字
        all_flag: 全部执行进程标志

    Returns:
        进程id集合
    """
    if not pname:
        return None
    pid_set = set()

    if _plat == 'Windows':
        cmd = "tasklist | findstr {}".format(pname)
        import os
        a = os.popen(cmd)
        outs = a.read()
    else:
        if all_flag:
            cmd = "ps -ef | grep {}".format(pname)
        else:
            cmd = "ps | grep {}".format(pname)
        p = IpeckerPopen(cmd, timeout=3, shell=_shell)
        outs, errs = p.execute()
    if outs:
        line_split = outs.splitlines()
        for line in line_split:
            line_format = line.strip()
            if line_format and "grep {}".format(pname) not in line_format:
                split_msg = line_format.split()
                if len(split_msg) > 2 and split_msg[1].isdigit():
                    pid_set.add(split_msg[1])
    return pid_set


def is_port_used(port):
    """
    判断tcp端口是否被使用
    Args:
        port: 端口号

    Returns:
        是否被使用
    """
    if isinstance(port, int):
        port = str(port)
    return port in _get_used_port()


def _get_used_port():
    """
    获取已经被使用的端口集合
    Returns:
        已经使用的端口集合
    """
    if _plat in ('Windows', 'Linux'):
        cmd = "netstat -ano"
        pattern = r'127.0.0.1:(\d{1,5})'
    else:   # IOS
        cmd = "lsof -i tcp"
        pattern = r'localhost:(\d{1,5})'
    p = IpeckerPopen(cmd, timeout=3, shell=_shell)
    outs, errs = p.execute()
    if outs:
        port_list = re.findall(pattern, outs)
        return port_list
    return []


def get_dev_list():
    """
    获取设备列表
    Returns:
        设备列表，若没有连接设备，返回空列表
    """
    device_list = []
    shell = False if _plat == 'Windows' else True
    if _plat in ('Windows', 'Linux'):
        cmd = "adb devices"
        p = IpeckerPopen(cmd, shell=shell, timeout=5)
        outs, errs = p.execute()
        if outs:
            lines = outs.splitlines()
            for line in lines:
                line_format = line.strip()
                if line_format.endswith('device'):
                    line_split = line_format.split()
                    device_list.append({'id': line_split[0], 'status': 'free'})
                elif line_format.endswith('unauthorized'):
                    raise DeviceUnauthorized(line_format)
                else:
                    continue
    else:   # ios 平台
        cmd = "idevice_id -l"
        p = IpeckerPopen(cmd, shell=shell, timeout=5)
        outs, errs = p.execute()
        if outs:
            lines = outs.splitlines()
            for line in lines:
                device_list.append({'id': line.strip(), 'status': 'free'})
    return device_list


def check_device(dev_id, dev_list=None):
    """
    检测配置的设备是否在连接的设备列表中
    Args:
        dev_id: 配置的设备id
        dev_list: 实际连接的设备列表

    Returns:
        True: 设备在连接设备列表中
        False: 设备不在连接设备列表中
    """
    if not dev_list:
        dev_list = get_dev_list()
    return dev_id in [dev.get('id') for dev in dev_list]


if __name__ == '__main__':
    device_list = get_dev_list()
    print(device_list)
    print(check_device("1a91dcad"))
    kill_process(pname='idevicesyslog')

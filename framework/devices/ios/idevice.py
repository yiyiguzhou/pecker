# -*- coding: UTF-8 -*-

"""
File Name:      idevice
Author:         wzhang
Create Date:    2018/1/29
"""
from framework.utils.threads import IpeckerPopen


class IDevice(object):
    """
    IOS设备命令行方式通讯类
    """
    def __init__(self, udid=None):
        self.__id = udid
        self.info = self.__get_device_info()

    def get_device_name(self):
        """
        获取设备名称
        Returns:
            设备名称列表
        """
        cmd = "idevicename -u {}".format(self.__id) if self.__id else "idevicename"
        p = IpeckerPopen(cmd, timeout=3)
        outs, errs = p.execute()
        return self.__split_lines(outs)

    @property
    def product_version(self):
        """
        获取设备产品版本
        Returns:
            设备产品版本
        """
        product_ver = self.info.get('ProductVersion', '10.3')
        if product_ver.count('.') > 1:
            return ".".join(product_ver.split('.')[:2])
        return '10.3'

    def __get_device_info(self):
        """
        获取设备信息，将获取到的信息存储到字典中
        Returns:
            设备信息字典
        """
        cmd = "ideviceinfo -u {}".format(self.__id) if self.__id else "ideviceinfo"
        p = IpeckerPopen(cmd, shell=True, timeout=3)
        outs, errs = p.execute()
        outs_line = self.__split_lines(outs)

        info_dict = {}
        for line in outs_line:
            line_striped = line.strip()
            if line_striped:
                line_split = line_striped.split(":")
                if len(line_split) == 2:
                    info_dict[line_split[0].strip()] = line_split[1].strip()
        return info_dict

    def __split_lines(self, outs):
        """
        字符串分割行操作
        Args:
            outs: 待分割字符串
        Returns:
            分割后的字符串，若outs字符串为空，则返回None
        """
        if not outs:
            return None

        out_list = outs.splitlines()
        ret_list = []
        for line in out_list:
            line_striped = line.strip()
            if line_striped:
                ret_list.append(line_striped)
        return ret_list


if __name__ == "__main__":
    dev = IDevice()
    name = dev.get_device_name()
    print(name)
    for key,value in dev.info.items():
        print(key, ":", value)

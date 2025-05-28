# -*- coding: UTF-8 -*-

"""
File Name:      ftp
Author:         zhangwei04
Create Date:    2018/5/16
"""

import os
from framework.utils.iftp.ftplib import FTP
from framework.logger.logger import g_framework_logger


class IpeckerFtp(object):
    """IpeckerFtp工具，用于报告上传"""
    def __init__(self, host='10.5.170.105', port=0, user='ftptest', passwd='ftptest', base_path=None, timeout=60):
        """
        初始化FTP操作类
        Args:
            host: 服务器地址
            port: 服务器端口号
            user: 用户名
            passwd: 密码
            base_path: 服务器地址基础路径
            timeout: 超时
            __ftp：ftp操作对象
        """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.base_path = base_path
        self.base_local_dir = ""
        self.timeout = timeout
        self.__ftp = None

    def login(self):
        """登录ftp服务器"""
        self.__ftp = FTP()
        self.__ftp.connect(self.host, self.port, timeout=self.timeout)
        self.__ftp.login(self.user, self.passwd)
        if self.base_path:
            self.__ftp.cwd(self.base_path)

    def upload_dir(self, local_dir, ftp_dir=None):
        """
        上传本地目录至服务器上
        Args:
            local_dir: 带传本地目录
            ftp_dir: ftp服务器基目录
        """
        g_framework_logger.info("uploaddir {}".format(local_dir), console=False)
        if not os.path.isdir(local_dir):
            return False
        if not self.__ftp:
            self.login()

        self.base_local_dir, cur_dir_name = os.path.split(os.path.abspath(local_dir))

        if ftp_dir:
            self.base_path = ftp_dir
        # 遍历目录上传文件
        self.__up_dirs(cur_dir_name)

        self.base_local_dir = None  # 恢复变量

    def __up_dirs(self, curt_dir):
        """
        遍历目录树，创建目录树及上传对应目录下的文件
        Args:
            curt_dir: 上传目录路径
        """
        if self.base_path:
            self.__ftp.cwd(self.base_path)

        walks = os.walk(os.path.join(self.base_local_dir, curt_dir))
        for dirpath, dirs, files in walks:
            if self.base_local_dir:
                curt_dir = dirpath[len(self.base_local_dir) + 1:].replace("\\", "/")    # 截取相对目录路径
            else:
                curt_dir = dirpath.replace("\\", "/")

            self.mk_dir(curt_dir)
            # 上传文件至目录上
            for f in files:
                file_path = "{}/{}".format(curt_dir, f)
                with open(os.path.join(dirpath, f), 'rb') as file_handle:
                    self.__ftp.storbinary("STOR {}".format(file_path), file_handle)  # 上传目标文件

    def mk_dir(self, curt_dir, base_dir=None):
        """
        创建dir
        Args:
            curt_dir: 待创建目录路径
            base_dir: 服务器基本路径
        """
        if base_dir:
            self.__ftp.cwd(base_dir)
        try:
            self.__ftp.mkd(curt_dir)
        except Exception as e:  # 目录已存在 会抛出异常
            g_framework_logger.error("ftp: {} 目录创建失败，请检查是否已经存在".format(str(e)), console=False)


if __name__ == "__main__":
    ftp = IpeckerFtp(base_path='/auto/http_server')
    ftp.upload_dir("D:\\code\\svn\\ipecker\\project\\result\\test")
    pass
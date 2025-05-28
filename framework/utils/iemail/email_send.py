# -*- coding: UTF-8 -*-

"""
File Name:      email
Author:         zhangwei04
Create Date:    2018/5/23
"""

import smtplib

from email.message import EmailMessage
from framework.logger.logger import g_framework_logger


class Email(object):
    """邮件功能类"""
    def __init__(self, user, passwd, address, host="mail.iqiyi.com", port=465):
        """
        Args:
            user: 邮件登录用户名
            passwd: 邮件登录用户密码
            address: 邮箱号
            host: SMTP服务器地址
            port: SMTP服务器端口号
        """
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port

        self.__msg = EmailMessage()
        self.__msg['From'] = address

    def send(self, subject, to, cc=[]):
        """
        邮件发送
        Args:
            subject: 邮件主题
            to: 接收人列表
            cc: 抄送人列表
        """
        self.__msg['Subject'] = subject
        self.__msg['To'] = to
        self.__msg['cc'] = cc
        try:
            with smtplib.SMTP(self.host, self.port) as smtp:
                smtp.login(self.user, self.passwd)
                smtp.send_message(self.__msg)
        except Exception as e:
            g_framework_logger.error("send email failed!")
            g_framework_logger.error(str(e))
            raise e

    def add_content(self, msg_content, subtype='text'):
        """添加邮件内容
        Args:
            msg_content: 内容字符串
            sbutype: 内容类型
        """
        self.__msg.add_alternative(msg_content, subtype=subtype)


if __name__ == "__main__":
    e = Email("zhangwei04", "!FENG122772", "zhangwei04@qiyi.com")
    msg = """\
    <html>
      <head></head>
      <body>
        <p>iPecker 测试完成</p>
        <p> 报告链接：<a href="http://10.5.170.105:8080/05-18_18_38_11/report.html">结果报告链接</a> </p>
      </body>
    </html>
    """
    subtype = 'html'
    e.add_content(msg, subtype)
    e.send("iPecker测试结果", ["zhangwei04@qiyi.com"], cc=[])
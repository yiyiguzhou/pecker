# -*- coding: UTF-8 -*-

"""
File Name:      email_report
Author:         zhangwei04
Create Date:    2018/5/25
"""
import os
import base64
import configparser
from framework.utils.iemail.email_send import Email
from framework.report.html_report.report_html import ReportHtml
from framework.core.resource import g_resource
from framework.logger.logger import g_logger


class EmailReport(object):
    """发送结果邮件类，框架执行结尾时，若将结果上传到http服务器，则发送邮件通知"""
    def __init__(self, result=None):
        self.__result = result
        conf_file = os.path.join(os.path.dirname(__file__), "conf.txt")
        conf = configparser.ConfigParser()
        section = "send_user"
        with open(conf_file, 'r', encoding='utf-8') as fp:
            conf.read_file(fp)
            user=conf.get(section, "user")
            passwd = conf.get(section, "passwd")
            self.__email = Email(base64.decodebytes(bytes(conf.get(section, "user"), encoding='utf-8')).decode(),
                                 base64.decodebytes(bytes(conf.get(section, "passwd"), encoding='utf-8')).decode(),
                                 conf.get(section, "email_addr"))

    def send_html_report(self):
        """
        发送html格式报告邮件
        """
        self.__email.add_content(self.html_msg(), subtype='html')
        # 读取发送人员信息

        to, cc = self.__get_email_to_cc()
        if not to:
            return
        self.__email.send(subject="iPecker 执行报告", to=to, cc=cc)

    def html_msg(self):
        """html 内容信息"""
        parmeter = g_resource["aml_data"]['parameter']
        host = parmeter.get("server_localhost")
        port = parmeter.get("http_server_port", 8080)
        log_name = os.path.split(g_resource["log_path"])[1]

        url = "http://{host}:{port}/{log_name}/report.html".format(host=host, port=port, log_name=log_name)
        # return """\
        #  <html>
        #   <head>
        #      <link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
	    #      <script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
	    #      <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        #   </head>
        #   <body>
        #     <h3 align="center">iPecker 测试完成</h3>
        #     <table border="1" class="table table-bordered table-striped " id="totalTable">
        #         <tr>
        #             <th>开始时间</th>
        #             <th>{start_time}</th>
        #         </tr>
        #         <tr>
        #             <th>运行时间</th>
        #             <th>{run_time}</th>
        #         </tr>
        #         <tr>
        #             <th>报告链接</th>
        #             <th><a href={url}>点击前往链接</a></th>
        #         </tr>
        #     </table>
        #   </body>
        # </html>
        # """.format(url=url, start_time=self.__result.start_time, run_time=self.__result.run_time)
        report_html = ReportHtml()
        return report_html.report_email(self.__result, url=url)

    @classmethod
    def __get_email_to_cc(cls):
        """读取配置文件，获取收件人及抄送人
        Returns:
            收件人列表，抄送人列表
        """
        to = []
        cc = []
        # 读取环境变量
        email_conf_name = os.environ.get("EMAIL_CONF", "email.conf")

        conf_path = os.path.join(g_resource['project_path'], "conf", email_conf_name)
        if not os.path.exists(conf_path):
            g_logger.warning("can not find email.conf file in {}, and we will not send".format(conf_path))
            return to, cc
        with open(conf_path, 'r', encoding='utf-8') as fp:
            flag = ""
            for line in fp:
                line = line.strip(" :[]\n")
                if line:
                    if line == "to":
                        flag = "to"
                    elif line == "cc":
                        flag = "cc"
                    else:
                        if line.startswith((";", "#")):
                            continue
                        if flag == "to":
                            to.append(line)
                        elif flag == "cc":
                            cc.append(line)

        return to, cc


if __name__ == "__main__":
    g_resource["aml_data"]['parameter'] = {"server_localhost": "10.5.170.105",
                                           "http_server_port": 8080}
    er = EmailReport()
    # print(er.html_msg)
    er.send_html_report()
    pass

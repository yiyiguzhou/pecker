# -*- coding: UTF-8 -*-

"""
File Name:      run
Author:         zhangwei04
Create Date:    2018/4/23
"""


import os
from framework.utils.jinja2.jinja2 import Environment, FileSystemLoader
from framework.core.resource import g_resource


class ReportHtml(object):
    def __init__(self):
        # 模板文件的目录
        self.html_module_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
        # 设置jinja2的环境配置
        self.env = Environment(loader=FileSystemLoader(self.html_module_path),
                          extensions=['framework.utils.jinja2.jinja2.ext.do'])

    def report(self, result):
        """
        生成总的html报告
        Args:
            result: 工程结果类
        """
        report = self.env.get_template('report.html')
        # 将结果类传递到模板中，进行渲染
        html_rep = report.render(testresult=result)

        report_path = os.path.join(g_resource['log_path'], 'report.html')
        with open(report_path, 'w', encoding='utf-8') as handle:
            handle.write(html_rep)

    def report_testcase(self, testcase_result, targets=None):
        """
        生成用例报告
        Args:
            testcase_result:用例结果报告
        """
        target_name_list = []
        if targets:
            for target in targets:
                if target.device and target.device.inited:
                    log_type = "logcat" if target.data.get("type", "") else "idevicesys"
                    if testcase_result.loop_times > 1:
                        tmp_log_name = "{}_{}_loop1_log.txt".format(target.name, log_type)
                    else:
                        tmp_log_name = "{}_{}_log.txt".format(target.name, log_type)
                    if os.path.exists(os.path.join(testcase_result.log_abs_dir, tmp_log_name)):
                        target_name_list.append((target.name, log_type))

        testcast_report = self.env.get_template('testcase_loop_report.html')
        html_rep = testcast_report.render(testcaseResult=testcase_result, target_name_list=target_name_list)
        rpt_path = os.path.join(g_resource['log_path'], testcase_result.report_path)
        with open(rpt_path, 'w', encoding='utf-8') as handle:
            handle.write(html_rep)

    def report_email(self, result, url):
        """工程执行结束后，生成发送Email报告内容
        Args:
            result: 工程结果类
        """
        email_report = self.env.get_template('email_report.html').render(testResult=result, url=url)
        return email_report


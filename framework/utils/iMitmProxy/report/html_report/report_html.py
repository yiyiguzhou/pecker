# -*- coding: UTF-8 -*-

"""
File Name:      run
Author:         zhangwei04
Create Date:    2018/4/23
"""

import time
import os
from framework.core.resource import g_resource

report_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'result', time.strftime("%m-%d_%H_%M_%S", time.localtime(time.time())))
# if not os.path.exists(report_dir):
#     os.makedirs(report_dir)

from framework.utils.jinja2.jinja2 import Environment, FileSystemLoader


class ReportHtml(object):
    def __init__(self):
        # 模板文件的目录
        self.html_module_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
        # 设置jinja2的环境配置
        self.env = Environment(loader=FileSystemLoader(self.html_module_path),
                          extensions=['framework.utils.jinja2.jinja2.ext.do'])

    def report_pingback(self, result, actions):
        for i, conf_msg in enumerate(result):
            # 生成每个action报告
            self._repot_action_report(conf_msg, i, report_dir)
            self._report_action_params(conf_msg, i, report_dir)

        pingback_report = self.env.get_template('pingback_report.html')
        html_rep = pingback_report.render(result=result, actions=actions)

        report_path = os.path.join(report_dir, 'report.html')
        with open(report_path, 'w', encoding='utf-8') as handle:
            handle.write(html_rep)

    def report_ipecker_pingback(self, pingback_testcase_result):
        pingback_testcase_result.add_log_path()  # 添加本地及相对目录
        # 步骤报告
        for step_result in pingback_testcase_result.results:
            self._report_ipecker_step_pingback(step_result)

        pingback_report = self.env.get_template('pingback_testcase_report.html')
        html_rep = pingback_report.render(result=pingback_testcase_result)
        with open(pingback_testcase_result.abs_log_path, 'w', encoding='utf-8') as handle:
            handle.write(html_rep)

    def _report_ipecker_step_pingback(self, step_result):
        # 只有一个数据投递，则直接在用例表里面链接，多个新生成步骤表
        pb_step_report = self.env.get_template('pingback_step_report.html')
        step_result.add_log_path()

        # 生成参数报告
        for params_result in step_result.results:
            params_result.add_log_path()
            self._report_ipecker_params(params_result)

        html_step_rep = pb_step_report.render(result=step_result)
        with open(step_result.abs_log_path, 'w', encoding='utf-8') as handle:
            handle.write(html_step_rep)

    def _report_ipecker_params(self, action_result):
        # 生成参数比较详情报告
        for i, params_result_dict in enumerate(action_result.cmp_result):
            params_result_dict['rel_log_path'] = "params_{}_{}.html".format(action_result.index, i)

            pb_params_detail_report = self.env.get_template('pingback_action_params_report.html')
            html_params_detail_rep = pb_params_detail_report.render(result=params_result_dict)
            abs_log_path = os.path.join(action_result.abs_log_dir, "params_{}_{}.html".format(action_result.index, i))
            with open(abs_log_path, 'w', encoding='utf-8') as handle:
                handle.write(html_params_detail_rep)

        pb_params_report = self.env.get_template('pingback_step_action_report.html')
        html_params_rep = pb_params_report.render(result=action_result)
        with open(action_result.abs_log_path, 'w', encoding='utf-8') as handle:
            handle.write(html_params_rep)

    def _report_action_report(self, conf_msg, action_num, report_dir):
        # 生成action报告路径
        action_report_dir = os.path.join(report_dir, 'action_report')
        if not os.path.exists(action_report_dir):
            os.makedirs(action_report_dir)

        action_report_path = os.path.join(action_report_dir, '{}.html'.format(action_num))
        conf_msg['action_report_path'] = "action_report/{}.html".format(action_num)

        action_report = self.env.get_template('pingback_action_report.html')
        html_action_report = action_report.render(result=conf_msg, action_num=action_num)

        with open(action_report_path, 'w', encoding='utf-8') as handle:
            handle.write(html_action_report)

    def _report_action_params(self, conf_msg, action_num, report_dir):
        action_params_report_dir = os.path.join(report_dir, 'action_report',
                                                '{}_{}'.format(conf_msg['desc'], action_num))
        if not os.path.exists(action_params_report_dir):
            os.makedirs(action_params_report_dir)

        # 生成各个http参数报告
        for i, http_msg in enumerate(conf_msg['cmp_result']['http_list']):
            action_params_rpt = self.env.get_template('pingback_action_params_report.html')
            html_action_params_rpt = action_params_rpt.render(result=http_msg['cmp_result'])

            action_params_report_path = os.path.join(action_params_report_dir, '{}.html'.format(i))
            with open(action_params_report_path, 'w', encoding='utf-8') as handle:
                handle.write(html_action_params_rpt)




# -*- coding: UTF-8 -*-

"""
File Name:      result
Author:         zhangwei04
Create Date:    2018/8/16
"""
import os
from framework.core.resource import g_resource


class PingBackTestCase(object):
    """PingBack测试用例结果类"""
    def __init__(self):
        self.results = []  # 步骤结果类
        self.status = 'not_run'
        self.rel_log_path = ""
        self.abs_log_path = ""

    def add_result(self, result):
        self.results.append(result)

    def add_log_path(self):
        # 添加路径
        log_relative_dir = g_resource['testcase_log_dir'][len(g_resource['log_path']):].lstrip('\\/')  # 添加用例相对目录
        abs_report_dir = os.path.join(g_resource['testcase_log_dir'], "pingback")   # 添加本地目录路径
        report_dir = "pingback"

        loop = g_resource['testcase_loop']
        if loop != 0:   # 压测时，需要创建压测目录
            report_dir = os.path.join(report_dir, "loop_{}".format(loop))
            abs_report_dir = os.path.join(abs_report_dir, "loop_{}".format(loop))

        self.rel_log_path = os.path.join(report_dir, 'report.html')
        # 创建用例pingback本地报告目录
        if not os.path.exists(abs_report_dir):
            os.makedirs(abs_report_dir)
        self.abs_log_path = os.path.join(abs_report_dir, 'report.html')


class PingBackTestCaseStep(object):
    """需要PingBackTestCase添加此步骤的结果类后，才能使用此类生成报告"""
    def __init__(self, desc=""):
        self._results = []  # http比较结果类
        # self.status = 'not_run'
        self.parent = None
        self.rel_log_path = ""
        self.abs_log_path = ""
        self.desc = desc

    def add_log_path(self):
        if not self.parent.rel_log_path:
            self.parent.add_log_path()
        step_index = self.index

        rel_log_dir = 'step_{}'.format(step_index)
        abs_log_dir = os.path.join(os.path.split(self.parent.abs_log_path)[0], 'step_{}'.format(step_index))
        if not os.path.exists(abs_log_dir):
            os.makedirs(abs_log_dir)

        self.rel_log_path = os.path.join(rel_log_dir, "step_report.html".format(step_index))
        self.abs_log_path = os.path.join(abs_log_dir, "step_report.html".format(step_index))

    def add_result(self, result):
        self.results.append(result)

    @property
    def results(self):
        return self._results

    @property
    def index(self):
        return self.parent.results.index(self)

    @property
    def rel_log_dir(self):
        return os.path.split(self.rel_log_path)[0]

    @property
    def abs_log_dir(self):
        return os.path.split(self.rel_log_path)[0]

    @property
    def actions(self):
        action_set = set()
        for action_result in self._results:
            if not action_result.action:
                return ""
            actions_str = action_result.action
            if ',' in actions_str:
                action = actions_str.split(',')
                action_set.update(action)
            else:
                action_set.add(actions_str)
        return action_set

    @property
    def status(self):
        for cmp_result in self._results:
            if cmp_result.status == 'failed' or cmp_result.status == 'not_run':
                return "failed"
        return "passed"


class PingBackAction(object):
    def __init__(self):
        self._passed_times = -1
        self._failed_times = -1
        self.parent = None
        self.http_msg_list = []
        self.conf_msg = None
        # self.cmp_params = []    # 元素为参数字典：{'expect', 'actual', 'result'}
        self.cmp_result = []    #  {'paramaters': {}, 'result_status': "passed", "failed_params": ""}
        self.match_index = -1
        # self.status = 'not_run'
        self.is_run = False
        self.need_cmp_order = False
        self.is_order = True
        self.rel_log_path = ""
        self.abs_log_path = ""

    def add_params(self, expect, actual, result):
        self.cmp_params.append({'expect': expect, 'actual': actual, 'result': result})

    def add_log_path(self):
        if not self.parent.rel_log_path:
            self.parent.add_log_path()

        params_index = self.index

        rel_log_dir = ""
        abs_log_dir = os.path.split(self.parent.abs_log_path)[0]
        if not os.path.exists(abs_log_dir):
            os.makedirs(abs_log_dir)

        self.rel_log_path = "params_{}.html".format(params_index)
        self.abs_log_path = os.path.join(abs_log_dir, "params_{}.html".format(params_index))

    @property
    def abs_log_dir(self):
        return os.path.split(self.abs_log_path)[0]

    @property
    def rel_log_dir(self):
        return os.path.split(self.rel_log_path)[0]

    @property
    def index(self):
        return self.parent.results.index(self)

    @property
    def action(self):
        return ','.join([value for value in self.conf_msg['action']]) if self.conf_msg else None

    @property
    def desc(self):
        return self.conf_msg['desc'] if self.conf_msg else None

    @property
    def status(self):
        self._passed_times = 0
        self._failed_times = 0
        for cmp_result in self.cmp_result:
            if cmp_result['result_status'] == 'failed':
                self._failed_times += 1
            elif cmp_result['result_status'] == 'passed':
                self._passed_times += 1
        if not self.is_order:
            return "failed"
        if self._failed_times == 0 and self._passed_times == 0:
            return 'not_run'
        else:
            return "passed" if self._passed_times > 0 else "failed"

    @property
    def passed_times(self):
        if self._passed_times == -1:
            self.status
        return self._passed_times

    @property
    def failed_times(self):
        if self._failed_times == -1:
            self.status
        return self._failed_times




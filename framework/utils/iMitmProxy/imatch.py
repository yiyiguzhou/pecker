# -*- coding: UTF-8 -*-

"""
File Name:      imatch
Author:         zhangwei04
Create Date:    2018/7/23
"""
from framework.utils.iMitmProxy.confparse import ConfParse
from framework.utils.iMitmProxy.ifilter import get_status_code, format_http_msg, IFilter
from framework.utils.iMitmProxy.report.html_report.report_html import ReportHtml
from framework.utils.iMitmProxy.excel.deal_excel import PingBackExcel2Xml
from framework.utils.iMitmProxy.result import *
from project.conf.pingback.configure import g_conf


class IMatch(object):
    def __init__(self, http_log_path=None, filter_key='GET https://msg'):
        self.conf_data = None
        self._http_msg_list =None
        self._filter_key = filter_key
        self._conf_msg_list = []    # 配置信息list
        self.result = PingBackTestCase()
        self._filter = None
        self._http_log_path = http_log_path

    def _load_conf_data(self, conf_path):
        if conf_path.endswith('.xlsx'):
            xml_path = "{}{}".format(os.path.splitext(conf_path)[0], ".xml")
            pbex = PingBackExcel2Xml(conf_path, xml_path=xml_path)
            pbex.read_excel()
            pbex.write_xml()
            conf_path = xml_path
        self.conf_data = ConfParse(conf_path)

    def _get_http_msg(self):
        if not self._filter:
            return
        http_format_list = []
        for http_line, status_code in self._filter.open():
            format_data = format_http_msg(http_line)
            if format_data:
                format_data['status_code'] = get_status_code(status_code)
                http_format_list.append(format_data)

        return http_format_list

    def to_file_end(self):
        if not self._filter:
            self._filter = IFilter(self._http_log_path, filter_key=self._filter_key, next_line=True)
        self._get_http_msg()

    def report(self, data_list=None):
        # rept = ReportHtml()
        # if self._http_msg_list:
        #     rept.report_pingback(self._http_msg_list)
        rept = ReportHtml()
        if not data_list:
            rept.report_pingback(self.conf_data.data['pingback'], self.__collect_actions(self.conf_data.data['pingback']))

    def ipecker_report(self):
        rept = ReportHtml()
        if self.result:
            rept.report_ipecker_pingback(self.result)

    def match_data(self, conf_path, http_log_path):
        # 一条用例执行结束后，http日志文件进行切换，需要重新打开文件
        if not self._filter or self._http_log_path != http_log_path:
            self._filter = IFilter(http_log_path, filter_key=self._filter_key, next_line=True)
            self._http_log_path = http_log_path     # http路径变更

        self._load_conf_data(conf_path)
        http_msg_list = self._get_http_msg()
        for i, conf_msg in enumerate(self.conf_data.data['pingback']):
            global_dict = self.conf_data.data['global'] if 'global' in self.conf_data.data else {}
            cmp_result_http_list, failed_times, success_times = self._cmp_action_paramater(conf_msg, http_msg_list, global_dict=global_dict)
            if failed_times > 0:
                result_status = 'failed'
            elif success_times == 0:
                result_status = 'not_run'
            else:
                result_status = 'passed'
            if conf_msg['desc']:
                conf_msg['report_path'] = os.path.join("action_report", "{}_{}.html".format(conf_msg['desc'], i))
            else:
                conf_msg['report_path'] = os.path.join("action_report", "{}.html".format(i))
            conf_msg['action_num'] = i
            conf_msg['cmp_result'] = {'http_list': cmp_result_http_list, "failed_times": failed_times, 'success_times': success_times, "result_status": result_status}

        return self.conf_data

    def order_match_data(self, conf_path, http_log_path, index_list: list, no_order_list, desc=""):
        """
        按照顺序匹配，即依次匹配
        Args:
            conf_path: 行为配置文件路径
            http_log_path: 存放捕获到的http行为文件路径
            index_list: 行为配置文件需要匹配的序号列表， 元素为int类型
            no_order_list: 不进行顺序比较的行为，相对index_list里面的位置
        Return:
            比较结果list
        """
        if not self.conf_data:
            self._load_conf_data(conf_path)

        # 一条用例执行结束后，http日志文件进行切换，需要重新打开文件
        if not self._filter or self._http_log_path != http_log_path:
            self._filter = IFilter(http_log_path, filter_key=self._filter_key, next_line=True)
            self._http_log_path = http_log_path  # http路径变更

        step_result = PingBackTestCaseStep(desc)
        step_result.parent = self.result

        http_msg_list = self._get_http_msg()
        self._conf_msg_list = conf_msg_list = [self.conf_data.data['pingback'][index - 1] for index in index_list]    # 获取配置action的list

        cmp_result_list = []
        if no_order_list:   # 部分顺序比较
            try:
                no_order_list[:] = [index_list.index(index) for index in no_order_list]     # 转化为index_list路径
            except Exception as e:
                raise(e)

            self.__part_order(conf_msg_list, http_msg_list, no_order_list, step_result)
        else:
            self.__complete_order(conf_msg_list, http_msg_list, step_result)

        self.result.add_result(step_result)

        return step_result.status

    def __part_order(self, conf_msg_list, http_msg_list, no_order_list, step_result):
        # 部分顺序比较，若投递数据出错，则位置定位在最后一行
        for i, conf_msg in enumerate(conf_msg_list):
            action_result = PingBackAction()
            action_result.parent = step_result
            action_result.conf_msg = conf_msg

            for j, http_msg in enumerate(http_msg_list):
                cmp_result = self._ensure_and_cmp_paramater(conf_msg, http_msg, global_dict={})

                if cmp_result['paramaters']:    # 满足比较条件，进行了比较
                    action_result.cmp_result.append(cmp_result)
                    action_result.is_run = True
                    if cmp_result['result_status'] == 'passed' and action_result.match_index == -1:
                        action_result.match_index = j + 1    # 记录匹配正确的位置

                    action_result.http_msg_list.append(http_msg)
                    action_result.need_cmp_order = True if j not in no_order_list else False

            step_result.add_result(action_result)

        self.__check_order(step_result)     # 查看顺序是否一致
        return step_result

    def __check_order(self, step_result):
        order_list = [params_result for params_result in step_result.results if params_result.need_cmp_order]
        if len(order_list) == 1:
            return
        for i in range(len(order_list) - 1):
            if not order_list[i].match_index < order_list[i + 1].match_index:
                order_list[i].is_order = False  # 序列不正确

    def __complete_order(self, conf_msg_list, http_msg_list, step_result):
        # 完全顺序比较
        for i, conf_msg in enumerate(conf_msg_list):
            cmp_result_dict = {"result_status": 'failed'}
            action_result = PingBackAction()
            action_result.conf_msg = conf_msg
            global_dict = self.conf_data.data['global'] if 'global' in self.conf_data.data else {}
            if i < len(http_msg_list):
                cmp_result = self._cmp_paramter(conf_msg, http_msg_list[i], global_dict=global_dict)
                action_result.cmp_result.append(cmp_result)
                action_result.is_run = True
                action_result.status = cmp_result['cmp_result']['result_status']
            else:
                action_result.is_run = False

            action_result.http_msg_list.append(http_msg_list[i])
            step_result.add_result(cmp_result_dict)

        return step_result

    def _cmp_action_paramater(self, action_msg, http_msg_list, global_dict):
        cmp_result_http_list = []
        failed_times = 0    # 失败投递个数
        success_times = 0  # 成功投递个数
        for http_msg in http_msg_list:
            cmp_result = self._ensure_and_cmp_paramater(http_msg, action_msg, global_dict)
            if cmp_result['paramaters']:
                cmp_result_http_list.append({"http_msg": http_msg, "cmp_result": cmp_result})
                if cmp_result['result_status'] == "failed":
                    failed_times += 1
                else:
                    success_times += 1

        return cmp_result_http_list, failed_times, success_times

    def _ensure_and_cmp_paramater(self, action_msg, http_msg, global_dict=None):
        # cmp_status = True
        # 通过确认参数确认要比较的http请求
        cmp_result = {'paramaters': {}, 'result_status': "passed", "failed_params": ""}
        if 'filter' in action_msg:
            filter_conf_msg = {}
            if action_msg['filter']:
                filter_conf_msg.update(action_msg['filter'])
            if action_msg['action']:
                filter_conf_msg.update(action_msg['action'])
            for ensure_param in filter_conf_msg:
                if ensure_param not in http_msg['params']:
                    print(ensure_param, [k for k in http_msg['params']])
                    break
                self.transferred_char(http_msg['params'], ensure_param)
                if filter_conf_msg[ensure_param] not in ("*", http_msg['params'][ensure_param]):
                    break
            else:   # ensure所有参数匹配
                # 比较参数
                cmp_result = self._cmp_paramter(http_msg, action_msg, global_dict)
        return cmp_result

    def _cmp_paramter(self,  http_msg, action_msg, global_dict=None):
        # 添加结果
        cmp_result = {'paramaters': {}, 'result_status': "passed", "failed_params": ""}
        failed_params = []
        # 比较参数
        param_conf_msg = {}
        if isinstance(global_dict, dict):
            param_conf_msg.update(global_dict)
        if 'common' in action_msg and isinstance(action_msg['common'], dict):
            param_conf_msg.update(action_msg['common'])
        param_conf_msg.update(action_msg['filter'])
        if isinstance(action_msg['expect'], dict):
            param_conf_msg.update(action_msg['expect'])

        paramater_set = set(param_conf_msg).union(set(http_msg['params']))
        # print(paramater_set)
        for param_key in paramater_set:
            cmp_result["paramaters"][param_key] = {'result': 'passed'}

            if param_key not in param_conf_msg:
                self.transferred_char(http_msg['params'], param_key)
                if action_msg.get('is_all_cmp', "no") == "yes":
                    cmp_result["paramaters"][param_key].update({"except": "-",
                                                                "actual": http_msg['params'][param_key],
                                                                "result": "failed"})
                    failed_params.append(param_key)
                    cmp_result['result_status'] = 'failed'
                else:
                    cmp_result["paramaters"][param_key].update({"except": "-",
                                                                "actual": http_msg['params'][param_key],
                                                                "result": "not_run"})
                continue
            elif param_key not in http_msg['params']:
                cmp_result["paramaters"][param_key].update({"except": param_conf_msg[param_key],
                                                            "actual": "-",
                                                            "result": "failed"})
                failed_params.append(param_key)
                cmp_result['result_status'] = 'failed'
                continue
            else:
                self.transferred_char(http_msg['params'], param_key)
                conf_param_value = param_conf_msg[param_key]

                # 任意值匹配
                if "*" == conf_param_value:
                    cmp_result["paramaters"][param_key].update({"except": param_conf_msg[param_key],
                                                                "actual": http_msg['params'][param_key]})
                    continue

                # 任意非空值匹配：
                if "?" == conf_param_value:
                    cmp_result["paramaters"][param_key].update({"except": param_conf_msg[param_key], "actual": http_msg['params'][param_key]})
                    if not http_msg['params'][param_key]:
                        cmp_result["paramaters"][param_key]['result'] = 'failed'
                        failed_params.append(param_key)
                        cmp_result['result_status'] = 'failed'
                    continue

                # 多值匹配
                if "," in conf_param_value:
                    conf_param_value = [value.strip() for value in conf_param_value.split(',')]
                else:
                    conf_param_value = [conf_param_value.strip()]

                # 正则匹配
                pass
                # 参数值比较
                if http_msg['params'][param_key] not in conf_param_value:
                    cmp_result['result_status'] = 'failed'
                    cmp_result["paramaters"][param_key]['result'] = 'failed'
                    cmp_status = False
                    failed_params.append(param_key)
                cmp_result["paramaters"][param_key].update({"except": param_conf_msg[param_key],
                                                            "actual": http_msg['params'][param_key]})

        cmp_result['failed_params'] = ", ".join(sorted(failed_params))
        return cmp_result

    def __collect_actions(self, pingback_list):
        action_set = set()
        for pingbac_dat_dict in pingback_list:
            filter_dict = pingbac_dat_dict.get('filter', None)
            if filter_dict:
                action_str = filter_dict.get('action', None)
                if action_str:
                    if ',' in action_str:
                        action_set.update(set(action_str.split(',')))
                    else:
                        action_set.add(action_str)

        return sorted(list(action_set))

    def reset_result(self):
        self.result = PingBackTestCase()

    @staticmethod
    def transferred_char(parma_dict, param):
        if "%3A" in parma_dict[param]:
            parma_dict[param] = parma_dict[param].replace("%3A", ":")


if __name__ == "__main__":
    http_log_path = "mitmproxy.txt"
    g_conf.get('pingback', 'http_pattern')
    ima = IMatch()
    # for http_msg in ima.match_data("pingBack.xml", "mitmproxy1.txt"):
    #     print(http_msg["cmp_result"])
    #     print(http_msg['result_status'])
    for conf_msg in ima.match_data("ios游戏中心数据投递用例-v2.7.5.xlsx", "mitmproxy.txt").data['pingback']:
        print(conf_msg['cmp_result'])
    ima.report()

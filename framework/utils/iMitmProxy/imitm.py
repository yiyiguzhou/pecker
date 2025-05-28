# -*- coding: UTF-8 -*-

"""
File Name:      imitm
Author:         zhangwei04
Create Date:    2018/7/20
"""
import os

from project.conf.pingback.configure import g_conf
from framework.utils.iMitmProxy.ithded import IpeckerThread
from framework.utils.iMitmProxy.imatch import IMatch
from framework.core.resource import g_resource, const
from framework.logger.logger import g_framework_logger, g_logger
from framework.exception.exception import PingbackException
# from framework.utils.iMitmProxy.report.html_report.report_html import report_dir
import shlex
from framework.utils.sys_shell import kill_process

class IMitm(object):
    def __init__(self):
        self._proc = None
        self._imatch = IMatch(self._get_http_log_path(), g_conf.get('pingback', 'http_pattern'))
        self._reuslt_list = []

    def start(self):
        try:
            if not self._imatch:
                self._imatch = IMatch(self._get_http_log_path(), g_conf.get('pingback', 'http_pattern'))

            catch_script = os.path.abspath(os.path.join(os.path.dirname(__file__), 'catchs.py')).replace('\\', '/')
            port = g_conf.get('proxy', 'port')
            args = shlex.split("mitmdump -s '{}' -p {} --ssl-insecure".format(catch_script, port))
            g_framework_logger.info(args)
            kill_process(pname="mitmdump.exe" if g_resource['system'] == const.SYSTEM_WINDOWS else "mitmdump")  # 启动前杀掉进程
            self._proc = IpeckerThread("mitmdump -s '{}' -p {} --ssl-insecure".format(catch_script, port), log_file=self._get_http_log_path(), time_interval=1)
            self._proc.start()
        except Exception as e:
            g_framework_logger.error(str(e))
            raise e

    def stop(self):
        if self._proc:
            self._proc.stop()
            self._proc = None
        kill_process(pname="mitmdump.exe" if g_resource['system'] == const.SYSTEM_WINDOWS else "mitmdump")

    def match(self, index_list=None, no_order_list=None, desc=""):

        conf_file_path = os.path.join(g_resource['project_path'], "conf", "pingback", g_conf.get('pingback', 'testcase_file'))
        if index_list:
            return self._imatch.order_match_data(conf_file_path, self._get_http_log_path(), index_list, no_order_list, desc=desc)
        else:
            # return self._imatch.match_data(conf_file_path,  self._get_http_log_path(), self._log_path)
            raise PingbackException("index_list is None")

    def to_file_end(self):
        if self._imatch:
            self._imatch.to_file_end()

    def add_cmp_result(self, desc, result_list):
        """添加用例描述"""
        self._reuslt_list.append({"desc": desc, "result_list": result_list})

    def report(self):
        """生成用例单次pingback报告"""
        g_logger.info("start generating pingback report")
        self._imatch.ipecker_report()
        g_logger.info("end generating pingback report")
        self._imatch.reset_result()  # 用例结束后，需要重置结果类

    def _get_http_log_path(self):
        if g_resource['testcase_loop'] != 0:
            catch_file_name = "mitmproxy_loop{}.txt".format(g_resource['testcase_loop'])
        else:
            catch_file_name = "mitmproxy.txt"

        return os.path.join(g_resource['testcase_log_dir'], catch_file_name)


if __name__ == "__main__":
    imitm = IMitm()
    imitm.start()

# -*- coding: UTF-8 -*-

"""
File Name:      dispatch
Author:         zhangwei04
Create Date:    2018/1/9
"""

import time
from framework.core.resource import g_resource
from framework.core.project_xml_parse import project_xml_parser
from framework.core.device_aml_parse import device_aml_parser
from framework.core.runner import Runner, g_signal
from framework.logger.logger import g_framework_logger
from framework.report.report import ReportXml
from framework.report.email_report import EmailReport
from framework.report.html_report.report_html import ReportHtml
from framework.devices.target_manager import TargetManager
from framework.utils.sys_shell import get_dev_list
from framework.utils.iftp.ftp import IpeckerFtp

# from framework.ui.signal.Signal import g_signal


class Dispatch(object):
    """工程调度类
    Attributes:
        start: 执行调度流程
    """
    def __init__(self):
        self.target_manager = None
        self._use_ui = False

        g_signal.use_ui[bool].connect(self._recv_use_ui)
        g_signal.is_use_ui.emit()

    def start(self):
        """调度开始接口，实现整个框架流程的调度，包含环境初始化工作、调用用例执行流程、环境收尾工作
        """
        try:
            if self._use_ui:
                g_signal.adapter_project_start.emit()
            g_framework_logger.info("starting ipecker...")
            # 解析配置文件
            project_xml_parser()
            device_aml_parser()

            # 加载设备
            self.__init_envir()
            try:
                # 执行流程
                run = Runner(self)
                run.start()

                # 环境信息放置结果类中
                run.result.environment = g_resource['aml_data'].get("environment", None)
            except Exception as e:
                g_framework_logger.error(str(e))

            # 生成 xml报告
            # try:
            #     xml_report = ReportXml()
            #     xml_report.report(run.result)
            # except Exception as e:
            #     g_framework_logger.error(str(e))

            # 生成html报告
            try:
                html_report = ReportHtml()
                html_report.report(run.result)
            except Exception as e:
                g_framework_logger.error(str(e))

            # 上传报告至ftp服务器
            self.__report_to_ftp(run.result)

        except Exception as e:
            g_framework_logger.error(str(e))
            raise e
        finally:
            # 释放资源
            self.__release_envir()

            g_resource['end_time'] = time.time()
            g_framework_logger.info("end ipecker")
            if self._use_ui:
                g_signal.adapter_project_end.emit()

    def __report_to_ftp(self, result):
        """上传报告至服务器
        Args:
            result: 测试结果类
        """
        parmeter = g_resource["aml_data"]['parameter']
        if parmeter.get("report_up_http", "false").lower() == "true":
            host = parmeter.get("server_localhost", "")
            base_path = parmeter.get("ftp_base_path", "")
            user = parmeter.get("ftp_user", "")
            passwd = parmeter.get("ftp_passwd", "")
            ftp = IpeckerFtp(host=host, base_path=base_path, user=user, passwd=passwd)
            ftp.login()
            ftp.upload_dir(g_resource['log_path'])

            # 发送邮件
            email = EmailReport(result)
            email.send_html_report()

    def __init_envir(self):
        """初始化环境接口"""
        self.__candidate_device()
        self.__load_target()

    def __candidate_device(self):
        """识别设备接口，用于标识实际连接设备"""
        g_resource['device_list'] = get_dev_list()
        device_data = g_resource['aml_data'].get('device')
        for target_name in device_data:
            device_id = device_data[target_name].get('id')
            for device_info in g_resource['device_list']:
                if device_info.get('id') == device_id:
                    device_info['status'] = 'candidate'

    def __load_target(self):
        """加载target"""
        self.target_manager = TargetManager(g_resource['aml_data'].get('device'))
        self.target_manager.load_target()

    def __release_envir(self):
        """环境收尾工作接口"""
        if self.target_manager:
            self.target_manager.remove_target()

    def _recv_use_ui(self, use_ui):
        self._use_ui = use_ui

# -*- coding: UTF-8 -*-

"""
File Name:      Adapter
Author:         zhangwei04
Create Date:    2018/10/24
"""
import os
import sys
from PyQt5.QtCore import pyqtSlot

from framework.ui.signal.Signal import g_signal
from framework.core.resource import g_resource
from framework.exception.exception import FileNotFound, ParamaterError, ParameterTypeError
from framework.core.dispatch import Dispatch
from framework.ui.iThreads import iPeckerThread


class Adapter:
    """适配器，用于充当框架和UI信号传递桥梁"""
    def __init__(self):
        self.dispatch = Dispatch()
        sys.path.insert(0, os.path.abspath(g_resource["project_path"]))
        self.xml_file = None
        self.aml_file = None
        self.current_testcase = None
        self.current_testsuit = None

        self._register_signal()

    def _register_signal(self):
        """注册信号"""
        g_signal.start_ipecker.connect(self.start_ipecker)
        g_signal.send_xml_file.connect(self.recv_xml_file)
        g_signal.send_aml_file[str].connect(self.recv_aml_file)

        g_signal.adapter_project_start.connect(self.project_start)
        g_signal.adapter_project_end.connect(self.project_end)
        g_signal.adapter_testsuite_start[str].connect(self.testsuite_start)
        g_signal.adapter_testsuite_end[str, str].connect(self.testsuite_end)
        g_signal.adapter_testcase_start[str].connect(self.testcase_start)
        g_signal.adapter_testcase_end[str, str].connect(self.testcase_end)

    def start_ipecker(self):
        """启动ipecker"""
        ipecker_thread = iPeckerThread(self.dispatch)
        self._parse_args()
        ipecker_thread.start()
        print("ipecker thread is start")

    def _parse_args(self):
        """xml和aml参数解析"""
        xml_file = self.get_xml_file()
        aml_file = self.get_aml_file()

        args_data = g_resource['input_args']
        args_data["order"] = None
        args_data["loop"] = None
        # check file if exists
        project_file_path = os.path.join(g_resource['project_path'], 'project')
        args_data['xml'] = os.path.join(project_file_path, xml_file)
        args_data['aml'] = os.path.join(project_file_path, aml_file)
        if not os.path.exists(args_data['xml']):
            raise FileNotFound('project xml file not found')
        if not os.path.exists(args_data['aml']):
            raise FileNotFound('device aml file not found')

    def recv_xml_file(self, xml_file):
        """接受xml文件"""
        self.xml_file = xml_file

    def get_xml_file(self):
        """获取xml文件"""
        return self.xml_file if self.xml_file else ""

    def recv_aml_file(self, aml_file):
        """接受aml文件"""
        self.aml_file = aml_file

    def get_aml_file(self):
        """获取aml文件"""
        return self.aml_file if self.aml_file else ""

    def project_start(self):
        """执行ipecker确认信号"""
        g_signal.project_start.emit()

    def project_end(self):
        """执行ipecker结束确认信号"""
        g_signal.project_end.emit()

    def testsuite_start(self, testsuite_name):
        """接收框架开始用例集信号，并转发出去"""
        self.current_testsuit = testsuite_name
        g_signal.testsuite_start.emit(testsuite_name)

    def testsuite_end(self, testsuite_name, status):
        """接收框架结束用例集信号，并转发出去"""
        self.current_testsuit = None
        g_signal.testsuite_end.emit(testsuite_name, status)

    def testcase_start(self, testcase_path):
        """接收框架开始单条用例信号，并转发出去"""
        self.current_testcase = testcase_path
        g_signal.testcase_start.emit(testcase_path)

    def testcase_end(self, testcase_path, status):
        """接收框架接受单条用例信号，并转发出去"""
        self.current_testcase = None
        g_signal.testcase_end.emit(testcase_path, status)

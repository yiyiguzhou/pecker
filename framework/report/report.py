# -*- coding: UTF-8 -*-

"""
File Name:      report
Author:         zhangwei04
Create Date:    2018/1/3
"""
import os
from ..report import result
from xml.dom.minidom import Document
from framework.core.resource import g_resource


class ReportXml(object):
    """xml报告类，根据框架执行的结果生成对应xml格式的报告"""
    def __init__(self):
        self.rpt = Document()

    def report(self, project_result):
        """
        报告生成函数，遍历结果类，生成对应接口的xml报告
        """
        rpt = self.rpt
        root = rpt.createElement(project_result.name)
        rpt.appendChild(root)
        # root.setAttribute('loop', g_project_result.loop_times)
        # 插入工程循环次数
        self.insert_child_text(root, 'loop', project_result.loop_times)
        # 插入状态：pass,failed
        self.insert_child_text(root, 'status', project_result.status)
        # 插入成功次数
        self.insert_child_text(root, 'passed_times', project_result.passed_times)
        # 插入开始时间
        self.insert_child_text(root, 'start_times', project_result.start_time)
        # 插入运行时间
        self.insert_child_text(root, 'run_time', project_result.run_time)

        # 插入循环报告
        for loop_result_tupple in project_result.results:
            loop_result = loop_result_tupple[1]
            loop_rst_node = self.insert_child(root, loop_result.name)
            # 插入状态：pass,failed
            self.insert_child_text(loop_rst_node, 'status', loop_result.status)
            # 插入开始时间
            self.insert_child_text(loop_rst_node, 'start_time', loop_result.start_time)
            # 插入运行时间
            self.insert_child_text(loop_rst_node, 'run_time', loop_result.run_time)

            # 插入用例集报告
            for testsuite_result in loop_result.results:
                testsuite_rst_node = self.insert_child(loop_rst_node, 'TestSuite')
                testsuite_rst_node.setAttribute("name", testsuite_result.name)
                # 插入状态
                self.insert_child_text(testsuite_rst_node, 'status', testsuite_result.status)
                # 插入开始时间
                self.insert_child_text(testsuite_rst_node, 'start_time', loop_result.start_time)
                # 插入运行时间
                self.insert_child_text(testsuite_rst_node, 'run_time', loop_result.run_time)

                passed_num = len(testsuite_result.passed_testcase)
                if passed_num > 0:
                    self.insert_child_text(testsuite_rst_node, 'passed', passed_num)

                if testsuite_result.message:
                    self.insert_child_text(testsuite_rst_node, 'message', "".join(testsuite_result.message))

                failed_num = len(testsuite_result.failed_testcase)
                if failed_num > 0:
                    self.insert_child_text(testsuite_rst_node, 'failed', failed_num)
                for testcase_result in testsuite_result.results:
                    testcase_rst_node = self.insert_child(testsuite_rst_node, testcase_result.name)
                    self.insert_child_text(testcase_rst_node, "status", testcase_result.status)
                    self.insert_child_text(testcase_rst_node, "start_time", testcase_result.start_time)
                    self.insert_child_text(testcase_rst_node, "run_time", testcase_result.run_time)
                    self.insert_child_text(testcase_rst_node, "loop", testcase_result.loop_times)
                    self.insert_child_text(testcase_rst_node, "passed_times", testcase_result.passed_times)
                    self.insert_child_text(testcase_rst_node, "failed_times", testcase_result.failed_times)
                    # 插入失败信息
                    for loop_times, msg_list in testcase_result.message.items():
                        message = "times:{}  {}".format(loop_times, "".join(msg_list))
                        self.insert_child_text(testcase_rst_node, "message", "{}".format(message))
        with open(os.path.join(g_resource['log_path'], 'report.xml'), 'w') as fp:
            rpt.writexml(fp, indent='\t', newl='\n', addindent='\t', encoding='utf-8')

    def insert_child_text(self, des_node, child_node_name, child_node_text):
        if not isinstance(child_node_text, str):
            child_node_text = str(child_node_text)
        node_text = self.rpt.createTextNode(child_node_text)
        child_node = self.insert_child(des_node, child_node_name)
        child_node.appendChild(node_text)
        return des_node

    def insert_child(self, des_node, child_node_name):
        child_node = self.rpt.createElement(child_node_name)
        des_node.appendChild(child_node)
        return child_node

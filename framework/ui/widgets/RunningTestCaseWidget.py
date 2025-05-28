# -*- coding: UTF-8 -*-

"""
File Name:      RunningTestCase
Author:         zhangwei04
Create Date:    2018/10/16
"""
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QMouseEvent
from framework.ui.signal.Signal import g_signal


class RunningTestCaseWidget(QTableWidget):
    """用例状态栏-执行用例表组件"""
    status_dict = {"passed": "成功", "failed": "失败", "error": "错误", "block": "中断", "running": "执行中"}

    def __init__(self):
        super().__init__()
        self.xml_file = None
        self.aml_file = None
        self.testcase_list = []
        self.testcase_status_list = []

        g_signal.testcase_tree_selected[list].connect(self.recv_testcase_list)
        g_signal.xml_selected[list].connect(self.recv_xml_list)
        g_signal.aml_selected[list].connect(self.recv_aml_list)
        g_signal.update_testcase_running_table.connect(self.update_queue)
        g_signal.get_testcase_from_running.connect(self.recv_enquire_testcase_list)

        g_signal.testsuite_start[str].connect(self.recv_testsuite_start)
        g_signal.testcase_end[str, str].connect(self.recv_testcase_end)
        g_signal.testcase_start[str].connect(self.recv_testcase_start)
        g_signal.testcase_end[str, str].connect(self.recv_testcase_end)

        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置为只读属性
        self.setColumnCount(2)
        self.setHorizontalHeaderItem(0, QTableWidgetItem("用例名"))
        self.setHorizontalHeaderItem(1, QTableWidgetItem("执行状态"))

    def update_queue(self):
        """更新队列，主要用于获取都选后的用例或者xml文件后，同步到此队列中"""
        g_signal.get_select_testcase.emit()
        try:
            g_signal.get_select_aml.emit()
        except Exception as e:
            print(e)
        if self.testcase_list:
            print("update_queue")
            print(self.testcase_list)
        else:
            g_signal.get_select_xml.emit()
            if self.xml_file:
                self.testcase_list = self.load_testcase_xml(self.xml_file)

        self._write_testcase_xml(self.testcase_list) # 写用例文件
        self.testcase_status_list[:] = ["未执行" for i in self.testcase_list]  # 添加队列初始化状态
        # Todo 待完善已存在情况
        self.view_select_testcase()  # 显示队列

    def load_testcase_xml(self, xml_file):
        """使用xml文件执行时，读取xml文件的用例
        Args:
            xml_file: 用例xml文件
        Returns:
            测试用例列表
        """
        from framework.core.resource import g_resource
        import xml.etree.ElementTree as ET

        xml_path = os.path.join(g_resource['project_path'], "project", xml_file)

        tree = ET.parse(xml_path)
        root = tree.getroot()
        testcase_info_list = []
        testcase_set = set()
        for child in root:
            if child.text:
                if child.text not in testcase_set:  # 去掉重复用例
                    testcase_set.add(child.text)
                    testcase_info_list.append(child.text)
        print(testcase_info_list)
        return testcase_info_list

    def recv_xml_list(self, xml_list):
        """接受传递xml文件列表函数，若勾选多个xml文件，则弹出提示
        Args:
            xml_list: xml文件列表
        Returns:
            若xml文件数量大于2个，返回空列表，非洲返回原xml文件列表
        """
        # 多选的xml待处理
        if len(xml_list) > 1:
            comment = "\n".join(xml_list)
            reply = QMessageBox.warning(self, "警告", "请选择一个工程文件，已选\n{}\n文件".format(comment), QMessageBox.Yes)
            return []

        self.xml_file = xml_list[0] if xml_list else None

    def recv_aml_list(self, aml_list):
        """接受传递aml文件列表函数，若勾选多个aml文件，则弹出提示"""
        # Todo 多选对话框弹出处理
        if len(aml_list) > 1:
            comment = "\n".join(aml_list)
            reply = QMessageBox.warning(self, "警告", "请选择一个设备配置文件，已选\n{}\n文件".format(comment), QMessageBox.Yes)
            return []
        self.aml_file = aml_list[0] if aml_list else None

    def recv_testcase_list(self, testcase_list):
        """接收测试用例列表函数，绑定测试用例信号"""
        self.testcase_list = testcase_list

    def view_select_testcase(self):
        """显示测试用例队列"""
        exist_row_count = self.rowCount()

        count = len(self.testcase_list)
        self.setRowCount(count)

        for row, (testcase, status) in enumerate(zip(self.testcase_list, self.testcase_status_list)):
            try:
                # 用例名列
                item = QTableWidgetItem()
                item.setText(str(testcase))
                item.setFlags(Qt.ItemIsEnabled)
                self.setItem(row, 0, item)
                # 执行状态列
                status_item = QTableWidgetItem()
                status_item.setText(status)
                status_item.setFlags(Qt.ItemIsEnabled)
                self.setItem(row, 1, status_item)
            except Exception as e:
                print(e)

    def _write_testcase_xml(self, testcase_list):
        """根据测试用例队列的内容写测试用例xml文件，用于ipecker框架执行
        Args:
            testcase_list: 测试用例列表
        """
        # 写测试用例文件
        from xml.dom.minidom import Document
        doc = Document()
        root = doc.createElement("project")
        root.setAttribute("sort", 'normal')
        root.setAttribute("loop", "1")
        doc.appendChild(root)

        for testcase in testcase_list:
            ele = doc.createElement("testcase")
            testcase = str(testcase).rstrip('\\/')
            testcase = testcase.rsplit('.', 1)[0] if testcase.endswith(".py") else testcase
            ele.appendChild(doc.createTextNode(testcase))
            root.appendChild(ele)

        from framework.core.resource import g_resource
        xml_path = os.path.join(g_resource['project_path'], 'project', "ipecker_tmp.xml")
        with open(xml_path, 'w', encoding='utf-8') as fp:
            doc.writexml(fp, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        g_signal.send_xml_file.emit("ipecker_tmp.xml")

    def recv_testsuite_start(self, testsute_name):
        """接收适配器发送的开始用例集信号函数"""
        self.run_testsuite = testsute_name

    def recv_testsuite_end(self, testsute_name, status):
        """接收适配器发送的结束用例集信号函数"""
        if self.run_testsuite != testsute_name:
            # 带添加抛出异常
            self.run_testsuite_status = status

    def recv_testcase_start(self, testcase_name):
        """接收适配器发送的开始用例信号函数"""
        if not testcase_name.endswith(".py"):
            testcase_name = "{}.py".format(testcase_name)
        self.run_testcase = testcase_name
        try:
            index = self.testcase_list.index(testcase_name)
            self.testcase_status_list[index] = "执行中"
            self.view_select_testcase()
        except Exception as e:
            print(e)
        self.update_status_bar()

    def recv_testcase_end(self, testcase_name, status):
        """接收适配器发送的结束用例信号函数"""
        if not testcase_name.endswith(".py"):
            testcase_name = "{}.py".format(testcase_name)
        try:
            index = self.testcase_list.index(testcase_name)
            self.testcase_status_list[index] = RunningTestCaseWidget.status_dict.get(status, "未知错误")
            self.view_select_testcase()
        except Exception as e:
            print(e)

        self.update_status_bar()

    def update_status_bar(self):
        """更新状态栏"""
        run_num = 0
        for status in self.testcase_status_list:
            if status in RunningTestCaseWidget.status_dict.values():
                run_num += 1
        g_signal.update_testcase_status_bar.emit(int(run_num / len(self.testcase_status_list) * 100))  # 发送信号

    def recv_enquire_testcase_list(self):
        import copy
        g_signal.send_testcase_from_running.emit(copy.deepcopy(self.testcase_list))



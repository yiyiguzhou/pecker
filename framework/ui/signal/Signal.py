# -*- coding: UTF-8 -*-

"""
File Name:      Signal
Author:         zhangwei04
Create Date:    2018/10/17
"""
from PyQt5.QtCore import QObject, pyqtSignal

__all__ = ["g_signal"]


class Signal(QObject):
    start_run = pyqtSignal()
    """用例模块信号"""
    testcase_add_queue = pyqtSignal(str)    # 用例树单用例添加至执行队列信号，参数：用例相对路径名
    testcase_tree_add_queue = pyqtSignal()   # 用例树全部更新至用例执行队列信号，若执行队列有，则添加至后面

    testcase_tree_reload = pyqtSignal()     # 用例树刷新
    get_select_testcase = pyqtSignal()  # 从用例树获取勾选的用例
    testcase_tree_selected = pyqtSignal(list)   # 用例树用例信号
    add_testcase = pyqtSignal(str)  # 用例树 添加用例文件 用例名

    """配置模块信号"""
    project_conf_get_select_testcase = pyqtSignal()     # 配置文件获取勾选的用例
    project_conf_return_testcase = pyqtSignal(list)     # 用例树返回信号
    get_select_xml = pyqtSignal()  # 获取勾选的xml文件
    xml_selected = pyqtSignal(list)  # 勾选过的xml文件列表
    get_select_aml = pyqtSignal()  # 获取勾选的aml文件
    aml_selected = pyqtSignal(list)  # 勾选过的aml文件列表

    send_aml_file = pyqtSignal(str)  # 发送aml文件

    """执行队列模块"""
    update_testcase_running_table = pyqtSignal()  # 更新用例执行队列
    send_xml_file = pyqtSignal(str)  # 发送xml文件
    get_testcase_from_running = pyqtSignal()
    send_testcase_from_running = pyqtSignal(list)

    """用例执行模块"""
    start_ipecker = pyqtSignal()  # 执行工程

    """适配器"""
    get_xml_file = pyqtSignal()  # 获取xml文件
    get_aml_file = pyqtSignal()  # 获取aml文件
    testcase_start = pyqtSignal(str)  # 测试用例开始信号， 参数测试用例名
    testcase_end = pyqtSignal(str, str)  # 测试用例执行结束，参数：测试用例名, 执行结果
    testsuite_start = pyqtSignal(str)  # 测试用例集开始信号， 参数测试用例集名
    testsuite_end = pyqtSignal(str, str)  # 测试用例级结束， 参数：测试用例集名, 执行结果
    project_start = pyqtSignal()  # 工程开始
    project_end = pyqtSignal()  # 工程结束

    """框架层"""
    adapter_testcase_start = pyqtSignal(str)  # 测试用例开始信号， 参数测试用例名
    adapter_testcase_end = pyqtSignal(str, str)  # 测试用例执行结束，参数：测试用例名, 执行结果
    adapter_testsuite_start = pyqtSignal(str)  # 测试用例集开始信号， 参数测试用例集名
    adapter_testsuite_end = pyqtSignal(str, str)  # 测试用例级结束， 参数：测试用例集名, 执行结果
    adapter_project_start = pyqtSignal()  # 工程开始
    adapter_project_end = pyqtSignal()  # 工程结束

    use_ui = pyqtSignal(bool)
    is_use_ui = pyqtSignal()
    ui_print = pyqtSignal(str)

    update_testcase_status_bar = pyqtSignal(int)  # 更新进度条


g_signal = Signal()

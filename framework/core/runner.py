# -*- coding: UTF-8 -*-

"""
File Name:      runner
Author:         zhangwei04
Create Date:    2017/12/25
"""

import copy
import os
import time
from framework.core.resource import g_resource
from operator import itemgetter
from framework.report.result import *
from framework.utils.func import introspect
from framework.logger.logger import g_logger, g_framework_logger
from framework.logger.logger import switch_log_path
from framework.exception.exception import AssertException
from framework.core.resource import MESSAGE
from framework.report import result
from framework.core.const import reslut_status
from framework.report.html_report.report_html import ReportHtml

# ui 信号
from framework.ui.signal.Signal import g_signal


class Runner(object):
    """用例执行类，用于用例的执行流程
    Attributes:
        start: 执行用例流程
    """

    def __init__(self, dispatch):
        self.__test_data = _classify_testcase(g_resource['xml_data'])
        self.result = result.ProjectResult("ipecker")
        self._use_ui = dispatch._use_ui

    def __run_test(self):
        """工程循环级执行流程
        """
        loop_times = self.__test_data.get("loop")
        self.result.start_time = time.time()
        self.result.log_dir = g_resource['log_path']
        self.result.loop_times = loop_times  # 工程循环次数
        for i in range(loop_times):
            project_loop_result = result.ProjectLoopResult("loop{}".format(i + 1))
            project_loop_result.start_time = time.time()
            project_log_dir = g_resource['log_path']
            if loop_times > 1:
                str_time = time.strftime("%m-%d_%H_%M_%S")
                project_log_dir = os.path.join(g_resource['log_path'], "loop{}_{}".format(i + 1, str_time))
                if not os.path.exists(project_log_dir):
                    os.makedirs(project_log_dir)

            self.__run_testsuite(project_log_dir, project_loop_result)
            project_loop_result.end_time = time.time()
            self.result.add_loop_result(project_loop_result)

        self.result.end_time = time.time()

    def __run_testsuite(self, project_log_dir, project_loop_result):
        """用例集执行流程
        Args:
            project_log_dir:工程循环时log目录
            project_loop_result: 工程循环结果类，用于用例集执行结果的回填
        """
        for testsuite_tupple in self.__test_data['testsuite']:
            # 创建testsuite目录
            testsuite_log_dir = os.path.join(project_log_dir, testsuite_tupple[0])
            g_resource['testsuite_log_dir'] = os.path.abspath(testsuite_log_dir)

            testsuite_name = testsuite_tupple[0].replace("/", ".")
            testsuite_result = result.TestSuiteResult(testsuite_name)
            testsuite_result.start_time = time.time()
            if self._use_ui:  # UI 用例集开始信号
                g_signal.adapter_testsuite_start.emit(testsuite_name)

            with switch_log_path(testsuite_log_dir, "testsuite_log.txt"):
                g_logger.critical("testsuite: {} start  ...".format(testsuite_name))
                first_testcase = testsuite_tupple[1][0][0].replace("\\", "/")  # 取第一个用例用作用例集初始化操作
                if not first_testcase.startswith(("script.", "script/")):
                    first_testcase = "script.{}".format(first_testcase)
                testsuite_class_path = os.path.join(g_resource['project_path'], 'script',
                                                    first_testcase.replace("/", "."))
                first_testcase_name = first_testcase.rsplit("/", 1)[1]
                testsuite = introspect(testsuite_class_path, first_testcase_name)()
                try:
                    testsuite.setup_testcase()
                except AssertException:
                    testsuite_result.add_message(copy.deepcopy(MESSAGE))
                    MESSAGE.clear()
                    self.__add_not_run_testcase(testsuite_result, testsuite_tupple[1])
                    testsuite_result.status = reslut_status.ERROR
                except Exception as e:
                    # 用例集初始化产生异常，用例没有执行，统计为error状态
                    self.__add_not_run_testcase(testsuite_result, testsuite_tupple[1])
                    testsuite_result.status = reslut_status.ERROR
                else:
                    try:
                        self.__run_testcase(testsuite_tupple, testsuite_log_dir, testsuite_result)
                    except AssertException:
                        testsuite_result.add_message(copy.deepcopy(MESSAGE))
                        MESSAGE.clear()
                    except Exception as e:
                        g_logger.warning(str(e))
                        g_framework_logger.exception(str(e))
                    finally:
                        try:
                            testsuite.teardown_testcase()
                        except AssertException:
                            testsuite_result.add_message(copy.deepcopy(MESSAGE))
                            MESSAGE.clear()
                        finally:
                            if MESSAGE:  # except_true等接口信息
                                testsuite_result.add_message(copy.deepcopy(MESSAGE))
                                MESSAGE.clear()
                            if self._use_ui:  # ui 用例集结束信号
                                g_signal.adapter_testsuite_end.emit(testsuite_name, testsuite_result.status)
                        g_logger.critical("testsuite: {} end".format(testsuite_name))

            testsuite_result.end_time = time.time()
            project_loop_result.add_testsuite_result(testsuite_result)

    def __run_testcase(self, testsuite_tupple, testsuite_log_dir, testsuite_result):
        """用例执行流程
        Args:
            testsuite_tupple:用例集数据元组(用例集名称，用例元组列表)
            testsuite_log_dir: 用例集log目录
            testsuite_result: 用例集结果类，用于用例执行结果的回填
        """
        current_time = 0  # 当前用例index
        for testcase_tupple in testsuite_tupple[1]:
            loop = testcase_tupple[1]
            testcase_moudle = testcase_tupple[0].replace("\\", "/")
            testcase_name = testcase_moudle.rsplit('/', 1)[1]
            testcase_log_dir = os.path.join(testsuite_log_dir, testcase_name)
            g_resource['testcase_log_dir'] = testcase_log_dir  # 添加到资源中

            testcase_module_path = "script.{}".format(testcase_moudle) if not testcase_moudle.startswith(
                ("script/", "script.")) else testcase_moudle
            testcase_module_path = os.path.join(g_resource['project_path'], 'script', testcase_module_path.replace("/", "."))

            testcase_result = result.TestCaseResult(testcase_name)
            testcase_result.start_time = time.time()
            testcase_result.loop_times = loop

            testcase_result.log_relative_dir = testcase_log_dir[len(g_resource['log_path']):].lstrip('\\/')  # 添加用例相对目录
            testcase_result.log_abs_dir = testcase_log_dir

            current_time += 1
            current_status = reslut_status.PASSED
            try:
                if self._use_ui:
                    g_signal.adapter_testcase_start.emit(testcase_moudle)
                testcase_obj = introspect(testcase_module_path, testcase_name)
                for i in range(loop):
                    current_status = reslut_status.PASSED
                    g_resource['testcase_loop'] = 0 if loop == 1 else i + 1
                    testcase_result.loop_start_time.append(time.time())

                    testcase_log_name = "{}_log.txt".format(
                        testcase_name if loop == 1 else "{}_loop{}".format(testcase_name, i + 1))

                    # global MESSAGE

                    with switch_log_path(testcase_log_dir, testcase_log_name):
                        testcase = testcase_obj()
                        if testcase_moudle.startswith('script'):
                            cls_path = os.path.join(g_resource['project_path'], '{}.xml'.format(testcase_moudle))
                        else:
                            cls_path = os.path.join(g_resource['project_path'], 'script',
                                                    '{}.xml'.format(testcase_moudle))
                        testcase.load_data(cls_path)

                        try:
                            g_logger.critical("start {} setup...".format(testcase_name))
                            testcase.setup()
                            g_logger.critical("end {} setup".format(testcase_name))
                            g_logger.critical("start {} test...".format(testcase_name))
                            testcase.test()
                        except AssertException:  # 其他异常需要抛出
                            pass
                        except Exception as e:
                            current_status = reslut_status.ERROR
                            raise e
                        finally:
                            g_logger.critical("end {} test".format(testcase_name))
                            g_logger.critical("start {} teardown...".format(testcase_name))
                            try:
                                testcase.teardown()
                            except AssertException:
                                pass
                            except Exception as e:
                                current_status = reslut_status.ERROR
                                raise e
                            finally:
                                if MESSAGE:
                                    if not current_status == reslut_status.ERROR:
                                        testcase_result.failed_times += 1
                                    testcase_result.add_message(copy.deepcopy(MESSAGE))
                                    MESSAGE.clear()
                                elif current_status == reslut_status.PASSED:
                                    testcase_result.passed_times += 1
                                testcase_result.loop_end_time.append(time.time())
                                g_logger.critical("end {} teardown".format(testcase_name))
            except Exception as e:
                g_framework_logger.exception(str(e))
                g_logger.exception(str(e))
                testcase_result.error_times += 1
                # 用例集初始化产生异常，用例没有执行，统计为error状态
                self.__add_not_run_testcase(testsuite_result, testsuite_tupple[1][current_time:])
                # 用例执行异常
                raise e
            finally:
                if self._use_ui:
                    g_signal.adapter_testcase_end.emit(testcase_moudle, testcase_result.status)
                testcase_result.end_time = time.time()
                testsuite_result.add_testcase_result(testcase_result)
                testcase_result.desc = testcase.desc  # 添加用例描述到用例结果类中
                report = ReportHtml()
                report.report_testcase(testcase_result, g_resource['targets'])

    def __add_not_run_testcase(self, testsuite_result, testcase_list, start_pos=0, end_pos=None):
        """
        添加未执行用例到用例集结果中
        Args:
            testsuite_result: 测试用例集结果集
            testcase_tupple: 测试用例元组
            start_pos: 开始位置
            end_pos: 结束位置
        """
        for testcase_tupple in testcase_list if end_pos else testcase_list[start_pos:end_pos]:
            testcase_moudle = testcase_tupple[0].replace("\\", "/").replace("/", ".")  # 获取用例名
            testsuite_name, testcase_name = testcase_moudle.rsplit(".", maxsplit=1)
            testcase_module_path = "script.{}".format(testcase_moudle) if not testcase_moudle.startswith(("script/", "script.")) else testcase_moudle
            testcase_module_path = os.path.join(g_resource['project_path'], 'script', testcase_module_path)
            testcase_obj = introspect(testcase_module_path, testcase_name)
            testcase_desc = testcase_obj().desc
            testsuite_result.block_testcase_list.append((testsuite_name, testcase_name, testcase_desc))

    def start(self):
        """用例执行流程入口"""
        self.__run_test()


def _classify_testcase(xml_data):
    """将从xml里面读取到的用例进行用例集划分，并设置执行模式（顺序，升序，随机）
    Args:
        xml_data: 读取到的xml数据
    Returns:

    """
    # 归类至用例集
    testsuite_list = []
    testsuite_set = []  # 用于记录用例集
    for testcase_data in xml_data['testcase']:
        # 用例集归类
        testcase = testcase_data[0].replace("\\", "/")
        testsuite = testcase.rsplit('/', 1)[0]
        if testsuite not in testsuite_set:
            testsuite_set.append(testsuite)
            testsuite_list.append((testsuite, [testcase_data]))
        else:
            index = testsuite_set.index(testsuite)
            testsuite_list[index][1].append(testcase_data)

    # 用例排序
    order = g_resource['input_args'].get('order', None)  # 参数配置执行模式优先级大于xml文件配置
    if not order:
        order = xml_data['order']
    if order == 'auto':
        testsuite_list = sorted(testsuite_list, key=itemgetter(0))  # 用例集排序
        for testsuite in testsuite_list:
            sorted_testcase = sorted(testsuite[1], key=itemgetter(0))
            testsuite[1].clear()
            testsuite[1][:] = sorted_testcase
    elif order == 'random':
        import random
        random.shuffle(testsuite_list)
        for testsuite in testsuite_list:
            random.shuffle(testsuite[1])
    else:  # 默认normal模式，不进行排序处理
        pass

    test_data = {}
    loop = g_resource['input_args']['loop']
    test_data['loop'] = int(loop if loop else xml_data['loop'])
    test_data['testsuite'] = testsuite_list

    return test_data

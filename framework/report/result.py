# -*- coding: UTF-8 -*-

"""
File Name:      result
Author:         zhangwei04
Create Date:    2017/12/27
"""
import os
import time
from framework.exception.exception import InstanceError
from framework.utils.func import format_time
from framework.exception.exception import AttributeNotSet
from framework.core.const import reslut_status


class BaseResult(object):
    """
    基本结果类，所有结果类的基类
    """
    def __init__(self, name):
        self._name = name
        self._results = []
        self._passed = True
        self._start_time = 0
        self.end_time = 0
        self.error = False
        self._status = reslut_status.BLOCK

    @property
    def results(self):
        """
        Returns:
            下一级结果类列表
        """
        return self._results

    @property
    def name(self):
        """
        Returns:
            当前结果类名字
        """
        return self._name

    @property
    def status(self):
        """
        Returns:
            当前结果类执行状态
        """
        return reslut_status.get_desc(self._status)

    @property
    def get_status(self):
        return self._status

    @property
    def status(self):
        """
        Returns:
            当前结果类执行状态
        """
        return reslut_status.get_desc(self._status)

    @status.setter
    def status(self, value):
        """
        Returns:
            设置结果类执行状态
        """
        if value in reslut_status.values:
            self._status = value

    @property
    def testcase_name_list(self):
        pass

    @property
    def testcase_count(self):
        return self.passed_testcase_count + self.failed_testcase_count + self.error_testcase_count + self.block_testcase_count

    @property
    def passed_testcase_count(self):
        return self._count_result(reslut_status.PASSED)

    @property
    def failed_testcase_count(self):
        return self._count_result(reslut_status.FAILED)

    @property
    def failed_testcase(self):
        pass

    @property
    def error_testcase_count(self):
        return self._count_result(reslut_status.ERROR)

    @property
    def block_testcase_count(self):
        return self._count_result(reslut_status.BLOCK)

    def _set_status(self, test_result):
        if self._status in (reslut_status.BLOCK, reslut_status.PASSED):
            self._status = test_result.get_status
        elif self._status == reslut_status.FAILED:
            if test_result.get_status == reslut_status.ERROR:
                self._status = reslut_status.ERROR

    def _count_result(self, status):
        _count = 0
        for result in self._results:
            if isinstance(result, tuple):
                result = result[1]
            if status == reslut_status.PASSED:
                _count += result.passed_testcase_count
            elif status == reslut_status.FAILED:
                _count += result.failed_testcase_count
            elif status == reslut_status.ERROR:
                _count += result.error_testcase_count
            else:
                _count += result.block_testcase_count

        return _count

    @property
    def passed(self):
        """
        Returns:
            当前结果类内所有用例是否都成功
        """
        return self._passed

    @property
    def run_time(self):
        """
        Returns:
            当前结果类执行时间
        """

        return format_time(self.end_time - self._start_time)

    @property
    def start_time(self):
        if self._start_time == 0:
            raise AttributeNotSet("start_time not be set")
        return time.ctime(self._start_time)

    @start_time.setter
    def start_time(self, value):
        self._start_time = value


class ProjectResult(BaseResult):
    """
    工程结果类
    """
    def __init__(self, name='ipecker'):
        super(ProjectResult, self).__init__(name)
        self.__passed_times = 0
        self.__failed_times = 0
        self.__error_times = 0
        self.loop_times = 0
        self.log_dir = None
        self.environment = None     # 环境配置

    def add_loop_result(self, loop_result):
        """
        添加工程循环执行结果类
        Args:
            loop_result: 循环结果类对象
        """
        result_tupple = (self.__passed_times + self.__failed_times + self.__error_times, loop_result)
        if not isinstance(loop_result, ProjectLoopResult):
            raise InstanceError("instance must be ProjectLoopResult class")

        if loop_result.get_status == reslut_status.FAILED:
            self.__failed_times += 1
        elif loop_result.get_status == reslut_status.PASSED:
            self.__passed_times += 1
        elif loop_result.get_status == reslut_status.ERROR:
            self.__error_times += 1

        self._set_status(loop_result)

        self._results.append(result_tupple)

    @property
    def run_times(self):
        """
        Returns:
            工程已经进行循环测试的次数
        """
        return self.__failed_times + self.__passed_times + self.__error_times

    @property
    def passed_times(self):
        """
        Returns:
            执行成功次数
        """
        return self.__passed_times

    @property
    def testcase_without_loop(self):
        pass

    @property
    def testcase_without_loop_count(self):
        return len(self.testcase_without_loop)

    @property
    def testcase_name_list(self):
        tmp_testcase_name_list = []
        for loop_result_tuple in self._results:
            tmp_testcase_name_list.extend(loop_result_tuple[1].testcase_name_list)
        return tmp_testcase_name_list

    @property
    def failed_testcase(self):
        """
        Returns:
            执行失败的用例用例列表，列表元素：工程循环失败用例类列表
        """
        failed_testcase_list = []
        for loop_result_tuple in self._results:
            for failed_testcase in  loop_result_tuple[1].failed_testcase:
                failed_testcase_list.append((loop_result_tuple[0], failed_testcase))
        return failed_testcase_list

    @property
    def passed_rate(self):
        status_list = self.testcase_count_without_loop
        total = sum(status_list)
        if total == 0:
            return "0%"
        return "{}%".format("%.2f" % (status_list[0] / total * 100))

    @property
    def testcase_count_without_loop(self):
        """获取整合循环后的不同用例状态数量
        Returns:
            返回包含：成功用例个数，失败用例个数，错误用例个数，阻塞用例个数，这四个元素的集合
        """
        testcase_dict = {
            reslut_status.PASSED: set(),
            reslut_status.FAILED: set(),
            reslut_status.ERROR: set(),
            reslut_status.BLOCK: set(),
        }

        for (testcase_name, status) in self.testcase_name_list:  # block用例没有testcase对象
            testcase_dict[status].add(testcase_name)
            if testcase_name in testcase_dict[reslut_status.ERROR]:
                testcase_dict[reslut_status.BLOCK].discard(testcase_name)
                testcase_dict[reslut_status.FAILED].discard(testcase_name)
                testcase_dict[reslut_status.PASSED].discard(testcase_name)
            elif testcase_name in testcase_dict[reslut_status.FAILED]:
                testcase_dict[reslut_status.BLOCK].discard(testcase_name)
                testcase_dict[reslut_status.PASSED].discard(testcase_name)
            elif testcase_name in testcase_dict[reslut_status.PASSED]:
                testcase_dict[reslut_status.BLOCK].discard(testcase_name)

        return [len(testcase_dict[reslut_status.PASSED]),
                len(testcase_dict[reslut_status.FAILED]),
                len(testcase_dict[reslut_status.ERROR]),
                len(testcase_dict[reslut_status.BLOCK])]


class ProjectLoopResult(BaseResult):
    """
    工程循环结果类
    """
    def __init__(self, name):
        super(ProjectLoopResult, self).__init__(name)

    def add_testsuite_result(self, testsuite_result):
        """
        添加用例集结果类
        Args:
            testsuite_result: 用例集结果类
        """
        if not isinstance(testsuite_result, TestSuiteResult):
            raise InstanceError("instance must be TestSuiteResult class")
        self._set_status(testsuite_result)

        self._results.append(testsuite_result)

    @property
    def passed_testsuite_results(self):
        """
        Returns:
            执行成功的用例集结果类
        """
        passed_testsuite_list = []
        for testsuite in self._results:
            if testsuite.passed:
                passed_testsuite_list.append(testsuite)
        return passed_testsuite_list

    @property
    def failed_testsuite_results(self):
        """
        Returns:
            执行失败的用例集结果类
        """
        failed_testsuite_list = []
        for testsuite in self._results:
            if not testsuite.__passed:
                failed_testsuite_list.append(testsuite)
        return failed_testsuite_list

    @property
    def testcase_name_list(self):
        testcase_list = []
        for testsuite in self._results:
            testcase_list.extend(testsuite.testcase_name_list)
        return testcase_list

    @property
    def failed_testcase(self):
        """
        Returns:
            执行失败的用例集结果类
        """
        failed_testcase_list = []
        for testsuite in self._results:
            failed_testcase_list.extend(testsuite.failed_testcase)
        return failed_testcase_list

    @property
    def block_testcase_name(self):
        """
        获取未运行用例
        Return:
            未执行用例列表
        """
        testcase_name_list = []
        for testsuite in self._results:
            for testcase_name in testsuite.block_testcase_list:
                testcase_name_list.append(testcase_name)

        return testcase_name_list


class TestSuiteResult(BaseResult):
    """
    用例集结果类
    """
    def __init__(self, name):
        super(TestSuiteResult, self).__init__(name)
        self.__message = None
        self.block_testcase_list = []   # 元素为元组，包含用例集名，用例名，用例描述

    @property
    def passed_testcase(self):
        """
        Returns:
            成功的用例结果类
        """
        passed_testcase_list = []
        for testcase in self._results:
            if testcase.get_status == reslut_status.PASSED:
                passed_testcase_list.append(testcase)
        return passed_testcase_list

    @property
    def testcase_name_list(self):
        tmp_testcase_name_list = []
        tmp_testcase_name_list.extend([(testcase_name, reslut_status.BLOCK) for testcase_name in self.block_testcase_list])
        for testcase in self._results:
            testcase_name = "{}.{}".format(self.name, testcase.name)
            status = testcase.get_status
            tmp_testcase_name_list.append((testcase_name, status))
        return tmp_testcase_name_list

    @property
    def failed_testcase(self):
        """
        Returns:
            失败的用例结果类
        """
        failed_testcase_list = []
        for testcase in self._results:
            if not testcase.passed:
                failed_testcase_list.append(testcase)
        return failed_testcase_list

    def add_testcase_result(self, testcase_result):
        """
        添加用例结果类
        Args:
            testcase_result: 用例结果类
        """
        if not isinstance(testcase_result, TestCaseResult):
            raise InstanceError("instance must be TestCaseResult class")

        self._set_status(testcase_result)

        self._results.append(testcase_result)

    def add_message(self, message):
        """
        添加用例集执行信息
        Args:
            message: 用例集执行过程中断言产生的信息

        Returns:

        """
        self.__message = message
        self._passed = False
        self._status = reslut_status.FAILED

    @property
    def message(self):
        """
        Returns:
            用例集执行过程中的信息
        """
        return self.__message

    @property
    def block_testcase_count(self):
        return len(self.block_testcase_list)

    @property
    def passed_testcase_count(self):
        return self._count_result(reslut_status.PASSED)

    @property
    def failed_testcase_count(self):
        return self._count_result(reslut_status.FAILED)

    @property
    def error_testcase_count(self):
        return self._count_result(reslut_status.ERROR)

    def _count_result(self, status):
        _count = 0
        for testcase in self._results:
            if status == reslut_status.PASSED:
                if testcase.get_status == reslut_status.PASSED:
                    _count += 1
            elif status == reslut_status.FAILED:
                if testcase.get_status == reslut_status.FAILED:
                    _count += 1
            elif status == reslut_status.ERROR:
                if testcase.get_status == reslut_status.ERROR:
                    _count += 1
        return _count


class TestCaseResult(BaseResult):
    """
    用例结果类
    """
    def __init__(self, name):
        self.__loop_times = 1
        self.__passed_times = 0
        self.__error_times = 0
        self.__failed_times = 0
        self.__message = {}     # message 信息字典
        self.log_relative_dir = None
        self.log_abs_dir = None
        self.loop_start_time = []
        self.loop_end_time = []
        self.__loop_status = []
        self.desc = ""  # 用例描述
        super(TestCaseResult, self).__init__(name)

    @property
    def loop_times(self):
        """
        Returns:
            循环次数
        """
        return self.__loop_times

    @loop_times.setter
    def loop_times(self, value):
        """
        设置循环次数
        Args:
            value: 循环次数
        """
        self.__loop_times = value

    @property
    def total_times(self):
        """
        Returns:
            用例已经进行循环测试的次数
        """
        return self.__failed_times + self.__passed_times + self.__error_times

    @property
    def passed_times(self):
        """
        Returns:
            用例已经进行循环测试成功的次数
        """
        return self.__passed_times

    @passed_times.setter
    def passed_times(self, value):
        """
        设置用例通过次数
        Args:
            value: 通过次数
        """
        if self._status == reslut_status.BLOCK:
            self._status = reslut_status.PASSED
        self.__passed_times = value

    @property
    def error_times(self):
        """
        Returns:
            用例已经进行循环测试成功的次数
        """
        return self.__error_times

    @error_times.setter
    def error_times(self, value):
        """
        设置用例通过次数
        Args:
            value: 通过次数
        """
        self._status = reslut_status.ERROR
        self.__error_times = value

    @property
    def failed_times(self):
        """
        Returns:
            用例压力测试失败次数
        """
        return self.__failed_times

    @failed_times.setter
    def failed_times(self, value):
        """
        设置用例压力测试失败次数
        Args:
            value: 用例压力测试失败次数
        """
        if self._status != reslut_status.ERROR:
            self._status = reslut_status.FAILED
        self.__failed_times = value

    def add_message(self, message):
        """
        添加用例执行过程中的信息
        Args:
            message: 用例执行过程中信息
        """
        if isinstance(message, list):
            message = ", ".join(message)
        loop_times = self.__passed_times + self.__failed_times
        loop_key = self.__message.get(loop_times, None)
        if loop_key:
            self.__message[loop_times].append(message)
        else:
            self.__message[loop_times] = [message]

    @property
    def message(self):
        """
        Returns:
            用例执行信息
        """
        return self.__message if self.__message else ""

    def get_loop_message(self, loop):
        return self.__message.get(loop, "")

    def loop_run_time(self, loop):
        """获取loop循环位置的时间"""
        if isinstance(loop, (int, float)) and loop < len(self.loop_end_time):
            return format_time(self.loop_end_time[loop] - self.loop_start_time[loop])
        else:
            return 0

    def get_loop_start_time_str(self, loop):
        if isinstance(loop, int) and loop < len(self.loop_start_time):
            if self.loop_start_time == 0:
                raise AttributeNotSet("start_time not be set")
            return time.ctime(self.loop_start_time[loop])
        return ""

    def get_loop_end_time_str(self, loop):
        if isinstance(loop, int) and loop < len(self.loop_end_time):
            if self.loop_end_time == 0:
                raise AttributeNotSet("start_time not be set")
            return time.ctime(self.loop_end_time[loop])
        return ""

    def log_name(self, loop):
        if self.__loop_times == 1:
            return "{}_log.txt".format(self.name)
        else:
            return "{}_loop{}_log.txt".format(self.name, loop)

    def loop_status(self, loop):
        status = reslut_status.PASSED
        if loop == self.total_times and self._status == reslut_status.ERROR:
            return self.status
        if self.__message.get(loop, None):
            status = reslut_status.FAILED
        return reslut_status.get_desc(status)

    @property
    def report_path(self):
        return os.path.join(self.log_relative_dir, self.report_name)

    @property
    def report_name(self):
        return "{}.html".format(self.name)

    @property
    def passed(self):
        return self._status == reslut_status.PASSED

    @property
    def is_pingback(self):
        pingback_dir = os.path.join(self.log_abs_dir, "pingback")
        return True if os.path.exists(pingback_dir) else False

    def report_pingback_path(self, loop=1):
        if self.__loop_times == 1:
            return "pingback/report.html"
        else:
            return "pingback/loop_{}/report.html".format(loop)


if __name__ == "__main__":
    project_test = ProjectResult("project")
    for j in range(2):
        loop_test = ProjectLoopResult("loop{}".format(j+1))
        for k in range(2):
            testsuite = TestSuiteResult("testsuite{}".format(k+1))
            for i in range(2):
                testcase = TestCaseResult("testcase%d" % i)
                # if i % 2:
                #     testcase.passed_times += 1
                # else:
                testcase.failed_times += 1
                testcase.add_message("testcaset1 message")
                testsuite.add_testcase_result(testcase)
            loop_test.add_testsuite_result(testsuite)
            print(loop_test.testcase_count)
            print(loop_test.failed_testcase_count)
        project_test.add_loop_result(loop_test)



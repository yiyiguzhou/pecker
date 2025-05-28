# -*- coding: UTF-8 -*-

"""
File Name:      testcase_base
Author:         zhangwei04
Create Date:    2018/1/3
"""
from abc import abstractmethod, ABCMeta
from framework.core.testcase_data_parse import TestCaseData


class TestSuiteBase(metaclass=ABCMeta):
    """用例集基类"""
    @abstractmethod
    def setup_testcase(self):
        """用例集执行前准备操作接口"""
        pass

    @abstractmethod
    def teardown_testcase(self):
        """用例集执行后收尾工作接口"""
        pass


class TestCaseBase(metaclass=ABCMeta):
    """用例基类"""
    def __init__(self):
        self.desc = ""  # 用例描述
        self.data = None

    def load_data(self, data_path_file):
        """
        加载用例数据
        Args:
            data_path_file:用例数据xml格式文件
        """
        self.data = TestCaseData(data_path_file)

    @abstractmethod
    def setup(self):
        """用例执行前准备工作接口"""
        pass

    @abstractmethod
    def test(self):
        """用例执行接口"""
        pass

    @abstractmethod
    def teardown(self):
        """用例执行后收尾工作接口"""
        pass

    @property
    def name(self):
        """用例名称"""
        return self.__class__.__name__
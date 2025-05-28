# -*- coding: UTF-8 -*-

"""
File Name:      ipecker
Author:         zhangwei04
Create Date:    2018/1/3
"""
import os
import inspect
from framework.exception.exception import AssertException
from framework.core.resource import MESSAGE, g_resource
from framework.logger.logger import g_logger
from framework.devices.target import Target
from framework.utils.func import local_time


def assert_true(func, desc='', target=None):
    """框架用例执行断言接口，断言函数执行返回结果值为True，若断言失败则用例直接抛出异常，不进行往下执行
    Args:
        func: 函数执行返回结果
        desc: 函数业务描述，失败时，能够通过该信息能够大致确认业务失败点
        target：目标对象，用于失败时截图

    Raises:
        AssertException 断言失败时，产生的异常
    """
    if not func:
        msg_info = __get_last_func(__get_current_func_name(), inspect.currentframe().f_back)
        MESSAGE.append(msg_info)
        g_logger.error(msg_info)
        __screen_shot(desc, target)

        raise AssertException

    if desc:
        g_logger.info("{} 执行成功".format(desc))


def assert_false(func, desc='', target=None):
    """框架用例执行断言接口，断言函数执行返回结果值为False；若断言失败则用例直接抛出异常，不进行往下执行，用例标记失败
    Args:
        func: 函数执行返回结果
        desc: 函数业务描述，失败时，能够通过该信息能够大致确认业务失败点
        target：目标对象，用于失败时截图
    Raises:
        AssertException 断言失败时，产生的异常
    """
    if func:
        msg_info = __get_last_func(__get_current_func_name(), inspect.currentframe().f_back)
        MESSAGE.append(msg_info)
        g_logger.error(msg_info)
        if desc:
            g_logger.error("{} 执行失败".format(desc))
        __screen_shot(desc, target)

        raise AssertException
    if desc:
        g_logger.info("{} 执行成功".format(desc))


def expect_true(func, desc='', target=None):
    """框架用例执行断言接口，断言函数执行返回结果值为True；若期望断言失败则继续往下执行，但用例标记为失败
    Args:
        func: 函数执行返回结果
        desc: 函数业务描述，失败时，能够通过该信息能够大致确认业务失败点
        target：目标对象，用于失败时截图
    """
    if not func:
        msg_info = __get_last_func(__get_current_func_name(), inspect.currentframe().f_back)
        MESSAGE.append(msg_info)
        g_logger.error(msg_info)
        if desc:
            g_logger.error("{} 执行失败".format(desc))
        __screen_shot(desc, target)
        return

    if desc:
        g_logger.info("{} 执行成功".format(desc))


def expect_false(func, desc='', target=None):
    """框架用例执行断言接口，断言函数执行返回结果值为False；若期望断言失败则继续往下执行，但用例标记为失败
    Args:
        func: 函数执行返回结果
        desc: 函数业务描述，失败时，能够通过该信息能够大致确认业务失败点
        target：目标对象，用于失败时截图
    """
    if func:
        msg_info = __get_last_func(__get_current_func_name(), inspect.currentframe().f_back)
        MESSAGE.append(msg_info)
        g_logger.error(msg_info)
        __screen_shot(desc, target)
        if desc:
            g_logger.error("{} 执行失败".format(desc))
        return

    if desc:
        g_logger.info("{} 执行成功".format(desc))


def __screen_shot(desc, target):
    if isinstance(target, Target) and target.device:
        desc_str = "_%s" % desc if desc else ""
        loop = "_loop%d" % g_resource["testcase_loop"] if g_resource["testcase_loop"] != 0 else ""
        log_file = "{}{}{}_failed.png".format(local_time(), desc_str, loop)

        log_path = os.path.join(g_resource['testcase_log_dir'], log_file)
        device_type = target.data.get('type', "").lower()
        if device_type == "android":
            target.device.adb.screen_shot(log_path)
        elif device_type == "pc":
            target.device.get_screenshot_as_file(log_path)


def __get_last_func(func_name, func_back):
    """获取回调栈中最近调用函数的代码信息，暂取最大数为20行
    Args:
        func_name: 函数名
        func_back: 程序执行回调栈

    Returns:
        最近调用函数的代码信息
    """
    left_brackets = -1  # '('数量
    find_func_flag = False
    length = 0

    while length < 20:
        length += 1
        code_context = inspect.getframeinfo(func_back, length).code_context

        if not find_func_flag and __fetch__func_name(reversed(code_context[:int((length + 1) / 2)]), func_name):
            func_pos = __find_func_pos(code_context, func_name)

            left_brackets = __get_brackets(code_context[func_pos:int((length + 1) / 2)], '(')
            find_func_flag = True

        if find_func_flag:
            func_pos = __find_func_pos(code_context, func_name)
            if func_pos == -1:
                continue
            right_pos_end = __fetch_right_brackets_pos_end(code_context, func_pos, left_brackets)
            if right_pos_end != -1:
                return "".join(line.strip() for line in code_context[func_pos:right_pos_end + 1])
                # return "".join(code_context[func_pos:right_pos_end + 1])
    return ""


def __fetch_right_brackets_pos_end(code_context, func_pos, left_brackets):
    """匹配右括号在栈中结束的相对位置
    Args:
        code_context: 函数代码信息
        func_pos: 函数断言起始位置
        left_brackets: 左括号个数

    Returns:
        函数结束代码行，相对开始行偏移位置
    """
    right_brackets = 0
    for i, code_line in enumerate(code_context[func_pos:]):
        right_brackets += code_line.count(')')
        if right_brackets == left_brackets:
            return i + func_pos
    return -1


def __find_func_pos(code_context, func_name):
    """查找函数断言关键字位置
    Args:
        code_context: 函数代码信息栈
        func_name: 函数断言关键字

    Returns:
        函数断言关键字在信息栈中的位置，若没找到则返回-1
    """
    length = len(code_context)

    if length == 1:
        length = 0
    for i in range(int((length + 1) / 2), -1, -1):
        if func_name in code_context[i]:
            return i
    return -1


def __fetch__func_name(code_context, func_name):
    """确认断言接口是否在函数栈中
    Args:
        code_context: 函数代码信息栈
        func_name: 函数断言接口关键字

    Returns:
        若在函数代码栈中找到函数断言关键字，则返回True，否则返回False
    """
    for code_line in code_context:
        if func_name in code_line:
            return True
    return False


def __get_current_func_name():
    """获取当前函数名字
    Returns:
        函数名字
    """
    return inspect.stack()[1][3]


def __get_brackets(code_context, brackets):
    """获取括号数量
    Args:
        code_context: 函数代码信息栈
        brackets: 括号标记，范围：'(', ')'

    Returns:
        括号数量
    """
    number = 0
    for context in code_context:
        number += context.count(brackets)
    return number


if __name__ == "__main__":

    def __test(a, *arg):
        return a

    expect_true(__test(5,6,7,8))
    assert_true(1)
    assert_true(__test(False,
                     2,
                     3,
                     'test'))
    assert_true(__test(0, 10, 11, 12)) #

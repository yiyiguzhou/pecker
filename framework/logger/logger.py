# -*- coding: UTF-8 -*-

"""
File Name:      logger
Author:         zhangwei04
Create Date:    2017/12/25
"""

import os
import logging
import platform
from contextlib import contextmanager
from framework.core.resource import g_resource

# ui
from framework.ui.signal.Signal import g_signal

__FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'


class Logger(logging.Logger):
    """日志打印类"""
    def __init__(self, name, level=logging.NOTSET):
        self.__handle_stack = []
        self.__console_stream_handle = None
        super(Logger, self).__init__(name, level)
        self._ue = None

    def set_ui_console(self, ue):
        """ui界面设置打印回调"""
        self._ue = ue

    def addHandler(self, hdlr):
        """
        添加一个handler
        Args:
            hdlr: 输出流句柄
        """
        super(Logger, self).addHandler(hdlr)
        if isinstance(hdlr, logging.FileHandler):
            self.__handle_stack.append(hdlr)
        else:
            self.__console_stream_handle = hdlr

    def debug(self, msg, console=True, *args, **kwargs):
        """
        debug等级日志打印接口
        Args:
            msg: 日志格式化字符串信息
            console: 是否控制台输出
            *args: 字符串格式化合入参数
            **kwargs: 堆栈信息开关字典，exc_info, stack_info, and extra
        """
        if self._ue and console:
            # self._ue.normal_output_written(str(msg) + "\n")
            g_signal.ui_print.emit(str(msg) + "\n")
        with self.__check_console(console):
            super(Logger, self).debug(msg, *args, **kwargs)

    def info(self, msg, console=True, *args, **kwargs):
        """
        info等级日志打印接口
        Args:
            msg: 日志格式化字符串信息
            console: 是否控制台输出
            *args: 字符串格式化合入参数
            **kwargs: 堆栈信息开关字典，exc_info, stack_info, and extra
        """
        if self._ue and console:
            # self._ue.normal_output_written(str(msg) + "\n")
            g_signal.ui_print.emit(str(msg) + "\n")
        with self.__check_console(console):
            super(Logger, self).info(msg, *args, **kwargs)

        return True

    def warning(self, msg, console=True, *args, **kwargs):
        """
        warning等级日志打印接口
        Args:
            msg: 日志格式化字符串信息
            console: 是否控制台输出
            *args: 字符串格式化合入参数
            **kwargs: 堆栈信息开关字典，exc_info, stack_info, and extra
        """
        if self._ue and console:
            # self._ue.normal_output_written(str(msg) + "\n")
            g_signal.ui_print.emit(str(msg) + "\n")
        with self.__check_console(console):
            super(Logger, self).warning(msg, *args, **kwargs)

        return True

    def error(self, msg, console=True, *args, **kwargs):
        """
        error等级日志打印接口
        Args:
            msg: 日志格式化字符串信息
            console: 是否控制台输出
            *args: 字符串格式化合入参数
            **kwargs: 堆栈信息开关字典，exc_info, stack_info, and extra
        """
        if self._ue and console:
            g_signal.ui_print.emit(str(msg) + "\n")
            # self._ue.normal_output_written(msg + "\n")
        with self.__check_console(console):
            super(Logger, self).error(msg, *args, **kwargs)

        return False

    def critical(self, msg, console=True, *args, **kwargs):
        """
        critical等级日志打印接口(框架保留)
        Args:
            msg: 日志格式化字符串信息
            console: 是否控制台输出
            *args: 字符串格式化合入参数
            **kwargs: 堆栈信息开关字典，exc_info, stack_info, and extra
        """
        if self._ue and console:
            # self._ue.normal_output_written(str(msg) + "\n")
            g_signal.ui_print.emit(str(msg) + "\n")
        with self.__check_console(console):
            super(Logger, self).critical(msg, *args, **kwargs)

    def switch_handle(self, hdlr):
        """
        切换输出流句柄
        """
        if self.__handle_stack:
            self.removeHandler(self.__handle_stack[-1])
        self.addHandler(hdlr)

    def pop_handle(self):
        """
        输出流句柄弹栈操作
        """
        if self.__handle_stack:
            self.removeHandler((self.__handle_stack.pop()))
            super(Logger, self).addHandler(self.__handle_stack[-1])

    @contextmanager
    def __check_console(self, console):
        """
        检查控制台句柄操作，当调用log打印等级接口时，使用此接口进行控制控制台输出操作
        Args:
            console: 是否开心控制台标记
        yield:
            控制台标记
        """
        if not console and self.__console_stream_handle:
            self.removeHandler(self.__console_stream_handle)
        yield console
        if not console and self.__console_stream_handle:
            self.addHandler(self.__console_stream_handle)


def logger_factory(log_path, name=None, console=False,  level=logging.DEBUG):
    """
    日志工厂函数，用于生产日志log类
    Args:
        log_path: 日志文件目录
        name: 日志文件名称
        console: 是否打印控制台
        level: 日志输出级别
    Returns:
        产生的日志类
    """
    if not name:
        from framework.utils.func import random_str
        name = random_str(10)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handle = logging.FileHandler(log_path, encoding='utf-8')
    file_handle.setFormatter(logging.Formatter(__FORMAT))
    logger.addHandler(file_handle)

    if console:
        stream_hanler = logging.StreamHandler()
        # stream_hanler.setFormatter(logging.Formatter(__FORMAT))
        logger.addHandler(stream_hanler)
    return logger


def _add_coloring_to_emit_windows(fn):
    """
    windows下控制台打印颜色
    Args:
        fn: logging模块 emit函数地址
    Returns:
        新的添加打印颜色的emit函数地址
    """
    def _set_color(self, code):
        import ctypes
        # Constants from the Windows API
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    setattr(logging.StreamHandler, '_set_color', _set_color)

    def new(*args):
        FOREGROUND_BLACK = 0x0000
        FOREGROUND_BLUE = 0x0001
        FOREGROUND_GREEN = 0x0002
        FOREGROUND_CYAN = 0x0003
        FOREGROUND_RED = 0x0004
        FOREGROUND_MAGENTA = 0x0005
        FOREGROUND_YELLOW = 0x0006
        FOREGROUND_GREY = 0x0007
        FOREGROUND_INTENSITY = 0x0008  # foreground color is intensified.
        FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED

        BACKGROUND_BLACK = 0x0000
        BACKGROUND_BLUE = 0x0010
        BACKGROUND_GREEN = 0x0020
        BACKGROUND_CYAN = 0x0030
        BACKGROUND_RED = 0x0040
        BACKGROUND_MAGENTA = 0x0050
        BACKGROUND_YELLOW = 0x0060
        BACKGROUND_GREY = 0x0070
        BACKGROUND_INTENSITY = 0x0080  # background color is intensified.

        level_no = args[1].levelno
        if level_no >= 50:
            color = FOREGROUND_BLUE | FOREGROUND_RED
        elif level_no >= 40:
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif level_no >= 30:
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif level_no >= 20:
            # color = FOREGROUND_GREEN
            color = FOREGROUND_WHITE
        elif level_no >= 10:
            color = FOREGROUND_WHITE
        else:
            color = FOREGROUND_WHITE
        args[0]._set_color(color)

        ret = fn(*args)
        args[0]._set_color(FOREGROUND_WHITE)
        return ret
    return new


def _add_coloring_to_emit_ansi(fn):
    """
    unix下控制台打印颜色
    Args:
        fn: logging模块 emit函数地址
    Returns:
        新的添加打印颜色的emit函数地址
    """
    def new(*args):
        level_no = args[1].levelno
        if level_no >= 50:
            color = '\x1b[35m'  # pink
        elif level_no >= 40:
            color = '\x1b[31m'  # red
        elif level_no >= 30:
            color = '\x1b[33m'  # yellow
        elif level_no >= 20:
            color = '\x1b[0m'  # green
        elif level_no >= 10:
            color = '\x1b[0m'  # pink
        else:
            color = '\x1b[0m'  # normal
        msg = args[1].msg
        if not isinstance(msg, str):
            msg = str(msg)

        if not msg.endswith('\x1b[0m'):
            if not isinstance(msg, str):
                msg = str(msg)
            args[1].msg = color + msg + '\x1b[0m'  # normal
        return fn(*args)
    return new


# logging.basicConfig(level=logging.DEBUG, format=__FORMAT)
logging.setLoggerClass(Logger)  # 设置日志Logger类

# log颜色函数封装
if platform.system() == 'Windows':
    logging.StreamHandler.emit = _add_coloring_to_emit_windows(logging.StreamHandler.emit)
# else:
#     logging.StreamHandler.emit = _add_coloring_to_emit_ansi(logging.StreamHandler.emit)

# 创建框架及工程log
g_framework_logger = logger_factory(log_path=os.path.join(g_resource['log_path'], 'framework_log.txt'), name='framework')
g_logger = logger_factory(log_path=os.path.join(g_resource['log_path'], 'ipecker_log.txt'), console=True, name='ipecker')


@contextmanager
def switch_log_path(log_dir, log_file):
    """
    切换log，用于重新定向到目标log文件中
    Args:
        log_dir: 目标log路径目录
        log_file: 目标log文件名

    yield:
        切换后的日志类
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = os.path.join(log_dir, log_file)

    file_handle = logging.FileHandler(log_path, encoding='utf-8')
    file_handle.setFormatter(logging.Formatter(__FORMAT))
    g_logger.switch_handle(file_handle)
    yield g_logger
    g_logger.pop_handle()


if __name__ == "__main__":
    floger = logger_factory("framework_log.txt", 'framework')
    floger.debug(" floger debug")
    floger.info(" floger info")
    floger.warning(" floger warning")
    floger.error(" floger error")
    g_logger.debug(console=False, msg=" gloger debug")
    g_logger.info(" gloger info")
    g_logger.warning(" gloger. warning")
    g_logger.error(" gloger. error")

    with switch_log_path('.', "testcase_log1.txt"):
        g_logger.debug(" 1gloger debug")
        g_logger.info(" 1gloger info")
        g_logger.warning(" 1gloger. warning")
        g_logger.error(" 1gloger. error")
        g_logger.info("log start")
        with switch_log_path('.', "testcase_log2.txt"):
            g_logger.debug(" 2gloger debug")
            g_logger.info(" 2gloger info")
            g_logger.warning(" 2gloger. warning")
            g_logger.error(" 2gloger. error")
        g_logger.info("log end")

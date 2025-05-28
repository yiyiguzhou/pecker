# -*- coding: UTF-8 -*-

"""
File Name:      func
Author:         zhangwei04
Create Date:    2017/12/27
"""
import time
import datetime
import sys
import os
import math
from framework.logger.logger import g_framework_logger
from framework.exception.exception import TimeoutException


def introspect(module_path, attr_name=None):
    """
    发射功能函数，根据传入的module_path获取attr_name属性实例，若attr_name为None，则划分module_path最后的模板名作为属性
    Args:
        module_path: 模块路径
        attr_name: 属性名

    Returns:
        属性实例
    """
    ret = None
    module_path = module_path.replace("\\", "/")
    if not attr_name:
        md_split = module_path.rsplit("/", 1)
        if len(md_split) > 1:
            attr_name = md_split[1]
            module_name = md_split[1]
            module_path = md_split[0]
        else:
            attr_name = md_split[0]
            module_name = md_split[0]
    else:
        md_split = module_path.rsplit("/", 1)
        module_name = md_split[1]
        module_path = md_split[0]

    try:
        sys.path.insert(0, os.path.abspath(module_path))
        module_obj = __import__(module_name, globals(), locals(), [attr_name], 0)
        ret = getattr(module_obj, attr_name)
        sys.path.pop(0)
    except Exception as e:
        g_framework_logger.exception(e)
        raise e

    return ret


def make_dirs(path, *more_dir):
    """
    创建目录
    Args:
        path: 目录路径
        *more_dir: 多层目录
    """
    for dir in more_dir:
        path = os.path.join(path, dir)
    if not os.path.exists(path):
        os.makedirs(path)


def random_str(length=10):
    """随机字符串功能
    Args：
        length: 随机的字符串长度
    """
    import random
    import string
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def local_time():
    """
    获取本地格式化的日期
    Returns:
        格式化的时间字符串,如'05-06_14h_50m_59s_637ms'
    """
    now_time = datetime.datetime.now()
    time_str = now_time.strftime('%m-%d_%Hh_%Mm_%Ss')
    time_ms = now_time.strftime("%f")[:2]
    return "{}_{}ms".format(time_str, time_ms)


def format_time(seconds):
    """
    根据描述，格式化月日时分秒时间
    Args:
        seconds: 秒数，基于time.time()获取的时间
    Returns:
        时间字符串
    """
    # 获取毫秒
    ms = int(math.modf(seconds)[0] * 1000)
    time_str = "%d毫秒" % ms

    m, s = divmod(seconds, 60)
    if s == 0:
        return time_str

    time_str = "%d秒%s" % (s, time_str)
    if m == 0:
        return time_str

    h, m = divmod(m, 60)
    time_str = "%d分%s" % (m, time_str)
    if h == 0:
        return time_str

    d, h = divmod(h, 24)
    time_str = "%d小时%s" % (h, time_str)
    if d == 0:
        return time_str
    else:
        return "%d天%s" % (d, time_str)


class TestBuilt():
    def print1(self):
        print("this is DUT")


def timeout_decorate(dec_timeout, ignore_exception=True):
    """
    超时修饰器，用于执行时间短，失败时需要重复执行的操作修饰
    Args:
        dec_timeout: 修饰器时间
        ignore_exception: 是否忽略异常

    Returns:

    """
    def decorate(func):
        def wrapper(*args, **kwargs):
            timeout = kwargs.get('timeout', dec_timeout)

            if not isinstance(timeout, (int, float)):
                timeout = float(timeout)

            time_start = time.time()
            while time_start + timeout > time.time():
                try:
                    ret = func(*args, **kwargs)
                    break
                except Exception as e:
                    if not ignore_exception:
                        raise e
            else:
                raise TimeoutException("run func: {}, params: ({},{}) timeout".format(func.__name__, args, kwargs))
            return ret

        return wrapper
    return decorate


def ping_back(func):
    def wrapper(*args, **kwargs):
        index_list = kwargs.get('index_list', None)
        sleep_time = kwargs.get('sleep_time', 5)
        no_order_list = kwargs.get('no_order_index', None)
        mitm_obj = kwargs.get('mitm', None)
        if mitm_obj:
            if isinstance(index_list, int):
                index_list = [index_list]
            mitm_obj.to_file_end()

        ret = func(*args, **kwargs)

        if mitm_obj and index_list:
            time.sleep(sleep_time)
            desc = kwargs.get('desc', "")
            status = mitm_obj.match(index_list=index_list, no_order_list=no_order_list, desc=desc)
            if status == "failed":
                from framework.core.runner import MESSAGE
                MESSAGE.append("步骤：{} 数据投递执行失败".format(desc))
        return ret

    return wrapper


def get_file_dir(ser_dir, f, file_type=""):
    """
     遍历目录，得到文件的绝对路径
        Args:
            ser_dir: 搜索的当前目录
            f: 搜索的目标文件
            file_type: 文件类型

        Returns:

        """
    path_list = []
    for dirpath, dirs, files in os.walk(ser_dir, topdown=False):
        file_name = "{}.{}".format(f, file_type) if file_type else f
        if file_name in files:
            path_list.append(os.path.join(dirpath, f))

    return path_list


if __name__ == "__main__":
    import os
    # module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "project", "script", "sdk", "TestSdk1"))
    # module_path = os.path.abspath(
    #     os.path.join(os.path.dirname(__file__), "..", "..", "project.lib.sdk.TestSdl"))
    # cls = introspect(module_path, 'SdkDemo')
    # try:
    #
    #     # ins = cls()
    #     ins = cls("dtest")
    #     ins.print()
    #     print(sys.modules)
        # ins.setup()
        # ins.test()
        # ins.teardown()
    # except Exception as e:
    #     g_framework_logger.exception(e)
    # print(get_file_dir('jinja2', "__init__.py", ""))

    __builtins__.__dict__['DUT'] = TestBuilt()
    test_built()
    pass

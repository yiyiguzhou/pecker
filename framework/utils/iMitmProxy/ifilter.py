# -*- coding: UTF-8 -*-

"""
File Name:      ifilter
Author:         zhangwei04
Create Date:    2018/7/23
"""


class IFilter:
    def __init__(self, file_path, filter_key="GET https://msg", encoding='utf-8', next_line=False):
        self._file_path = file_path
        self._filter_key = filter_key
        self._encoding = encoding
        self._next_line = next_line
        self._seek_pos = 0

    def open(self):
        try:
            with open(self._file_path, 'r', encoding=self._encoding) as f:
                f.seek(self._seek_pos)
                for line in f:
                    if self._filter_key in line:
                        if self._next_line:
                            yield line, f.readline()
                        else:
                            yield line
                self._seek_pos = f.tell()
        except Exception as e:
            with open(self._file_path, 'r', encoding='GBK') as f:
                f.seek(self._seek_pos)
                for line in f:
                    if self._filter_key in line:
                        if self._next_line:
                            next_line = f.readline()
                            yield line, next_line
                        else:
                            yield line
                self._seek_pos = f.tell()


def filter_open(file_path, filter_key="GET https://msg", encoding='utf-8', next_line=False):
    """过滤方式打开文件
    Args:
        file_path: 文件路径
        filter_key: 过滤关键字
        encoding: 编码方式
    """
    try:
        with open(file_path, encoding=encoding) as f:

            for line in f:
                if filter_key in line:
                    if next_line:
                        yield line, f.readline()
                    else:
                        yield line
    except:
        with open(file_path, encoding='GBK') as f:
            for line in f:
                if filter_key in line:
                    if next_line:
                        yield line, f.readline()
                    else:
                        yield line


def get_status_code(status_code_line):
    line_split_list = status_code_line.split()
    for line_split in line_split_list:
        if line_split.isdigit():
            return line_split
    return None


def format_http_msg(get_msg):
    """
    解析http(s)请求文本行，解析成字典方式返回
    Args:
        get_msg: http(s)请求数据行
    Return:
        解析后存放数据的字典
    """
    ret_msg = {}
    try:
        if "https://" in get_msg:
            http_pos = get_msg.find("https://")+len("https://")
        elif "http://" in get_msg:
            http_pos = get_msg.find("http://") + len("http://")
        else:
            print("{} is not http requese".format(get_msg))
            return ret_msg
        # 获取host
        ret_msg['host'] = get_msg[http_pos:get_msg.find("/", http_pos)]
        http_pos += len(ret_msg['host'])
        # 获取path
        ret_msg['path'] = get_msg[http_pos:get_msg.find("?", http_pos)]
        http_pos += len(ret_msg['path']) + 1
        # 获取参数
        params_pairs = get_msg[http_pos:get_msg.find("#", http_pos)]
        ret_msg['params'] = {}
        for params_pair in params_pairs.split("&"):
            if params_pair == "":
                continue
            params_split = params_pair.split("=")
            if len(params_split) == 2:
                ret_msg['params'][params_split[0].strip()] = params_split[1].strip()
        http_pos += len(params_pairs)
    except:
        print('request {} get paramter error'.format(get_msg))
    return ret_msg


if __name__ == "__main__":
    http_format_list = []

    ifilter = IFilter("mitmproxy.txt", filter_key='GET http://msg.qy.net', next_line=True)
    # line_list, next_line_list = ifilter.open()
    for http_line, status_code in ifilter.open():
        pass
        print(get_status_code(status_code))
        print(format_http_msg(http_line))
    print("###########################")
    for http_line, status_code in ifilter.open():
        print(get_status_code(status_code))
        print(format_http_msg(http_line))
        pass


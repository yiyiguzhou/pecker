# -*- coding: UTF-8 -*-

"""
File Name:      finder
Author:         zhangwei04
Create Date:    2018/3/15
"""
import os


class Finder(object):
    """文件查找器"""
    def __init__(self):
        self.__file_dict = {} # 文件字典，key:文件绝对路径， value：文件位置

    def find(self, keys, file_path=None, flag='or', regular=None):
        """
        查找文件关键字，若文件已经查找过，则基于上次的位置往下继续查找。
        返回包含key的行信息，若regular为None，则返回找到的行信息，
        否则返回正则表达式regular匹配到此行的信息
        Args:
            file_path: 查找文件路径
            keys: 查找关键字（或列表）
            flag: 多个关键字时，查找多个关键字的逻辑与、或操作，即同时满足还是至少满足一个条件标志
            regular: 非None时，正则方式匹配查找到的行返回匹配到的信息；None值时，返回查到到的行
        Returns:
            若查找匹配到信息，返回信息，否则返回None
        """
        if flag not in ('or', 'and'):
            raise Exception("paramater: flag value must be or/and")

        if file_path:   # 传入文件则检查文件是否存在
            if os.path.exists(file_path):
                file_abs_path = os.path.abspath(file_path)
                return self.__find_key(keys, file_abs_path, self.__file_dict.get(file_abs_path, 0), flag=flag, regular=regular)
            else:
                raise Exception("can not find file:{}".format(file_path))
        else:
            if len(self.__file_dict) == 1:
                for file_abs_path in self.__file_dict:
                    return self.__find_key(keys, file_abs_path, self.__file_dict[file_abs_path], flag=flag, regular=regular)
            else:
                raise Exception("must be take file name because finder has more than one file")

    def __find_key(self, keys, file_abs_path, pos, flag='or', regular=None):
        """
        按照规则匹配查找到的关键字行信息
        Args:
            keys: 查找关键字（或列表)
            file_abs_path: 文件绝对路径
            pos: 文件上次查找位置，初始值为0
            flag: 多个关键字与或操作
            regular: 匹配规则

        Returns:
            None:没有找到关键字行，或者没有匹配到关键字行的规则
            list类型信息：匹配到的信息，
            str类型：没有使用匹配规则，直接返回找到的行
        """
        line = self.__get_line(keys, file_abs_path, pos, flag)
        if line:
            if isinstance(regular, str):
                import re
                pat = re.compile(repr(regular))
                match = pat.match(line)
                if match:
                    return match.group()
            else:
                return line
        return None

    def __get_line(self, keys, file_abs_path, pos, flag='or'):
        """
        根据关键字获取到文件行信息
        Args:
            keys: 查找关键字（或列表）
            file_abs_path: 查找文件的绝对路径
            pos: 起始查找位置
            flag: 关键字与或操作

        Returns:
            None：没有找到包含关键字的信息行
            str类型：找到的关键字行
        """
        find_line = None
        new_pos = pos
        with open(file_abs_path, "rb") as fp:
            fp.seek(pos)
            if isinstance(keys, (set, tuple)):
                keys = list(keys)
            else:
                keys = [str(keys)]

            for line in fp:
                new_pos += len(line)
                line = str(line, encoding='utf-8')

                if flag == 'or':
                    for key in keys:
                        if key in line:
                            find_line = line
                            break
                else:  # and操作
                    for key in keys:
                        if key not in line:
                            break
                    else:
                        find_line = line

                if find_line is not None:
                    break

            self.__file_dict[file_abs_path] = new_pos   # 更新文件位置
            return find_line

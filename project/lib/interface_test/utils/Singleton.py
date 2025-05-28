# -*- coding: UTF-8 -*-

"""
File Name:      Singleton
Author:         xumohan
Create Date:    2018/7/17
"""
# 单例模式，保证全局可用testcase_id且只有一个
class Singleton(object):
    instance = None


    def __init__(self, id, name):
        self.id = id
        self.name = name


    @classmethod
    def get_instance(cls, id, name, flag):
        if flag == False:
            if cls.instance:
                return cls.instance
            else:
                obj = cls(id, name)
                cls.instance = obj
                return obj
        else:
            obj = cls(id, name)
            cls.instance = obj
            return obj





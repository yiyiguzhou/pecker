# -*- coding: UTF-8 -*-

"""
File Name:      main
Author:         zhangwei04
Create Date:    2017/12/22
"""

import os
import sys
import getopt
from framework.core.resource import g_resource, OrderSet
from framework.exception.exception import FileNotFound, ParamaterError, ParameterTypeError
from framework.core.dispatch import Dispatch


def parse_args():
    short_opts = 'a:l:o:x:'
    long_opts = ['aml=', 'loop=', 'order=', 'xml=']
    options, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)

    args_data = g_resource.get('input_args')

    args_data["order"] = None
    args_data["loop"] = None
    # 解析参数)
    for name, value in options:
        if name in ('-a', '--aml'):
            args_data["aml"] = value
        elif name in ('-l', '--loop'):
            args_data["loop"] = value
        elif name in('-o', '--order'):
            args_data["order"] = value
        elif name in ('-x', '--xml'):
            args_data["xml"] = value
        else:
            usage()
            exit(-1)

    # check parameter
    if not (args_data.get('aml', None) and args_data.get('xml', None)):
        raise ParamaterError('xml and aml are necessary input parameters')

    # check parameter type
    if args_data['order'] and args_data['order'] not in OrderSet().values:
        raise ParameterTypeError('parameter: order is illegal and must be in normal,auto,random')
    try:
        if args_data["loop"]:
            args_data["loop"] = int(args_data["loop"])
    except Exception as e:
        raise ParameterTypeError('parameter: loop must be number')

    # check file if exists
    project_file_path = os.path.join(g_resource['project_path'], 'project')
    args_data['xml'] = os.path.join(project_file_path, args_data['xml'])
    args_data['aml'] = os.path.join(project_file_path, args_data['aml'])
    if not os.path.exists(args_data['xml']):
        raise FileNotFound('project xml file not found')
    if not os.path.exists(args_data['aml']):
        raise FileNotFound('device aml file not found')


def usage():
    """
    help message
    """
    print('''input paramater error, please check!
    usage:
    python run_ipecker.py --xml=default.xml --aml=default.aml --loop=1 --order=auto
    ''')


def start():
    parse_args()

    dispatch = Dispatch()
    dispatch.start()


if __name__ == '__main__':
    start()
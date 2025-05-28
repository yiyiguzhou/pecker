# coding=utf-8
import json
import sys
import unittest

from project.lib.interface_test.testcase import Request
from project.lib.interface_test.utils import toJson, generateReport, Singleton
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.testcase import runWay

sys.setrecursionlimit(1000000)


def getTest(single_test_case):
    response = Request.sendRequest(single_test_case)
    response_decode = Request.get_response(response)
    ss = response_decode.encode('utf-8').decode('unicode_escape')
    #print(response_decode.encode('utf-8'))

    if response_decode != '':
        response_decode = toJson.to_json_string(response_decode)
        expect_true(toJson.is_json(response_decode), single_test_case['testcase_id'] +' Json格式校验')
        results = json.loads(response_decode, encoding='utf-8')
        runWay.check_data(results, single_test_case)


def run_test_case(file):

    test_single_test_case = generateReport.get_test_cases(file)
    for single_test_case in test_single_test_case:
        obj = Singleton.Singleton.get_instance(single_test_case['testcase_id'], single_test_case["testcase_name"], True)
        print('++++++++++++++', obj.id, obj.name, '++++++++++++++')
        getTest(single_test_case)


#run_test_case("D:\\test\\auto\\code\\ipecker\\project\\script\\interface_test\\houtai\\card_cardlist.xml")

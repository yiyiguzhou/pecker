# -*- coding: UTF-8 -*-
import hashlib
import time
import requests
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.utils import toJson


# 鎷兼帴url锛岃幏鍙栬繑鍥炴暟鎹�
def splice_url(single_test_case):
    if '%{timestamp}' in single_test_case["url_parameter"]:

        cur_time = str(int(time.time()))
        single_test_case["url_parameter"] = single_test_case["url_parameter"].replace('%{timestamp}', cur_time)
        print (cur_time)
    # 鑷姩鏍规嵁褰撳墠鐨勬椂闂存埑锛岀畻鍑烘帴鍙ｇ殑sign鍊硷紝骞舵浛鎹㈠師鏉ョ殑瀛楃涓�

    if 'sign=%{sign}' in single_test_case["url_parameter"]:
        single_test_case["url_parameter"] = single_test_case["url_parameter"].replace('sign=%{sign}', 'sign_key=1234567890')
        # 拼接参数
        ll = single_test_case["url_parameter"].split('&')
        # 清除空传参
        for n in ll:
            if n.endswith('='):
                ll.remove(n)

        ll_sorted = sorted(ll)
        sdict = '&'.join(ll_sorted)
        myMd5 = hashlib.md5()
        myMd5.update(sdict.encode("utf8"))
        sign_md5 = myMd5.hexdigest()

        print (sign_md5)
        # 替换sign值
        single_test_case["url_parameter"] = single_test_case["url_parameter"].replace('sign_key=1234567890', 'sign=' + sign_md5)
    else:
        sign_md5 = ""

    url_place = single_test_case["url_place"]
    url_parameter = single_test_case["url_parameter"]
    return url_place, url_parameter, sign_md5


def check_response_method(s):
    if s in ("GET", "POST", "POST_BODY"):
        return True
    else:
        return False


def sendRequest(single_test_case):
    url_palce, url_parameter, sign_md5 = splice_url(single_test_case)
    expect_true(check_response_method(single_test_case["response_method"].upper()), single_test_case['testcase_name'] + ' GET/POST方法设置')
    # 发送请求
    if (single_test_case["response_method"]).upper() == 'GET':
        url = url_palce + url_parameter
        response = requests.request("GET", url)
    elif (single_test_case["response_method"]).upper() == 'POST':
        url = url_palce + url_parameter
        response = requests.request("POST", url)
    else:
        if 'sign=%{sign}' in url_parameter:
            url_parameter = url_parameter.replace('sign=%{sign}', 'sign=' + sign_md5)
        bodydata = url_parameter.split('&')
        payload = dict()
        for b in bodydata:
            kv1 = b.split('=')
            k1 = kv1[0]
            v1 = kv1[1]
            payload[k1] = v1
            url = url_palce + url_parameter
        response = requests.post(url, data=payload)
    ss = response.encoding

    print(response.url)
    return response

def get_response(response):
    # 处理返回值
    #rtext = response.text
    b = response.content
    bb = b.decode('unicode_escape')
    a = response.text.encode('utf-8')
    rtext = response.text.encode('utf-8').decode('unicode_escape')

    response_decode = rtext.replace(" ", "").replace("\n", "").replace("\r", "")
    response_decode = str(response_decode).replace("\\", '').replace("\\", "\\\\")

    wlist = []
    for a in (
            '\"video\"', '\"detail\"', '\"content\"', '\"brief\"', '\"tpl_contents\"', '\"use_method\"',
            '\"qudao_desc\"',
            '\"qudao_desc\"'):
        if a in response_decode:
            wlist.append(a)

    for a in wlist:
        rkey = a
        response_decode = toJson.json_string(rkey, response_decode, response_decode)

    response_decode = response_decode.replace("null,", "\"\",")
    return response_decode


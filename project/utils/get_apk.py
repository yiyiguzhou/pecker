# -*- coding: UTF-8 -*-

"""
File Name:      get_apk
Author:         zhangwei04
Create Date:    2018/9/25
"""
import os
import re
import requests


def _get_apk_list(apk_dir_url):
    r = requests.get(apk_dir_url)

    if apk_dir_url.endswith(".apk"):
        url_list = os.path.split(apk_dir_url)
        apk_name = url_list[1]
        apk_list = [apk_name]
    else:
        apk_list = re.findall(r'href="([\w|_|\-|\\.]*\.apk)"', r.content.decode())
    return apk_list


def download_apk(apk_dir_url, apk_name, save_dir='.'):
    """
    下载apk
    Args:
        apk_dir_url: apk下载链接，若不是以.apk结尾，则认为是apk下载目录，找到apk链接下载
        save_dir: apk保存目录
    Returns:
        True：进入成功
        False：进入失败
    """
    # r = requests.get(apk_dir_url)
    #
    # if apk_dir_url.endswith(".apk"):
    #     url_list = os.path.split(apk_dir_url)
    #     apk_dir_url = url_list[0]
    #     apk_name = url_list[1]
    #     apk_list = [apk_name]
    # else:
    #     apk_list = re.findall(r'href="([\w|_|\-|\\.]*\.apk)"', r.content.decode())

    pattern = "{}{}" if apk_dir_url.endswith(("\\", "/")) else "{}/{}"

    url = pattern.format(apk_dir_url, apk_name)
    with open(os.path.join(save_dir, apk_name), "wb") as code:
        print("download: {}".format(url))
        r = requests.get(url)
        code.write(r.content)


def get_base_apk():
    base_apk_url = 'http://10.13.43.127:8888/view/Android%E5%9F%BA%E7%BA%BF%E7%BC%96%E8%AF%91/job/Android_iQiYi_Build_Trunck/lastSuccessfulBuild/artifact/output/apk'
    save_dir = os.path.join(os.path.dirname(__file__), "..", "app_pkg")
    apk_name_list = _get_apk_list(base_apk_url)
    for apk_name in apk_name_list:
        if "video_" in apk_name.lower():
            # 写版本号
            download_apk(base_apk_url, apk_name, save_dir)
            version = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3})', apk_name)[0]
            with open(os.path.join(save_dir, "base_version.txt"), "w") as fp:
                fp.write(version)

            base_apk_name = "iqiyi.apk"
            base_apk_path = os.path.join(save_dir, base_apk_name)
            if os.path.exists(base_apk_path):
                os.remove(base_apk_path)
            os.rename(os.path.join(save_dir, apk_name), base_apk_path)


def get_gamecenter_apk():
    gamecenter_apk_url = 'http://10.110.89.186/jenkins/job/Android-Gphone%E6%B8%B8%E6%88%8F%E4%B8%AD%E5%BF%83/job/gamecenter-revision/lastSuccessfulBuild/artifact/output/apk/'
    gamecenter_project_dir = 'http://10.110.89.186/jenkins/job/Android-Gphone游戏中心/job/gamecenter-revision/'
    save_dir = os.path.join(os.path.dirname(__file__), "..", "app_pkg")
    apk_name_list = _get_apk_list(gamecenter_apk_url)
    for apk_name in apk_name_list:
        if "com.qiyi.gamecenter" in apk_name.lower():
            download_apk(gamecenter_apk_url, apk_name, save_dir)
            # 获取构建好号
            version_tuple = re.findall(r"_(\d{1,10})\.", apk_name)
            if version_tuple:
                build_num = version_tuple[0]
                with open(os.path.join(save_dir, "gamecenter_build_url.txt"), "w") as fp:
                    fp.write("{}{}".format(gamecenter_project_dir, build_num))

            gamecenter_apk_name = "com.qiyi.gamecenter.apk"
            gamecenter_apk_path = os.path.join(save_dir, gamecenter_apk_name)
            if os.path.exists(gamecenter_apk_path):
                os.remove(gamecenter_apk_path)
            os.rename(os.path.join(save_dir, apk_name), gamecenter_apk_path)


if __name__ == "__main__":
    get_base_apk()
    get_gamecenter_apk()

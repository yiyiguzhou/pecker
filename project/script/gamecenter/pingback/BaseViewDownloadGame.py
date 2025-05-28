# -*- coding: UTF-8 -*-

"""
File Name:      DownloadGamePressure
Author:         zhangwei04
Create Date:    2018/9/29
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class BaseViewDownloadGame(TestsuiteNormal):
    def setup(self):
        DUT.Common.reset_app()
        DUT.device.start_log()
        self.load_data(os.path.join(os.path.dirname(__file__), "BaseDownloadGame.xml"))  # 加载用例数据文件
        DUT.Common.uninstall_app(app_pkg=self.data.game_app_name)

    def test(self):
        assert_true(DUT.Common.base_search_and_play_video(self.data.video_name), target=DUT)
        assert_true(DUT.Common.base_video_ad_view_download_game(), target=DUT)
        DUT.Common.uninstall_app(app_pkg=self.data.game_app_name)
        DUT.Common.back_page()
        time.sleep(1)

    def teardown(self):
        DUT.device.stop_log()
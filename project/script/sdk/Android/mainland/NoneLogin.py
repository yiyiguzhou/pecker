"""
File Name:      NoneLogin
Author:         xuxiaofang_sx
Create Date:    2018/7/26
"""

import time
from project.script.testsuite.TestsuiteNormal import *


class NoneLogin(TestsuiteNormal):
    """
        用例描述：
        预制条件：
        """
    def setup(self):
        DUT.device.start_log()
        DUT.Mainland.start_ipecker_app()
        DUT.Mainland.reset_app()


    def test(self):
        # assert_true(DUT.Mainland.clear_buff_data(), "手机缓存清理", target=DUT)
        assert_true(DUT.Mainland.login(), "登录页面", target=DUT)
        assert_true(DUT.Mainland.No_login(self.data.title), "手机号注册页面显示成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
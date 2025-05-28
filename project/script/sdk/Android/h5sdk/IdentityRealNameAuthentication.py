"""
File Name:      IdentityRealNameAuthentication
Author:         xuxiaofang_sx
Create Date:    2018/8/20
"""

import time
from project.script.testsuite.TestsuiteNormal import *

class IdentityRealNameAuthentication(TestsuiteNormal):
    """
        用例描述：身份实名认证
        预制条件：1.该账号身份认证过
                  2.该账号未身份认证过
                  title:进入小游戏页面标题
                  name：身份证姓名
                  idcard：身份证号码
        """
    def setup(self):
        DUT.device.start_log()
        DUT.H5sdk.start_ipecker_app()
        DUT.H5sdk.reset_app()

    def test(self):
        assert_true(DUT.H5sdk.into_game_center(), "进入游戏中心", target=DUT)
        assert_true(DUT.H5sdk.into_mygame_page(self.data.title), "成功进入爱奇艺小游戏", target=DUT)
        time.sleep(5)
        assert_true(DUT.H5sdk.coin(), "成功进入小游戏", target=DUT)
        time.sleep(5)
        assert_true(DUT.H5sdk.identity_name_authentication(self.data.name,self.data.id_card), "身份实名认证成功", target=DUT)

    def teardown(self):
        DUT.device.stop_log()
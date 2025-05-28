# -*- coding: UTF-8 -*-

"""
File Name:      001_androidh5_cachelogin
Author:         fuhongzi
Create Date:    2018/5/10
"""
import time
import random
from project.script.testsuite.TestsuiteNormal import *


class androidh5_002_baselogin(TestsuiteNormal):

    def setup(self):
        DUT.device.start_logcat()

    def test(self):
        #assert_true(DUT.h5sdk.no_cache())
        #assert_true(DUT.h5sdk.gamecenter_search('决战沙城h5'))
        #assert_true(DUT.h5sdk.into_game('决战沙城h5'))
        #assert_true(DUT.h5sdk.into_h5game('决战沙城h5'))
        assert_true(DUT.h5sdk.common_account_login('苍穹破', 'xu175444'))

    def teardown(self):
        DUT.device.stop_logcat()
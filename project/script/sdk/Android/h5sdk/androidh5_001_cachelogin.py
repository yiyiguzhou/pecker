# -*- coding: UTF-8 -*-

"""
File Name:      001_androidh5_cachelogin
Author:         fuhongzi
Create Date:    2018/5/9
"""
import time
import random
from project.script.testsuite.TestsuiteNormal import *


class androidh5_001_cachelogin(TestsuiteNormal):

    def setup(self):
        DUT.device.start_logcat()

    def test(self):
        assert_true(DUT.h5sdk.no_cache())
        assert_true(DUT.h5sdk.gamecenter_search('决战沙城H5'))
        assert_true(DUT.h5sdk.into_gamedetail('决战沙城H5'))
        assert_true(DUT.h5sdk.into_h5game('决战沙城H5'))
        assert_true(DUT.h5sdk.guest_login('决战沙城H5'))

    def teardown(self):
        DUT.device.stop_logcat()

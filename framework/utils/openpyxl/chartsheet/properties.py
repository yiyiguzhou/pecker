from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

from framework.utils.openpyxl.descriptors import (
    Bool,
    String,
    Typed
)
from framework.utils.openpyxl.descriptors.serialisable import Serialisable
from framework.utils.openpyxl.styles import Color


class ChartsheetProperties(Serialisable):
    tagname = "sheetPr"

    published = Bool(allow_none=True)
    codeName = String(allow_none=True)
    tabColor = Typed(expected_type=Color, allow_none=True)

    __elements__ = ('tabColor',)

    def __init__(self,
                 published=None,
                 codeName=None,
                 tabColor=None,
                 ):
        self.published = published
        self.codeName = codeName
        self.tabColor = tabColor

from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

from framework.utils.openpyxl.descriptors.serialisable import Serialisable
from framework.utils.openpyxl.descriptors.excel import Relation


class Related(Serialisable):

    id = Relation()


    def __init__(self, id=None):
        self.id = id


    def to_tree(self, tagname, idx=None):
        return super(Related, self).to_tree(tagname)

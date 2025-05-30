from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

"""Write the shared string table."""
from io import BytesIO

# package imports
from framework.utils.openpyxl.xml.constants import SHEET_MAIN_NS
from framework.utils.openpyxl.xml.functions import Element, xmlfile, SubElement

PRESERVE_SPACE = '{%s}space' % "http://www.w3.org/XML/1998/namespace"

def write_string_table(string_table):
    """Write the string table xml."""
    out = BytesIO()

    with xmlfile(out) as xf:
        with xf.element("sst", xmlns=SHEET_MAIN_NS, uniqueCount="%d" % len(string_table)):

            for key in string_table:
                el = Element('si')
                text = SubElement(el, 't')
                text.text = key
                if key.strip() != key:
                    text.set(PRESERVE_SPACE, 'preserve')
                xf.write(el)

    return  out.getvalue()

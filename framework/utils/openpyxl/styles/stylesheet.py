from framework.utils.openpyxl.descriptors.serialisable import Serialisable
from framework.utils.openpyxl.descriptors import (
    Alias,
    Typed,
    Sequence
)
from framework.utils.openpyxl.descriptors.sequence import NestedSequence
from framework.utils.openpyxl.descriptors.excel import ExtensionList
from framework.utils.openpyxl.utils.indexed_list import IndexedList
from framework.utils.openpyxl.xml.constants import ARC_STYLE, SHEET_MAIN_NS
from framework.utils.openpyxl.xml.functions import fromstring

from .colors import ColorList, COLOR_INDEX
from .differential import DifferentialStyle
from .table import TableStyleList
from .borders import Border
from .fills import Fill
from .fonts import Font
from .numbers import (
    NumberFormatList,
    BUILTIN_FORMATS,
    BUILTIN_FORMATS_REVERSE
)
from .alignment import Alignment
from .protection import Protection
from .named_styles import (
    NamedStyle,
    _NamedCellStyle,
    _NamedCellStyleList
)
from .cell_style import CellStyle, CellStyleList


class Stylesheet(Serialisable):

    tagname = "styleSheet"

    numFmts = Typed(expected_type=NumberFormatList)
    fonts = NestedSequence(expected_type=Font, count=True)
    fills = NestedSequence(expected_type=Fill, count=True)
    borders = NestedSequence(expected_type=Border, count=True)
    cellStyleXfs = Typed(expected_type=CellStyleList)
    cellXfs = Typed(expected_type=CellStyleList)
    cellStyles = Typed(expected_type=_NamedCellStyleList)
    dxfs = NestedSequence(expected_type=DifferentialStyle, count=True)
    tableStyles = Typed(expected_type=TableStyleList, allow_none=True)
    colors = Typed(expected_type=ColorList, allow_none=True)
    extLst = Typed(expected_type=ExtensionList, allow_none=True)

    __elements__ = ('numFmts', 'fonts', 'fills', 'borders', 'cellStyleXfs',
                    'cellXfs', 'cellStyles', 'dxfs', 'tableStyles', 'colors')

    def __init__(self,
                 numFmts=None,
                 fonts=(),
                 fills=(),
                 borders=(),
                 cellStyleXfs=None,
                 cellXfs=None,
                 cellStyles=None,
                 dxfs=(),
                 tableStyles=None,
                 colors=None,
                 extLst=None,
                ):
        if numFmts is None:
            numFmts = NumberFormatList()
        self.numFmts = numFmts
        self.number_formats = IndexedList()
        self.fonts = fonts
        self.fills = fills
        self.borders = borders
        if cellStyleXfs is None:
            cellStyleXfs = CellStyleList()
        self.cellStyleXfs = cellStyleXfs
        if cellXfs is None:
            cellXfs = CellStyleList()
        self.cellXfs = cellXfs
        if cellStyles is None:
            cellStyles = _NamedCellStyleList()
        self.cellStyles = cellStyles

        self.dxfs = dxfs
        self.tableStyles = tableStyles
        self.colors = colors

        self.cell_styles = self.cellXfs._to_array()
        self.alignments = self.cellXfs.alignments
        self.protections = self.cellXfs.prots
        self._normalise_numbers()
        self.named_styles = self._merge_named_styles()


    @classmethod
    def from_tree(cls, node):
        # strip all attribs
        attrs = dict(node.attrib)
        for k in attrs:
            del node.attrib[k]
        return super(Stylesheet, cls).from_tree(node)


    def _merge_named_styles(self):
        """
        Merge named style names "cellStyles" with their associated styles
        "cellStyleXfs"
        """
        named_styles = self.cellStyles.names

        for style in named_styles:
            self._expand_named_style(style)

        return named_styles


    def _expand_named_style(self, named_style):
        """
        Bind format definitions for a named style from the associated style
        record
        """
        xf = self.cellStyleXfs[named_style.xfId]
        named_style.font = self.fonts[xf.fontId]
        named_style.fill = self.fills[xf.fillId]
        named_style.border = self.borders[xf.borderId]
        if xf.numFmtId in self.custom_formats:
            named_style.number_format = self.custom_formats[xf.numFmtId]
        if xf.alignment:
            named_style.alignment = xf.alignment
        if xf.protection:
            named_style.protection = xf.protection


    def _split_named_styles(self, wb):
        """
        Convert NamedStyle into separate CellStyle and Xf objects
        """
        for style in wb._named_styles:
            self.cellStyles.cellStyle.append(style.as_name())
            self.cellStyleXfs.xf.append(style.as_xf())


    @property
    def custom_formats(self):
        return dict([(n.numFmtId, n.formatCode) for n in self.numFmts.numFmt])


    def _normalise_numbers(self):
        """
        Rebase numFmtIds with a floor of 164
        """
        custom = self.custom_formats
        formats = self.number_formats
        for style in self.cell_styles:
            if style.numFmtId in custom:
                fmt = custom[style.numFmtId]
                if fmt in BUILTIN_FORMATS_REVERSE: # remove builtins
                    style.numFmtId = BUILTIN_FORMATS_REVERSE[fmt]
                    continue
                style.numFmtId = formats.add(fmt) + 164


    def to_tree(self, tagname=None, idx=None, namespace=None):
        tree = super(Stylesheet, self).to_tree(tagname, idx, namespace)
        tree.set("xmlns", SHEET_MAIN_NS)
        return tree


def apply_stylesheet(archive, wb):
    """
    Add styles to workbook if present
    """
    try:
        src = archive.read(ARC_STYLE)
    except KeyError:
        return wb

    node = fromstring(src)
    stylesheet = Stylesheet.from_tree(node)

    wb._borders = IndexedList(stylesheet.borders)
    wb._fonts = IndexedList(stylesheet.fonts)
    wb._fills = IndexedList(stylesheet.fills)
    wb._differential_styles.styles = stylesheet.dxfs
    wb._number_formats = stylesheet.number_formats
    wb._protections = stylesheet.protections
    wb._alignments = stylesheet.alignments
    wb._table_styles = stylesheet.tableStyles

    # need to overwrite openpyxl defaults in case workbook has different ones
    wb._cell_styles = stylesheet.cell_styles
    wb._named_styles = stylesheet.named_styles

    for ns in wb._named_styles:
        ns.bind(wb)

    if stylesheet.colors is not None:
        wb._colors = stylesheet.colors.index


def write_stylesheet(wb):
    stylesheet = Stylesheet()
    stylesheet.fonts = wb._fonts
    stylesheet.fills = wb._fills
    stylesheet.borders = wb._borders
    stylesheet.dxfs = wb._differential_styles.styles

    from .numbers import NumberFormat
    fmts = []
    for idx, code in enumerate(wb._number_formats, 164):
        fmt = NumberFormat(idx, code)
        fmts.append(fmt)

    stylesheet.numFmts.numFmt = fmts

    xfs = []
    for style in wb._cell_styles:
        xf = CellStyle.from_array(style)

        if style.alignmentId:
            xf.alignment = wb._alignments[style.alignmentId]

        if style.protectionId:
            xf.protection = wb._protections[style.protectionId]
        xfs.append(xf)
    stylesheet.cellXfs = CellStyleList(xf=xfs)

    stylesheet._split_named_styles(wb)
    stylesheet.tableStyles = wb._table_styles

    return stylesheet.to_tree()

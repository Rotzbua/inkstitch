# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import NSS, Boolean, errormsg

from ..elements import FillStitch, Stroke
from ..i18n import _
from .base import InkstitchExtension


class Cleanup(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-f", "--rm_fill", dest="rm_fill", type=Boolean, default=True)
        self.arg_parser.add_argument("-s", "--rm_stroke", dest="rm_stroke", type=Boolean, default=True)
        self.arg_parser.add_argument("-a", "--fill_threshold", dest="fill_threshold", type=int, default=20)
        self.arg_parser.add_argument("-l", "--stroke_threshold", dest="stroke_threshold", type=int, default=5)

    def effect(self):
        self.rm_fill = self.options.rm_fill
        self.rm_stroke = self.options.rm_stroke
        self.fill_threshold = self.options.fill_threshold
        self.stroke_threshold = self.options.stroke_threshold

        self.svg.selection.clear()

        count = 0
        svg = self.document.getroot()
        empty_d_objects = svg.xpath(".//svg:path[@d='' or not(@d)]", namespaces=NSS)
        for empty in empty_d_objects:
            empty.getparent().remove(empty)
            count += 1

        if not self.get_elements():
            errormsg(_("%s elements removed" % count))
            return

        for element in self.elements:
            if (isinstance(element, FillStitch) and self.rm_fill and element.shape.area < self.fill_threshold):
                element.node.getparent().remove(element.node)
                count += 1
            if (isinstance(element, Stroke) and self.rm_stroke and
               element.shape.length < self.stroke_threshold and element.node.getparent() is not None):
                element.node.getparent().remove(element.node)
                count += 1

        errormsg(_("%s elements removed" % count))

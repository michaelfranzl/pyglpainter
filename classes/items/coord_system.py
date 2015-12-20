"""
pyglpainter - Copyright (c) 2015 Michael Franzl

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from OpenGL.GL import (GL_LINES)

from .item import Item


class CoordSystem(Item):
    """
    Draws a classical XYZ coordinate system with axis X as red, Y as green
    and Z as blue. Length of axes is 1.
    """

    def __init__(self, label, prog_id, origin=(0, 0, 0), scale=10,
                 linewidth=1):
        """
        @param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @param origin
        Origin of this item in world space.

        @param scale
        Scale of this item in world space.

        @param linewidth
        Width of rendered lines in pixels.
        """

        vertex_count = 6
        super(CoordSystem, self).__init__(label, prog_id, GL_LINES,
                                          linewidth, origin, scale, False,
                                          vertex_count)

        self.append_vertices([[(0, 0, 0), (.6, .0, .0, 1.0)]])
        self.append_vertices([[(1, 0, 0), (.6, .0, .0, 1.0)]])
        self.append_vertices([[(0, 0, 0), (.0, .6, .0, 1.0)]])
        self.append_vertices([[(0, 1, 0), (.0, .6, .0, 1.0)]])
        self.append_vertices([[(0, 0, 0), (.0, .0, .6, 1.0)]])
        self.append_vertices([[(0, 0, 1), (.0, .0, .6, 1.0)]])

        self.upload()

    def highlight(self, val):
        """
        Visually highlight this coordinate system.

        Create a gradient towards white, towards the center

        @val
        True or False
        """

        for x in range(0, 3):
            if val is True:
                newcol = (1, 1, 1, 1)
            else:
                newcol = (0, 0, 0, 1)

            self.vdata_pos_col["color"][x * 2] = newcol

        self.upload()
        self.dirty = True

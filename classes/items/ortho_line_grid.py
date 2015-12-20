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


class OrthoLineGrid(Item):
    """
    Draws a 2-dimensional grid from individual lines useful for
    coordinate systems or visualization of a 'ground'.

    It can not be filled.
    """

    def __init__(self, label, prog,
                 lower_left, upper_right, unit,
                 origin=(0, 0, 0), scale=1, linewidth=1, color=(1, 1, 1, 0.2)):
        """
        @param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @param lower_left
        Lower left corner in local coordinates.

        @param upper_right
        Upper right corner in local coordinates.

        @param unit
        At which intervals to draw a line.

        @param origin
        Origin of this item in world space.

        @param scale
        Scale of this item in world space.

        @param linewidth
        Width of rendered lines in pixels.

        @param color
        Color of this item.
        """

        width = upper_right[0] - lower_left[0]
        height = upper_right[1] - lower_left[1]

        width_units = int(width / unit) + 1
        height_units = int(height / unit) + 1

        vertex_count = 2 * width_units + 2 * height_units

        super(OrthoLineGrid, self).__init__(label, prog, GL_LINES,
                                            linewidth, origin, scale, False,
                                            vertex_count)

        for wu in range(0, width_units):
            x = unit * wu
            self.append_vertices([[(x, 0, 0), color]])
            self.append_vertices([[(x, height, 0), color]])

        for hu in range(0, height_units):
            y = unit * hu
            self.append_vertices([[(0, y, 0), color]])
            self.append_vertices([[(width, y, 0), color]])

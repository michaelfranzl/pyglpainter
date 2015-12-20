"""
pyglpainter - Minimalistic, modern OpenGL drawing for technical applications
Copyright (C) 2015 Michael Franzl

This file is part of pyglpainter.

pyglpainter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyglpainter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyglpainter. If not, see <https://www.gnu.org/licenses/>.
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

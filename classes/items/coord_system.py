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

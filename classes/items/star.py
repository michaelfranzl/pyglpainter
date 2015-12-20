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

from OpenGL.GL import GL_LINES

from .item import Item


class Star(Item):
    """
    Draws a simple 3-dimensional cross with 'ray' length of 1, which
    appears as a star when viewed from a non-orthogonal direction.
    """

    def __init__(self, label, prog_id, origin=(0, 0, 0), scale=1, linewidth=1,
                 color=(1, 1, .5, 1)):
        """
        @param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @param text
        Text to be rendered. An 8-bit ASCII string.

        @param origin
        Origin of this item in world space.

        @param scale
        Scale of this item in world space.

        @param linewidth
        Width of rendered lines in pixels.

        @param color
        Color of this item.
        """
        vertex_count = 6
        super(Star, self).__init__(label, prog_id, GL_LINES,
                                   linewidth, origin, scale, False,
                                   vertex_count)

        self.append_vertices([[(-.5, 0, 0), color]])
        self.append_vertices([[(1, 0, 0), color]])
        self.append_vertices([[(0, -.5, 0), color]])
        self.append_vertices([[(0, .5, 0), color]])
        self.append_vertices([[(0, 0, -.5), color]])
        self.append_vertices([[(0, 0, .5), color]])

        self.upload()

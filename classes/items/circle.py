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

from .arc import Arc


class Circle(Arc):
    """
    Draws a circle.
    """

    def __init__(self, label, prog_id, radius, use_triangles, filled,
                 origin=(0, 0, 0), scale=1, linewidth=1, color=(1, .5, .5, 1)):
        """
        @param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @radius
        The radius of the circle in local units.

        @param use_triangles
        Set to True to draw a fillable circle wedge.
        When False, draw the arc as 1D lines, not fillable.

        @param filled
        Set to True to fill the circle wedge. `use_triangles` must be True
        for this to have an effect.

        @param origin
        Origin of this item in world space.

        @param scale
        Scale of this item in world space.

        @param linewidth
        Width of rendered lines in pixels.

        @param color
        Color of this item.
        """

        start = (-radius, 0, 0)
        end = start
        offset = (radius, 0, 0)

        super(Circle, self).__init__(label, prog_id, start, end, offset,
                                     radius, True, use_triangles, filled,
                                     origin, scale, linewidth, color)

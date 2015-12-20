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

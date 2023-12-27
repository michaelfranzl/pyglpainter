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

from OpenGL.GL import GL_TRIANGLES

from .item import Item
from .fonts import font_dutch_blunt as font


class Text(Item):
    """
    Renders vector text with a triangle-only font. See font_dutch_blunt.py
    for more information.
    """

    def __init__(self, label, prog_id, text, origin=(0, 0, 0), scale=1,
                 linewidth=1, color=(1, 1, 1, 0.5)):
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

        # calculate the number of needed vertices
        vertexcount_total = 0

        for char in text:
            j = ord(char)
            vertexcount_total += font.sizes[j]

        super(Text, self).__init__(label, prog_id, GL_TRIANGLES,
                                   linewidth, origin, scale, True,
                                   vertexcount_total)

        self.render(text, color)
        self.upload()

    def render(self, text, color):
        """
        Reads vertex coordinates and appends vertices with a simple
        typesetting algorithm.

        @param text
        Text to be rendered. An 8-bit ASCII string.

        @param color
        Color of the text.
        """

        letterpos = 0
        letterspacing = 0.5
        linepos = 0
        linespacing = 6

        for char in text:
            j = ord(char)

            if char == "\n":
                # start a new line
                linepos -= linespacing
                letterpos = 0

                continue

            vertexcount = font.sizes[j] * 2
            offset = font.vdataoffsets[j] * 2

            for i in range(offset, offset + vertexcount, 2):
                x = font.vdata[i]
                y = font.vdata[i + 1]
                w = font.widths[j]
                x += letterpos
                y += linepos
                self.append_vertices([[(x, y, 0), color]])

            letterpos += w
            letterpos += letterspacing

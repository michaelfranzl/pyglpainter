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

import OpenGL
from OpenGL.GL import (GL_TRIANGLE_STRIP)

import numpy as np

from .item import Item


class HeightMap(Item):
    """
    WIP
    """

    def __init__(self, label, prog,
                 nodes_x, nodes_y, pos_col, fill,
                 origin=(0, 0, 0), scale=1, linewidth=1, color=(1, 1, 1, 0.2)):
        """
        @param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @param positions
        List of 3-tuples of node positions

        @param origin
        Origin of this item in world space.

        @param scale
        Scale of this item in world space.

        @param linewidth
        Width of rendered lines in pixels.

        @param color
        Color of this item.
        """

        self.nodes_x = nodes_x
        self.nodes_y = nodes_y

        self.vdata_indices = self.calculate_indices()

        super(HeightMap, self).__init__(label, prog,
                                        GL_TRIANGLE_STRIP, linewidth, origin,
                                        scale, fill)

        self.set_data(pos_col)

    def set_data(self, pos_col):
        height_max_idx = pos_col["position"].argmax(axis=0)[2]
        height_min_idx = pos_col["position"].argmin(axis=0)[2]
        height_max = pos_col["position"][height_max_idx][2]
        height_min = pos_col["position"][height_min_idx][2]
        self.uniforms = {
            "height_max": [height_max],
            "height_min": [height_min],
        }

        self.vdata_pos_col = pos_col
        self.vertexcount = pos_col.size

    def draw(self, mat_v_inverted):
        super(HeightMap, self).draw(mat_v_inverted)

    def calculate_indices(self):
        nx = self.nodes_x
        ny = self.nodes_y

        size = 1 + 2 * (nx - 1) * (ny - 1) + 2 * (ny - 1)
        vdata_indices = np.zeros(size, dtype=OpenGL.constants.GLuint)

        j = 1  # start with one, first index always zero
        d = 1  # right direction

        for y in range(0, ny - 1):

            if d == 1:
                r = range(0, nx - 1)
            else:
                r = range(nx - 1, 0, -1)

            for x in r:
                vdata_indices[j] = (y + 1) * nx + x
                j += 1
                vdata_indices[j] = y * nx + x + d
                j += 1

            if d == 1:
                # make a degenerate triangle to finish this row
                vdata_indices[j] = (y + 2) * nx - 1
                j += 1
                vdata_indices[j] = (y + 2) * nx - 1
                j += 1
            else:
                # make a degenerate triangle to finish this row
                vdata_indices[j] = (y + 1) * nx
                j += 1
                vdata_indices[j] = (y + 1) * nx
                j += 1

            d *= -1

        return vdata_indices

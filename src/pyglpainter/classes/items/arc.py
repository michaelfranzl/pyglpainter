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

import math
import numpy as np
from OpenGL.GL import GL_TRIANGLE_FAN, GL_LINE_STRIP

from .item import Item


class Arc(Item):
    """
    Renders a circular arc or circle segment in the XY plane
    by approximating it with line segments. Helix arcs along the Z axis
    are supported.

    The initialization function defines an arc by start, end, and offset
    of the center relative to start. This actually over-defines a circular
    arc, so the user is responsible to do the correct 2D geometry math
    themselves.

    If start, end, and offset don't describe a circular arc, a warning is
    output, and the drawn result may be wrong.

    To simply draw a circle, use the more convenient Circle class instead.
    """

    def __init__(self, label, prog_id, start, end, offset, radius,
                 is_clockwise_arc, use_triangles, filled, origin=(0, 0, 0),
                 scale=1, linewidth=1, color=(1, .5, 1, 1)):
        """
        @param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @param start
        The xyz start coordinate of the arc in local coordinates. 3-tuple.

        @param end
        The xyz end coordinate of the arc in local coordinates. To draw a full
        circle, set identical to `start`. 3-tuple.

        @param offset
        The xyz offset of the center from the start point. 3-tuple.

        @param radius
        The radius of the arc. Only used to calculate the number of
        line segments to generate. The arc is fully defined by `start`,
        `end`, and `offset`.

        @param is_clockwise_arc
        There are two directions to draw an arc from `start` to `end`.
        Set to True if the arc should be drawn clockwise, otherwise False.

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

        positions = self.render(list(start), end, offset,
                                radius, 0, 1, 2, is_clockwise_arc)
        vertex_count = len(positions) + 1

        if use_triangles:
            primitive_type = GL_TRIANGLE_FAN
        else:
            primitive_type = GL_LINE_STRIP

        super(Arc, self).__init__(label, prog_id, primitive_type,
                                  linewidth, origin, scale, filled,
                                  vertex_count)

        if use_triangles:
            center = np.add(start, offset)
            self.append_vertices([[center, color]])

        for pos in positions:
            self.append_vertices([[pos, color]])

        self.upload()

    def render(self, position, target, offset, radius, axis_0, axis_1,
               axis_linear, is_clockwise_arc):
        """
        This function is a direct port of Grbl's C code into Python
        (motion_control.c) with slight refactoring for Python by Michael
        Franzl.  This function is copyright (c) Sungeun K. Jeon under GNU
        General Public License 3
        """

        center_axis0 = position[axis_0] + offset[axis_0]
        center_axis1 = position[axis_1] + offset[axis_1]
        # radius vector from center to current location
        r_axis0 = -offset[axis_0]
        r_axis1 = -offset[axis_1]
        # radius vector from target to center
        rt_axis0 = target[axis_0] - center_axis0
        rt_axis1 = target[axis_1] - center_axis1

        angular_travel = math.atan2(
            r_axis0 * rt_axis1 - r_axis1 * rt_axis0, r_axis0 * rt_axis0 +
            r_axis1 * rt_axis1)

        arc_tolerance = 0.004
        arc_angular_travel_epsilon = 0.0000005

        if is_clockwise_arc:  # Correct atan2 output per direction
            if angular_travel >= -arc_angular_travel_epsilon:
                angular_travel -= 2*math.pi
        else:
            if angular_travel <= arc_angular_travel_epsilon:
                angular_travel += 2*math.pi

        segments = math.floor(
            math.fabs(0.5 * angular_travel * radius) /
            math.sqrt(arc_tolerance * (2 * radius - arc_tolerance))
        )

        positions = []
        positions.append(tuple(position))

        if segments:
            theta_per_segment = angular_travel / segments
            linear_per_segment = (
                target[axis_linear] - position[axis_linear]) / segments

            for i in range(1, segments):
                cos_Ti = math.cos(i * theta_per_segment)
                sin_Ti = math.sin(i * theta_per_segment)
                r_axis0 = -offset[axis_0] * cos_Ti + offset[axis_1] * sin_Ti
                r_axis1 = -offset[axis_0] * sin_Ti - offset[axis_1] * cos_Ti

                position[axis_0] = center_axis0 + r_axis0
                position[axis_1] = center_axis1 + r_axis1
                position[axis_linear] += linear_per_segment

                positions.append(tuple(position))

        # make sure we arrive at target
        positions.append(tuple(target))

        return positions

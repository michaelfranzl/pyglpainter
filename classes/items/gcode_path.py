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

import numpy as np
from OpenGL.GL import (glBindBuffer, glBufferSubData, GL_LINE_STRIP,
                       GL_ARRAY_BUFFER)

from gcode_machine.gcode_machine import GcodeMachine
from .item import Item


class GcodePath(Item):
    """
    Plot the path laid out by G-Code commands for CNC machines.

    Supports G0, G1, G2, G3, G90, G91, and G54-G59.

    G2 and G3 arcs are approximated by line segments. Different motion
    modes are drawn with different colors for better visualization.
    """

    def __init__(self, label, prog_id, gcode_list, cmpos, ccs, cs_offsets,
                 do_fractionize_arcs=True):
        """
        param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @param gcode_list
        A Python list of strings of G-codes that will be plotted.

        @param cmpos
        Current machine position. G-Codes imply a state machine knowing
        its position. This is the initial position of the state machine.
        A 3-tuple of global coordinates.

        @param ccs
        Current coordinate system. G-Codes imply a state machine knowing
        its current coordinate system. This is the initial coordinate system
        name of the state machine. It is an integer in the range from
        4..9 (corresponding to G54-G59). `ccs` must be a key in `cs_offsets`.

        @param cs_offsets
        Coordinate system offsets. A Python dict with
        3-tuples as offsets. Keys must correspond to the range of `ccs`.
        When a G54-G59 change coordinate system command is encountered,
        the position for the next movement command will be relative to the
        selected offset. This emulates the movement behavior of a classical
        CNC machine.

        @param do_fractionize_arcs
        If True, break circular arcs into tiny lines.
        False gives speed improvement.
        """

        super(GcodePath, self).__init__(label, prog_id, GL_LINE_STRIP, 2)

        self.machine = GcodeMachine(cmpos, ccs, cs_offsets)

        # OpenGL doesn't have a notion about arcs
        self.machine.do_fractionize_arcs = do_fractionize_arcs
        self.machine.do_fractionize_lines = False

        self.machine.special_comment_prefix = "_sim"

        self._lines_to_highlight = []  # line segments can be highlighted

        self.gcode = []

        if do_fractionize_arcs is True:
            for line in gcode_list:
                self.machine.set_line(line)
                self.machine.parse_state()
                lines = self.machine.fractionize()

                self.gcode += lines
                self.machine.done()
        else:
            self.gcode = gcode_list

        # reset, we re-run in render()
        self.machine.reset()
        self.machine.position_m = cmpos
        self.machine.current_cs = ccs

        self.set_vertexcount_max(2 * len(self.gcode) + 1)

        self.render()
        self.upload()

    def highlight_line(self, line_number):
        """
        Remember which lines to highlight.

        The color of a highlighted line will be substituted directly on
        the GPU. Substitution will happen during the next `draw()`
        call which is why this function is very efficient, and can be
        called from threads.
        """
        self._lines_to_highlight.append(line_number)
        pass

    def draw(self, mat_v_inverted):
        for line_number in self._lines_to_highlight:
            if 2 * line_number > self.vertexcount:
                continue

            # Substitute color of highlighted lines directly in the GPU.
            stride = self.vdata_pos_col.strides[0]
            position_size = self.vdata_pos_col.dtype["position"].itemsize
            color_size = self.vdata_pos_col.dtype["color"].itemsize

            # 2 opengl segments for each logical line, see below
            offset = 2 * line_number * stride + position_size

            col = np.array([1, 0.5, 1, 1], dtype=np.float32)

            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_array)
            glBufferSubData(GL_ARRAY_BUFFER, offset, color_size, col)

        del self._lines_to_highlight[:]

        super(GcodePath, self).draw(mat_v_inverted)

    def render(self):
        """
        Appends vertices corresponding to the path traveled by G-Code.

        This emulates the state machine of a CNC machine. The color
        of drawn paths is taken from a special comment environment
        `_gcm.color_begin` and `_gcm.color_end`. If color is not
        set via comments, default colors are taken from the motion mode.

        This method only supports G0 and G1 linear motion. Use a
        Gcode processor to break arcs down into lines.
        """

        colors = {
            0: (.5, .5, .5),
            1: (.7, .7, 1),
            2: (.8, .7, 1),
            3: (.7, .8, 1),
            None: (0, 0, 0),
        }
        col = colors[0]  # initial color

        # create vertex at start of path
        self.append_vertices(
            [[self.machine.position_m, (col[0], col[1], col[2], 1)]])

        arc_mode = False
        arc_by_sim = False
        arc_count = 0

        for line in self.gcode:
            self.machine.set_line(line)
            self.machine.parse_state()

            if "arc_begin[G02" in line:
                arc_mode = 2

                if "_sim" in line:
                    arc_by_sim = True
                arc_count += 1
            elif "arc_begin[G03" in line:
                arc_mode = 3

                if "_sim" in line:
                    arc_by_sim = True
                arc_count += 1
            elif "arc_end" in line:
                arc_mode = False

            if arc_mode is False:
                motion_mode = self.machine.current_motion_mode
            else:
                motion_mode = arc_mode

            col = colors[motion_mode]

            ss = self.machine.current_spindle_speed

            if arc_mode is False:
                color1 = (col[0], col[1], col[2], 1)

                if ss is None:
                    color2 = (col[0], col[1], col[2], 0.3)
                else:
                    color2 = (ss/255, ss/255, ss/255, 1)

            else:
                if arc_count % 2 == 0:
                    color1 = (col[0], col[1], col[2], 0.8)
                else:
                    color1 = (col[0], col[1], col[2], 1)

                if arc_by_sim is True:
                    color2 = color1  # continuous arc
                else:
                    color2 = (col[0], col[1], col[2], 0.5)

            if ss is not None:
                color2 = (ss/255, ss/255, ss/255, 1)

            # draw two gl line segments per gcode line for better visualization
            # of commands
            diff = np.subtract(self.machine.target_m, self.machine.position_m)

            self.append_vertices(
                [[self.machine.position_m + diff * 0.001, color1]])
            self.append_vertices([[self.machine.target_m, color2]])

            self.machine.done()

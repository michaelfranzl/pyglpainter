#!/usr/bin/env python3

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

import os
import random
import sys
import math

from PyQt5.QtWidgets import QApplication

import numpy as np

from OpenGL.GL import GL_LINE_STRIP, GL_LINES, GL_TRIANGLE_STRIP, GL_TRIANGLES

from mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    p = window.painter

    # ============= CREATE PROGRAMS BEGIN =============
    path = os.path.dirname(os.path.realpath(__file__)) + "/shaders/"
    opts = {
        "uniforms": {
            "mat_m": "Matrix4fv",
            "mat_v": "Matrix4fv",
            "mat_p": "Matrix4fv",
        },
        "attributes": {
            "color": "vec4",
            "position": "vec3",
        }
    }
    p.program_create("simple3d", path + "simple3d-vertex.c",
                     path + "simple3d-fragment.c", opts)

    opts = {
        "uniforms": {
            "mat_m": "Matrix4fv",
        },
        "attributes": {
            "color": "vec4",
            "position": "vec3",
        }
    }
    p.program_create("simple2d", path + "simple2d-vertex.c",
                     path + "simple2d-fragment.c", opts)

    opts = {
        "uniforms": {
            "mat_m": "Matrix4fv",
            "mat_v": "Matrix4fv",
            "mat_p": "Matrix4fv",
            "height_min": "1f",
            "height_max": "1f",
        },
        "attributes": {
            "position": "vec3",
        }
    }
    p.program_create("heightmap", path + "heightmap-vertex.c",
                     path + "heightmap-fragment.c", opts)
    # ============= CREATE PROGRAMS END =============

    # ============= CREATE COMPOUND PRIMITIVES BEGIN =============

    # create a "ground" for better orientation
    p.item_create("OrthoLineGrid", "mygrid1",
                  "simple3d", (0, 0), (1000, 1000), 10)

    # Create static 2D overlay text at bottom left corder of window
    i = p.item_create("Text", "mytext2", "simple2d",
                      "pyglpainter (c) 2015 Michael Franzl",
                      (-0.95, -0.95, 0), 0.01)

    # create the main coordinate system with label
    p.item_create("CoordSystem", "mycs1", "simple3d", (0, 0, 0), 100, 4)

    mycs2 = p.item_create("CoordSystem", "mycs2",
                          "simple3d", (100, 300, 0), 50, 2)
    mycs2.highlight(True)
    i = p.item_create("Text", "mycslabel", "simple3d",
                      "class CoordSystem", (0, 0, 0), 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # draw a random cloud of stars with label
    i = p.item_create("Text", "mystarlabel", "simple3d",
                      "class Star", (60, 60, 60), 1, 1, (1, 1, 1, 1))
    i.billboard = True

    for i in range(0, 50):
        x = random.randint(50, 80)
        y = random.randint(50, 80)
        z = random.randint(50, 80)
        s = random.randint(1, 12)
        p.item_create("Star", "mystar%d" % i, "simple3d", (x, y, z), s)

    # Draw a 3D circular arc, aka. Helix
    is_clockwise = True
    use_triangles = True
    filled = False
    i = p.item_create("Arc", "myarc1", "simple3d", (-1, 0, 0), (-1, 0, 2),
                      (1, 0, 1), 1, is_clockwise, use_triangles, filled,
                      (100, 200, 0), 40)
    i = p.item_create("Text", "myarc1label", "simple3d",
                      "class Arc (helix)", i.origin_tuple, 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # Draw a filled circle wedge
    is_clockwise = True
    use_triangles = True
    filled = True
    i = p.item_create("Arc", "myarc2", "simple3d", (-1, 0, 0), (0.7, 0.7, 0),
                      (1, 0, 0), 1, is_clockwise, use_triangles, filled,
                      (200, 200, 0), 40)
    i = p.item_create("Text", "myarc2label", "simple3d",
                      "class Arc (circle wedge filled)", i.origin_tuple, 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # Draw an arc from 1D line segments
    is_clockwise = False
    use_triangles = True
    filled = False
    i = p.item_create("Arc", "myarc3", "simple3d", (-1, 0, 0), (0.7, 0.7, 0),
                      (1, 0, 0), 1, is_clockwise, use_triangles, filled,
                      (300, 200, 0), 40)
    i = p.item_create("Text", "myarc3label", "simple3d",
                      "class Arc (triangles)", i.origin_tuple, 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # Draw a circle made from 1D line segments
    is_clockwise = False
    use_triangles = False
    filled = False
    i = p.item_create("Circle", "mycircle1", "simple3d", 20,
                      use_triangles, filled, (400, 200, 0), 1, 2,
                      (.5, 1, 1, 1))
    i = p.item_create("Text", "mycircle1label", "simple3d",
                      "class Circle (non-filled)", i.origin_tuple, 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # Draw a circle made from 1D line segments
    is_clockwise = False
    use_triangles = True
    filled = True
    i = p.item_create("Circle", "mycircle2", "simple3d", 20,
                      use_triangles, filled, (500, 200, 0), 1, 2,
                      (.5, 1, 1, 1))
    i = p.item_create("Text", "mycircle2label", "simple3d",
                      "class Circle (filled)", i.origin_tuple, 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # Plot CNC G-code relative to mycs2 and put label
    gcodes = []
    gcodes.append("G0 X20 Y20")
    gcodes.append("G1 X30")
    gcodes.append("G1 X40")
    gcodes.append("G1 X50")
    gcodes.append("G2 X60 Y30 I5 J5")
    cs_offsets = {"G54": (10, 10, 0)}
    # note this: since no Z movement in Gcode, all is in plane of Z=10
    cmpos = (0, 0, 0)
    mygcode1 = p.item_create("GcodePath", "mygcode1",
                             "simple3d", gcodes, cmpos, "G54", cs_offsets)
    mygcode1.set_origin(mycs2.origin_tuple)

    i = p.item_create("Text", "mygcodelabel", "simple3d",
                      "class GcodePath", (0, 0, 0), 1)
    i.billboard = True
    i.billboard_axis = "Z"
    # ============= CREATE COMPOUND PRIMITIVES END =============

    # ============= CREATE RAW OPENGL PRIMITIVES BEGIN =============

    # Create an arbitrary line strip plus label
    vertexcount = 4
    i = p.item_create("Item", "mylinestrip1", "simple3d",
                      GL_LINE_STRIP, 1, (200, 300, 1), 5, False, vertexcount)
    color = (0.7, 0.2, 0.2, 1)
    i.append_vertices([[(0, 0, 0), color]])
    i.append_vertices([[(10, 0, 0), color]])
    i.append_vertices([[(0, 10, 0), color]])
    i.append_vertices([[(10, 10, 0), color]])
    i.upload()
    i = p.item_create("Text", "linestriplabel", "simple3d",
                      "class Item (GL_LINE_STRIP)", i.origin_tuple, 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # Create arbitrary lines plus label
    vertexcount = 4
    i = p.item_create("Item", "mylines2", "simple3d", GL_LINES,
                      1, (300, 300, 1), 5, False, vertexcount)
    color = (0.2, 0.7, 0.2, 1)
    i.append_vertices([[(0, 0, 0), color]])
    i.append_vertices([[(10, 0, 0), color]])
    i.append_vertices([[(0, 10, 0), color]])
    i.append_vertices([[(10, 10, 0), color]])
    i.upload()
    i = p.item_create("Text", "lineslabel", "simple3d",
                      "class Item (GL_LINES)", i.origin_tuple, 1)
    i.billboard = True
    i.billboard_axis = "Z"

    # Create a fully camera-aligned billboard plus label
    vertexcount = 4
    i = p.item_create("Item", "myquad1", "simple3d",
                      GL_TRIANGLE_STRIP, 1, (400, 0, 0), 1, False, vertexcount)
    i.billboard = True
    i.billboard_axis = None
    col = (0.2, 0.7, 0.2, 1)
    i.append_vertices([[(0, 0, 0), col]])
    i.append_vertices([[(0, 50, 0), col]])
    i.append_vertices([[(50, 0, 0), col]])
    i.append_vertices([[(50, 50, 0), col]])
    i.upload()
    i = p.item_create("Text", "billboardlabel1", "simple3d",
                      "class Item\n(Billboard fully\naligned)", i.origin_tuple,
                      2)
    i.billboard = True
    i.billboard_axis = None

    # Create a camera-aligned billboard restrained to rotation around Z axis
    vertexcount = 4
    i = p.item_create("Item", "myquad2", "simple3d",
                      GL_TRIANGLE_STRIP, 2, (400, 300, 0), 1, False,
                      vertexcount)
    i.billboard = True
    i.billboard_axis = "Z"
    col = (0.7, 0.2, 0.7, 1)
    i.append_vertices([[(0, 0, 0), col]])
    i.append_vertices([[(0, 50, 0), col]])
    i.append_vertices([[(50, 0, 0), col]])
    i.append_vertices([[(50, 50, 0), col]])
    i.upload()
    i = p.item_create("Text", "billboardlabel2", "simple3d",
                      "class Item\n(Billboard\nZ axis)", i.origin_tuple, 2)
    i.billboard = True
    i.billboard_axis = "Z"

    # Create an arbitrary filled triangle with smooth colors
    vertexcount = 4
    i = p.item_create("Item", "mytriangle2", "simple3d",
                      GL_TRIANGLE_STRIP, 1, (250, 0, 0), 1, True, vertexcount)
    i.append_vertices([[(0, 0, 1), (0.2, 0.7, 0.2, 1)]])
    i.append_vertices([[(50, 50, 1), (0.7, 0.2, 0.2, 1)]])
    i.append_vertices([[(120, 50, 1), (0.2, 0.2, 0.7, 1)]])
    i.append_vertices([[(120, 50, 70), (1, 1, 1, 0.2)]])
    i.upload()
    i = p.item_create("Text", "trianglelabel1", "simple3d",
                      "class Item\n(GL_TRIANGLE_STRIP\nfilled)",
                      i.origin_tuple, 1)
    i.billboard = True

    # Create an 2D "overlay" triangle.
    # It uses a different shader and does not rotate with the world.
    vertexcount = 3
    i = p.item_create("Item", "mytriangle3", "simple2d",
                      GL_TRIANGLES, 4, (0, 0, 0), 1, False, vertexcount)
    i.append_vertices([[(-0.9, -0.9, 0), (1, 1, 1, 0.5)]])
    i.append_vertices([[(-0.8, -0.8, 0), (1, 1, 1, 0.5)]])
    i.append_vertices([[(-0.8, -0.7, 0), (1, 1, 1, 0.5)]])
    i.upload()

    # Draw a "mexican hat" function
    grid_x = 30
    grid_y = 10

    dat = np.zeros(grid_x * grid_y,
                   [("position", np.float32, 3), ("color", np.float32, 4)])

    for y in range(0, grid_y):
        for x in range(0, grid_x):
            idx = y * grid_x + x
            i = grid_x/2 - x
            j = grid_y/2 - y
            z = 10 * math.sin(math.sqrt(i**2 + j**2)) / \
                (math.sqrt(i**2 + j**2) + 0.1)
            dat["position"][idx] = (x, y, z)
            dat["color"][idx] = (1, 1, 1, 1)

    i = p.item_create("HeightMap", "myheightmap", "heightmap",
                      grid_x, grid_y, dat, True, (100, 400, 1), 10)
    # ============= CREATE RAW OPENGL PRIMITIVES END =============

    # ===== UPDATE ITEMS (OPTIONAL) =====
    # move mystar1
    # mystar1.set_origin((50,50,50))
    # mystar2.set_scale(100)

    # highlight 2nd line of the gcode
    mygcode1.highlight_line(2)

    # ===== DELETE ITEMS (OPTIONAL) =====
    # p.item_remove("mystar2")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

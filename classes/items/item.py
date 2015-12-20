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


import numpy as np
import ctypes
import math

from PyQt5.QtGui import (QMatrix4x4, QVector3D, QVector4D)

from OpenGL.GL import (glBindVertexArray, glBindBuffer,
                       glEnableVertexAttribArray, glVertexAttribPointer,
                       glGenVertexArrays, glGenBuffers, glBufferSubData,
                       glDeleteBuffers, glDeleteVertexArrays, glBufferData,
                       glDrawArrays, glPolygonMode, glDrawElements,
                       glLineWidth,
                       GL_LINES, GL_ARRAY_BUFFER, GL_FLOAT, GL_FALSE,
                       GL_ELEMENT_ARRAY_BUFFER, GL_DYNAMIC_DRAW,
                       GL_STATIC_DRAW, GL_FRONT_AND_BACK, GL_LINE, GL_FILL,
                       GL_UNSIGNED_INT)


class Item():
    """
    This class represents a separate object/item in 3D space.

    It implements OpenGL per-object boilerplate functions.

    Most importantly, an Item has its own relative coordinate system
    with local (0,0,0) located at global self.origin.

    It also has its own units of measurement determined by self.scale.

    It can be rotated around its own local origin by self.rotation_angle and
    self.rotation_vector.

    An instance of this class knows how to
      * add CPU vertex data (color and position) as simple tuples
      * manage all vertex data in numpy format
      * upload CPU vertex data into the GPU fully or in part (substitute)
      * draw itself
      * remove itself
      * calculate its own Model matrix (optionally in "billboard" mode)

    You can use this class directly for drawing raw OpenGL primitives.

    You can subclass to implement composite primitives (see other classes
    in this directory which inherit from it).
    """

    def __init__(self, label, program, primitive_type=GL_LINES, linewidth=1,
                 origin=(0, 0, 0), scale=1, filled=False, vertexcount_max=0):
        """
        @param label
        A string containing a unique name for this item.

        @param prog_id
        OpenGL program ID (determines shaders to use) to use for this item.

        @param primitive_type
        An OpenGL integer GL_LINES, GL_LINE_STRIP, GL_TRINAGLES,
        GL_TRINAGLE_STRIP and others. See OpenGL documentation.

        @param linewidth
        Width of rendered lines in pixels.

        @param origin
        Origin of this item in world space.

        @param scale
        Scale of this item in world space.

        @param vertexcount_max
        The maxiumum number of vertices supported by this item. If you
        decide later that you want to add more vertices than specified
        here, call `set_vertexcount_max()`. Remember that allocating CPU
        and GPU memory for vertices are an expensive operation and should
        be called only rarely.

        @param filled
        True or False. Determines if drawn triangles will be filled with color.
        """

        # generate attribute state label aka VAO
        self.vao = glGenVertexArrays(1)

        # generate data buffer labels aka VBO
        self.vbo_array = glGenBuffers(1)  # this buffer labels positions+colors
        self.vbo_element_array = glGenBuffers(1)  # VertexBuffer ID for indices

        self.program = program
        self.label = label

        self.vertexcount_max = vertexcount_max  # maximum number of vertices
        self.vertexcount = 0  # current number of appended/used vertices

        self.primitive_type = primitive_type
        self.linewidth = linewidth
        self.filled = filled  # if a triangle should be drawn filled

        # billboard mode
        self.billboard = False  # set to True to always face camera
        self.billboard_axis = None  # must be strings "X", "Y", or "Z"

        self.scale = scale  # 1 local unit corresponds to scale world units

        # by default congruent with world origin
        self.origin = QVector3D(*origin)
        self.origin_tuple = origin

        # by default not rotated
        self.rotation_angle = 0
        self.rotation_vector = QVector3D(0, 1, 0)  # default rotation around Y

        self.dirty = True

        self.uniforms = {}

        # TODO: Support not only for attributes "color" and "position", but
        # arbitrary formats.
        supported_vertex_format = [
            ("position", np.float32, 3),
            ("color", np.float32, 4)
        ]
        self.vdata_pos_col = np.zeros(
            self.vertexcount_max, supported_vertex_format)

        if "vdata_indices" not in list(vars(self).keys()):
            self.vdata_indices = None

    def __del__(self):
        """ Python's 'deconstructor'. Called when garbage collected.
        """
        pass

    def setup_vao(self, locations):
        stride = self.vdata_pos_col.strides[0]

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_array)

        offset_pos = ctypes.c_void_p(0)
        loc_pos = locations["attributes"]["position"]
        glEnableVertexAttribArray(loc_pos)
        glVertexAttribPointer(loc_pos, 3, GL_FLOAT,
                              GL_FALSE, stride, offset_pos)

        if "color" in locations["attributes"]:
            offset_col = ctypes.c_void_p(
                self.vdata_pos_col.dtype["position"].itemsize)
            loc_col = locations["attributes"]["color"]
            glEnableVertexAttribArray(loc_col)
            glVertexAttribPointer(loc_col, 4, GL_FLOAT,
                                  GL_FALSE, stride, offset_col)

        if self.vdata_indices is not None:
            # indexed drawing is optional and per-item
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_element_array)

        glBindVertexArray(0)

    def append_vertices(self, vertexdata):
        """
        Appends vertices, each defined with with position and color,
        to CPU data storage but doesn't upload to the GPU. Once done with
        appending all needed vertices, upload to the GPU by calling
        `upload()`.

        @param vertexdata
        A Python list. Each list element is a list `[position, color]`
        where `position` is a 3-tuple and `color` is a 4-tuple.

        """
        length_to_append = len(vertexdata)

        if self.vertexcount + length_to_append > self.vertexcount_max:
            raise IndexError("Item '{}': You are trying to append more vertices for item than the maximum of {}. Use set_vertexcount_max to increase the maximum possible vertices.".format(
                self.label, self.vertexcount_max))

        for vertex in vertexdata:
            self.vdata_pos_col["position"][self.vertexcount] = vertex[0]
            self.vdata_pos_col["color"][self.vertexcount] = vertex[1]
            self.vertexcount += 1

    def set_vertexcount_max(self, new_count):
        """
        Increase the CPU data buffer size to a value larger than the one
        set during initialization. This is an expensive operation.

        @param new_count
        The new maximum number of supported vertices.
        """

        if new_count > self.vertexcount_max:
            self.vertexcount_max = new_count
            extension = np.zeros(
                new_count, [("position", np.float32, 3), ("color", np.float32, 4)])
            self.vdata_pos_col = np.append(self.vdata_pos_col, extension)
        else:
            raise BufferError("Item '{}': You are trying to set a vertex count lower than has been reserved during initialization. This isn't yet supported. User a lower count during initialization instead.".format(
                self.label, self.vertexcount_max))

    def substitute(self, vertex_nr, pos, col):
        """
        If your object has very many vertices, it may be more
        efficient to substitute data directly on the GPU instead of
        re-uploading everything. Use this funtion to modify data
        directly in the GPU.

        @param vertex_nr
        Number of vertex to substitute.

        @param pos
        3-tuple of floats. Position to substitue for specified vertex.

        @params col
        4-tuple of RGBA color. Color to substitute for specified vertex.
        """

        if vertex_nr > self.vertexcount:
            return

        stride = self.vdata_pos_col.strides[0]
        position_size = self.vdata_pos_col.dtype["position"].itemsize
        color_size = self.vdata_pos_col.dtype["color"].itemsize

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_array)

        # replace position
        position = np.array([pos[0], pos[1], pos[2]], dtype=np.float32)
        offset = vertex_nr * stride
        glBufferSubData(GL_ARRAY_BUFFER, offset, position_size, position)

        # replace color
        color = np.array([col[0], col[1], col[2], col[3]], dtype=np.float32)
        offset = vertex_nr * stride + position_size
        glBufferSubData(GL_ARRAY_BUFFER, offset, color_size, color)

    def remove(self):
        """
        Removes self. The object will disappear from the world.
        """
        glDeleteBuffers(1, [self.vbo_array])

        if self.vdata_indices is not None:
            glDeleteBuffers(1, [self.vbo_element_array])

        glDeleteVertexArrays(1, [self.vao])
        self.dirty = True
        print("Item {}: removing myself.".format(self.label))

    def upload(self):
        """
        This method will upload the entire CPU vertex data to the GPU.

        Call this once after all the CPU data have been set with
        `append_vertices()`. Note that uploading a large set of data
        is an expensive operation. To modify data, call `substitute()`
        instead.
        """
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_array)
        # TODO: make STATIC/DYNAMIC drawing configurable
        glBufferData(GL_ARRAY_BUFFER, self.vdata_pos_col.nbytes,
                     self.vdata_pos_col, GL_DYNAMIC_DRAW)

        if self.vdata_indices is not None:
            # indexes never change and are static
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.vdata_indices.nbytes,
                         self.vdata_indices, GL_STATIC_DRAW)

        glBindVertexArray(0)

    def set_scale(self, fac):
        """
        Alternative method to set scale.

        @param fac
        Scale factor
        """
        self.scale = fac

    def set_origin(self, tpl):
        """
        Alternative method to set origin.

        @param tpl
        Origin of self in world coordinates as 3-tuple
        """
        self.origin = QVector3D(*tpl)
        self.origin_tuple = tpl

    def draw(self, mat_v_inverted):
        """
        Draws this object. Call this from within `paintGL()`.
        Assumes that glUseProgram() has been called.

        @param viewmatrix_inverted
        The inverted View matrix. It contains Camera position and angles.
        Mandatory only when self.billboard == True
        """

        mat_m = self.calculate_model_matrix(mat_v_inverted)
        mat_m = Item.qt_mat_to_list(mat_m)
        self.program.set_uniform("mat_m", mat_m)

        for key, val in self.uniforms.items():
            if not key in self.program.locations["uniforms"]:
                raise SystemError(
                    "Shader does not know about uniform {}".format(key))
            self.program.set_uniform(key, val)

        if self.filled:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # set up state
        glBindVertexArray(self.vao)

        # draw!
        glLineWidth(self.linewidth)

        if self.vdata_indices is not None:
            # indexed drawing
            glDrawElements(self.primitive_type, self.vdata_indices.size,
                           GL_UNSIGNED_INT, ctypes.c_void_p(0))
        else:
            glDrawArrays(self.primitive_type, 0, self.vertexcount)

        glBindVertexArray(0)

        self.dirty = False

    def calculate_model_matrix(self, viewmatrix_inv=None):
        """
        Calculates the Model matrix based upon self.origin and self.scale.

        If self.billboard == False, the Model matrix will also be rotated
        determined by self.rotation_angle and self.rotation_axis.

        If self.billboard == True and self.billboard_axis == None
        the Model matrix will also be rotated so that the local Z axis
        will face the camera and the local Y axis will be parallel to
        the camera up axis at all times.

        If self.billboard == True and self.billboard_axis is either "X",
        "Y", or "Z", the local Z axis will always face the camera, but
        the items rotation will be restricted to self.billboard_axis.

        @param viewmatrix_inv
        The inverted View matrix as instance of QMatrix4x4. Mandatory when
        self.billboard == True, otherwise optional.
        """
        mat_m = QMatrix4x4()
        mat_m.translate(self.origin)

        if self.billboard:
            # Billboard calulation is based on excellent tutorial:
            # http://nehe.gamedev.net/article/billboarding_how_to/18011/

            # extract 2nd column which is camera up vector
            cam_up = viewmatrix_inv * QVector4D(0, 1, 0, 0)
            cam_up = QVector3D(cam_up[0], cam_up[1], cam_up[2])
            cam_up.normalize()

            # extract 4th column which is camera position
            cam_pos = viewmatrix_inv * QVector4D(0, 0, 0, 1)
            cam_pos = QVector3D(cam_pos[0], cam_pos[1], cam_pos[2])

            # calculate self look vector (vector from self.origin to camera)
            bill_look = cam_pos - self.origin
            bill_look.normalize()

            if self.billboard_axis == None:
                # Fully aligned billboard, rotation not restricted to axes.
                # Calculate new self right vector based upon self look and
                # camera up
                bill_right = QVector3D.crossProduct(cam_up, bill_look)

                # Calculate self up vector based on self look and self right
                bill_up = QVector3D.crossProduct(bill_look, bill_right)

            else:
                axis_words = ["X", "Y", "Z"]
                axis = axis_words.index(self.billboard_axis)

                bill_up = [0]*3

                for i in range(0, 3):
                    bill_up[i] = 1 if i == axis else 0
                bill_up = QVector3D(*bill_up)

                bill_look_zeroed = [0]*3

                for i in range(0, 3):
                    bill_look_zeroed[i] = 0 if i == axis else bill_look[i]
                bill_look = QVector3D(*bill_look_zeroed)
                bill_look.normalize()

                bill_right = QVector3D.crossProduct(bill_up, bill_look)

            # View and Model matrices are actually nicely structured!
            # 1st column: camera right vector
            # 2nd column: camera up vector
            # 3rd column: camera look vector
            # 4th column: camera position

            # Here we only overwrite right, up and look.
            # Position is already in the matrix, and we don't have to change it
            mat_m[0, 0] = bill_right[0]
            mat_m[1, 0] = bill_right[1]
            mat_m[2, 0] = bill_right[2]

            mat_m[0, 1] = bill_up[0]
            mat_m[1, 1] = bill_up[1]
            mat_m[2, 1] = bill_up[2]

            mat_m[0, 2] = bill_look[0]
            mat_m[1, 2] = bill_look[1]
            mat_m[2, 2] = bill_look[2]

        else:
            mat_m.rotate(self.rotation_angle, self.rotation_vector)

        mat_m.scale(self.scale)

        return mat_m

    @staticmethod
    def angle_between(v1, v2):
        """
        Returns angle in radians between vector v1 and vector v2.

        @param v1
        Vector 1 of class QVector3D

        @param v2
        Vector 2 of class QVector3D
        """

        return math.acos(
            QVector3D.dotProduct(v1, v2) / (v1.length() * v2.length())
        )

    @staticmethod
    def qt_mat_to_list(mat):
        """
        Transforms a QMatrix4x4 into a one-dimensional Python list
        in row-major order, suitable to upload into the GPU.

        @param mat
        Matrix of type QMatrix4x4
        """
        arr = [0] * 16

        for i in range(4):
            for j in range(4):
                idx = 4 * i + j
                arr[idx] = mat[i, j]

        return arr

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

from OpenGL.GL import (glCreateShader, glShaderSource, glCompileShader,
                       glGetShaderiv, glGetShaderInfoLog, GL_COMPILE_STATUS)


class Shader():
    """
    This class represents an OpenGL shader.
    """

    def __init__(self, shader_type, filepath):
        """
        Create a named OpenGL program, attach shaders to it, and remember.
        """

        self.id = glCreateShader(shader_type)

        # set the GLSL sources
        with open(filepath, "r") as f:
            sourcecode = f.read()

        glShaderSource(self.id, sourcecode)

        # compile
        glCompileShader(self.id)

        compile_result = glGetShaderiv(self.id, GL_COMPILE_STATUS)

        if (compile_result == 0):
            raise RuntimeError("Error in Shader: " +
                               str(glGetShaderInfoLog(self.id)))
        print("SHADER COMPILE", filepath, compile_result)

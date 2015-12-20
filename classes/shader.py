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

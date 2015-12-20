# pyglpainter - Python OpenGL Painter

Minimalistic but modern OpenGL drawing for technical applications

![](http://michaelfranzl.com/wp-content/uploads/2016/04/Selection_309-1024x576.png)

This Python module provides the class `PainterWidget`, extending PyQt5's `QGLWidget` class with
boilerplate code necessary for applications which want to build a classical orthagonal 3D world in
which the user can interactively navigate with the mouse via the classical (and expected)
Pan-Zoom-Rotate paradigm implemented via a virtual trackball (using quaternions for rotations).

This class is especially useful for technical visualizations in 3D space. It provides a simple
Python API to draw raw OpenGL primitives (`LINES`, `LINE_STRIP`, `TRIANGLES`, etc.) as well as a
number of useful composite primitives rendered by this class itself (`Grid`, `Star`, `CoordSystem`,
`Text`, etc., see files in classes/items). As a bonus, all objects/items can either be drawn as real
3D world entities which optionally support "billboard" mode (fully camera-aligned or arbitrary- axis
aligned), or as a 2D overlay.

It uses the "modern", shader-based, OpenGL API rather than the deprecated "fixed pipeline" and was
developed for Python version 3 and Qt version 5.

Model, View and Projection matrices are calculated on the CPU, and then utilized in the GPU.

Qt has been chosen not only because it provides the GL environment, but also vector, matrix and
quaternion math. A port of this Python code into native Qt C++ is therefore trivial.

Look at `example.py`, part of this project, to see how this class can be used. If you need more
functionality, consider sub-classing.

Most of the time, calls to `item_create()` are enough to build a 3D world with interesting objects
in it (the name for these objects here is "items"). Items can be rendered with different shaders.

This project was originally created for a CNC application, but then extracted from this application
and made multi-purpose. The author believes it contains the simplest and shortest code to quickly
utilize the basic and raw powers of OpenGL. To keep code simple and short, the project was optimized
for technical, line- and triangle based primitives, not the realism that game engines strive for.
The simple shaders included in this project will draw aliased lines and the output therefore will
look more like computer graphics of the 80's.  But "modern" OpenGL offloads many things into shaders
anyway.

This class can either be used for teaching purposes, experimentation, or as a visualization backend
for production-class applications.

## Mouse Navigation

Left Button drag left/right/up/down: Rotate camera left/right/up/down

Middle Button drag left/right/up/down: Move camera left/right/up/down

Wheel rotate up/down: Move camera ahead/back

Right Button drag up/down: Move camera ahead/back (same as wheel)

The FOV (Field of View) is held constant. "Zooming" is rather moving the camera forward along its
look axis, which is more natural than changing the FOV of the camera. Even cameras in movies and TV
series nowadays very, very rarely zoom.



## Installation

Your graphics hardware and drivers need to support at least OpenGL version 2.1 with GLSL version
1.20.

Get and install `python3`, its `venv` module, and `git`. Then:

```bash
git clone https://github.com/michaelfranzl/pyglpainter
cd pyglpainter
git clone https://github.com/michaelfranzl/gcode_machine.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./example.py
```


### Usage as a module in your own project

You first need to create a PyQt5 window, then add to it one `PainterWidget` instance (for working
code see `example.py`). Let's say this `PainterWidget` instance is stored in the variable `painter`.
You then can simply draw a coordinate system:

```python
mycs1 = painter.item_create("CoordSystem", "mycs1", "simple3d", 12, (0, 0, 0))
```

This means: Painter, create an item of class `CoordSystem` labeled "mycs1" with the shader program
called "simple3d". Scale it by 12 and put its origin to the world coordinates (0,0,0).



## License

Copyright (c) 2015 Michael Franzl

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

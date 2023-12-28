# pyglpainter

Minimalistic, modern OpenGL drawing library for technical applications, teaching or
experimentation. It is implemented in Python 3 with Qt 5 bindings (it inherits from `QOpenGLWidget`).

It provides a simple Python API to draw raw OpenGL primitives (`LINES`, `LINE_STRIP`, `TRIANGLES`, etc.)
as well as a number of useful composite primitives
(see classes `Grid`, `Star`, `CoordSystem`, `Text`, `Circle`, `Arc`, `HeightMap`, `OrthoLineGrid`).

All objects/items can either be drawn as real
3D world entities (which optionally support "billboard" mode), or as a 2D overlay.

The user can interactively navigate using the mouse via the classical Pan-Zoom-Rotate paradigm
implemented via a virtual trackball (using quaternions for rotations).


## Background

This code was originally written for a CNC application, but then split off
and made more general.

This library was developed to produce simple technical visualizations
and minimalistic line drawings in 3D space; it does not implement a hierarchical scene graph.
To be extensible, shader code has to be supplied by the application.

It uses the "modern", shader-based, OpenGL API rather than the deprecated "fixed pipeline".

Qt has been chosen not only because it provides the GL environment, but also vector, matrix and
quaternion math. A port of this Python code into native Qt C++ would therefore be trivial.



## Installation

```sh
pip install pyglpainter
```


## Usage

The test directory of the source repository provides a full integration example,
which can also be run for testing.

Most of the time, calls to `item_create()` are enough to build a 3D world with objects
in it (the name for these objects here is "items"). Items can be rendered using different shader
programs.


### Mouse Navigation

**Left Button drag left/right/up/down:** Rotate camera left/right/up/down

**Middle Button drag left/right/up/down:** Move camera left/right/up/down

**Wheel rotate up/down:** Move camera ahead/back

**Right Button drag up/down:** Move camera ahead/back (same as wheel)

One particular choice was to hold the camera's field of view constant; "Zooming" can be achieved by
moving the camera forward along its look axis.


## Requirements

* The Python version specified in the file `.python-version`
* OpenGL version 2.1 (with GLSL version 1.20)


## Development

Dependencies are managed using `pipenv`:

```sh
pip install pipenv --user
pipenv install --dev
```

To run the example:

```sh
PYTHONPATH=src pipenv run python ./test/example.py
```

### Building

```sh
pipenv run make build_deps
pipenv run make dist
```

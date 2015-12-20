#version 120

uniform mat4 mat_m;

attribute vec4 color;
attribute vec3 position;
varying vec4 v_color;

void main()
{
  gl_Position = mat_m * vec4(position, 1.0);
  v_color = color;
}
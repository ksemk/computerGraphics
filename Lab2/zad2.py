#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time, x, y, a, b):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)

    # First Triangle
    # Vertex 1 (Red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y)

    # Vertex 2 (Green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x, y + a)

    # Vertex 3 (Blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x + b, y)

    # Second Triangle
    # Vertex 1 (Green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x, y + a)

    # Vertex 3 (White)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x + b, y + a)

    # Vertex 4 (Blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x + b, y)

    glEnd()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    
    x_coordinate = float(input("Give an x coordinates: "))
    y_coordinate = float(input("Give an y coordinates: "))
    a_length = float(input("Give an a length: "))
    b_length = float(input("Give an b length: "))

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), x_coordinate, y_coordinate, a_length, b_length)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

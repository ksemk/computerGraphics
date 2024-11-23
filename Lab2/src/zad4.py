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


def render(time, size, depth):
    def draw_square(x, y, size):
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + size, y)
        glVertex2f(x + size, y + size)
        glVertex2f(x, y + size)
        glEnd()

    def sierpinski_carpet(x, y, size, depth):
        if depth == 0:
            glColor3f(0.0, 0.0, 0.0)
            draw_square(x, y, size)
        else:
            new_size = size / 3
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1:
                        glColor3f(1.0, 1.0, 1.0)
                        draw_square(x + i * new_size, y + j * new_size, new_size)
                    else:
                        sierpinski_carpet(x + i * new_size, y + j * new_size, new_size, depth - 1)

    glClear(GL_COLOR_BUFFER_BIT)
    sierpinski_carpet(-size / 2, -size / 2, size, depth)
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

    depth = int(input("Enter depth of the algo: "))

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()



    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), 200.0, depth)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

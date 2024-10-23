#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def render(time, power, pixel_size):
    def draw_square(x, y, size, color):
        glBegin(GL_QUADS)
        glColor3f(color, color, color)  # Use grayscale color
        glVertex2f(x, y)
        glVertex2f(x + size, y)
        glVertex2f(x + size, y + size)
        glVertex2f(x, y + size)
        glEnd()

    def plasma(x, y, size, c1, c2, c3, c4):
        if size <= pixel_size:
            color = (c1 + c2 + c3 + c4) / 4
            draw_square(x, y, size, color)
        else:
            half = size / 2
            mid = (c1 + c2 + c3 + c4) / 4 + random.uniform(-0.1, 0.1)
            t1 = (c1 + c2) / 2
            t2 = (c2 + c3) / 2
            t3 = (c3 + c4) / 2
            t4 = (c4 + c1) / 2

            plasma(x, y, half, c1, t1, mid, t4)
            plasma(x + half, y, half, t1, c2, t2, mid)
            plasma(x + half, y + half, half, mid, t2, c3, t3)
            plasma(x, y + half, half, t4, mid, t3, c4)

    glClear(GL_COLOR_BUFFER_BIT)
    size = 2 ** power * pixel_size
    c1 = random.random()
    c2 = random.random()
    c3 = random.random()
    c4 = random.random()
    plasma(-size / 2, -size / 2, size, c1, c2, c3, c4)
    glFlush()

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)  # Match the viewport to the window size
    glLoadIdentity()

    # Remove the aspect ratio, ensure that the rendering space matches the window size
    glOrtho(-width / 2, width / 2, -height / 2, height / 2, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), power = 10, pixel_size = 1)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys
import numpy as np

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    generate_colors(1000)  # Precompute colors


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def egg_points(N):
    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)
    u, v = np.meshgrid(u, v)
    u = u.flatten()
    v = v.flatten()

    x = (-(90 * u**5) + (225 * u**4) - (270 * u**3) + (180 * u**2) - (45 * u)) * np.cos(np.pi * v)
    y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
    z = (-(90 * u**5) + (225 * u**4) - (270 * u**3) + (180 * u**2) - (45 * u)) * np.sin(np.pi * v)

    return x, y, z


# Precompute colors
colors = []

def generate_colors(N):
    global colors
    for _ in range((N - 1) * (N - 1) * 2):
        colors.append((
            random.random(),
            random.random(),
            random.random()
        ))


def egg_triangle(N):
    x, y, z = egg_points(N)
    glBegin(GL_TRIANGLES)
    
    global colors
    color_index = 0
    for i in range(N - 1):
        for j in range(N - 1):
            index = i * N + j
            
            # Triangle 1
            glColor3f(*colors[color_index])
            glVertex3f(x[index], y[index], z[index])
            glVertex3f(x[index + 1], y[index + 1], z[index + 1])
            glVertex3f(x[index + N], y[index + N], z[index + N])
            color_index += 1
            
            # Triangle 2
            glColor3f(*colors[color_index])
            glVertex3f(x[index + 1], y[index + 1], z[index + 1])
            glVertex3f(x[index + N + 1], y[index + N + 1], z[index + N + 1])
            glVertex3f(x[index + N], y[index + N], z[index + N])
            color_index += 1
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    spin(time * 180 / 3.1415)
    axes()
    egg_triangle(1000)
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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


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
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
        
    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()

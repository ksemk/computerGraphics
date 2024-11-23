#!/usr/bin/env python3
import sys
import numpy as np
from scipy.special import comb
import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
# Control points grid parameters
# Parametry siatki punktów kontrolnych
control_points = np.array([
    [[-1.5, -1.5,  4.0], [-0.5, -1.5,  2.0], [ 0.5, -1.5, -1.0], [ 1.5, -1.5,  2.0]],
    [[-1.5, -0.5,  1.0], [-0.5, -0.5,  3.0], [ 0.5, -0.5,  0.0], [ 1.5, -0.5, -1.0]],
    [[-1.5,  0.5,  4.0], [-0.5,  0.5,  0.0], [ 0.5,  0.5,  3.0], [ 1.5,  0.5,  4.0]],
    [[-1.5,  1.5, -2.0], [-0.5,  1.5, -2.0], [ 0.5,  1.5,  0.0], [ 1.5,  1.5, -1.0]]
])
show_bezier_surface = True
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glRotatef(45, 1.0, 1.0, 0.0)  # Rotate the scene by 45 degrees around the x and y axes
    gluLookAt(0.0, 0.0, 5.0, 
              0.0, 0.0, 0.0,  
              0.0, 1.0, 0.0)


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

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # spin(time * 180 / 3.1415)  # Rotate the scene
    axes()  # Draw coordinate axes
    draw_control_points()  # Show control points
def update_viewport(_, width, height):
    if show_bezier_surface:
        draw_bezier_surface()  # Paint the surface
    glFlush()
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

def draw_control_points():
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for row in control_points:
        for point in row:
            glVertex3f(point[0], point[1], point[2])
    glEnd()

def draw_control_lines():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    for row in control_points:
        for i in range(len(row) - 1):
            glVertex3f(row[i][0], row[i][1], row[i][2])
            glVertex3f(row[i + 1][0], row[i + 1][1], row[i + 1][2])
    for col in range(len(control_points[0])):
        for row in range(len(control_points) - 1):
            glVertex3f(control_points[row][col][0], control_points[row][col][1], control_points[row][col][2])
            glVertex3f(control_points[row + 1][col][0], control_points[row + 1][col][1], control_points[row + 1][col][2])
    glEnd()

def bernstein(i, n, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_surface(u, v):
    B = np.zeros(3)
    for i in range(4):
        for j in range(4):
            B += control_points[i][j] * bernstein(i, 3, u) * bernstein(j, 3, v)
    return B

def draw_bezier_surface():
    glColor3f(0.5, 0.5, 1.0)  # Base color for the surface
    N = 20  # Resolution of the surface (number of divisions)
    
    for i in range(N - 1):
        for j in range(N - 1):
            # Compute Bézier surface vertices for current and adjacent grid points
            u, v = i / (N - 1), j / (N - 1)
            u_next, v_next = (i + 1) / (N - 1), (j + 1) / (N - 1)
            
            # Get the positions of four surrounding vertices
            p1 = bezier_surface(u, v)
            p2 = bezier_surface(u_next, v)
            p3 = bezier_surface(u, v_next)
            p4 = bezier_surface(u_next, v_next)
            
            # Render two triangles per grid square
            glBegin(GL_TRIANGLES)
            
            # Triangle 1 (p1, p2, p3)
            glColor3f(u, v, 0.5)  # Gradient color based on (u, v)
            glVertex3f(p1[0], p1[1], p1[2])
            glVertex3f(p2[0], p2[1], p2[2])
            glVertex3f(p3[0], p3[1], p3[2])
            
            # Triangle 2 (p2, p4, p3)
            glColor3f(u_next, v_next, 0.5)  # Gradient color for variation
            glVertex3f(p2[0], p2[1], p2[2])
            glVertex3f(p4[0], p4[1], p4[2])
            glVertex3f(p3[0], p3[1], p3[2])
            
            glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)  # Rotate the scene
    axes()  # Draw coordinate axes
    draw_control_points()  # Show control points
    draw_control_lines()  # Show control lines
    if show_bezier_surface:
        draw_bezier_surface()  # Paint the surface
    glFlush()
    
def spin(angle):
    glRotatef(angle, 0.0, 0.1, 0.5)


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

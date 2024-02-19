# 3d_graphics.py
import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Graphics3D:
    def __init__(self):
        pygame.init()
        width, height = 800, 600
        display = (width, height)
        self.window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glBegin(GL_TRIANGLES)
            glColor3f(1, 0, 0)
            glVertex3f(-1, -1, 0)
            glColor3f(0, 1, 0)
            glVertex3f(0, 1, 0)
            glColor3f(0, 0, 1)
            glVertex3f(1, -1, 0)
            glEnd()
            pygame.display.flip()
            pygame.time.wait(10)

from math import sqrt, asinh, atan, atan2, cos, sin, pi
import numpy as np
import pygame
from pygame.locals import *
import sys
import random

import hack

x_data = hack.x
y_data = hack.y

J = len(x_data)

N = 5
T = 1
F = 0.1

dt = 0.05

x_coefs = [[] for _ in range(N)]
y_coefs = [[] for _ in range(N)]

for n in range(N):
    Sum_xcos, Sum_xsin, Sum_ycos, Sum_ysin = 0, 0, 0, 0

    for j in range(J):
        Sum_xcos += 2 / J * x_data[j] * cos(n * 2 * pi * j / J)
        Sum_xsin += 2 / J * x_data[j] * sin(n * 2 * pi * j / J)
        Sum_ycos += 2 / J * y_data[j] * cos(n * 2 * pi * j / J)
        Sum_ysin += 2 / J * y_data[j] * sin(n * 2 * pi * j / J)

    x_coefs[n] = [Sum_xcos, Sum_xsin]  
    y_coefs[n] = [Sum_ycos, Sum_ysin]

print(y_coefs)

old_point = None

w, h = 800, 480

screen = pygame.display.set_mode((w,h))
trace = pygame.Surface((w,h))
screen.fill((100, 30, 170))
pygame.display.update()
clock = pygame.time.Clock()

def draw_hor(n, d, P, t): #(harmonic, direction, center, time)
    R = sqrt(x_coefs[n][0]**2 + x_coefs[n][1]**2)
    alpha = atan(x_coefs[n][1] / x_coefs[n][0])
    pygame.draw.circle(screen, (100,40,70), P, R / 2, width = 2)
    pygame.draw.line(screen, (200,20,35), P, [P[0] + R / 2 * cos(n * F * t + alpha), P[1] + d * R / 2 * sin(n * F * t + alpha)], width = 3)
    return [P[0] + R / 2 * cos(n * F * t + alpha), P[1] + d * R / 2 * sin(n * F * t + alpha)]


def draw_ver(n, d, P, t):
    R = sqrt(y_coefs[n][0]**2 + y_coefs[n][1]**2)
    alpha = atan(y_coefs[n][1] / y_coefs[n][0]) 
    pygame.draw.circle(screen, (100,40,70), P, R / 2, width = 2)
    pygame.draw.line(screen, (200,20,35), P, [P[0] + d * R / 2 * sin(n * F * t + alpha), P[1] + R / 2 * cos(n * F * t + alpha)], width = 3)
    return [P[0] + d * R / 2 * sin(n * F * t + alpha), P[1] + R / 2 * cos(n * F * t + alpha)]


def Trace(A, B, Color):
    pygame.draw.line(trace, Color, A, B, width = 4)
    return


for j in range(J - 1):
    Trace((w/2 + x_data[j], h/2 + y_data[j]), (w/2 + x_data[j + 1], h/2 + y_data[j + 1]), (10, 200, 50))

"""for j in range(J - 1):
    Trace((j * w / J, h/2 + x_data[j]), ((j+1) * w / J, h/2 + x_data[j + 1]), (10, 200, 50))
"""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill((100, 30, 170))
    screen.blit(trace, (0, 0))

    Center = [w / 2, h / 2]
    
    for i in range(1, N):
        Center = draw_hor(i, 1, Center, T)
        Center = draw_ver(i, -1, Center, T)
        Center = draw_hor(i, -1, Center, T)
        Center = draw_ver(i, 1, Center, T)


        

    if old_point:
        Trace(old_point, Center, (40, 0, 200))



    old_point = Center

    T += dt
    clock.tick(100)
    pygame.display.update()
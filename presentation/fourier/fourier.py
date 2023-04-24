from math import sqrt, atan2, cos, sin, pi
from typing import Tuple, List, Callable
import numpy as np

class Fourier:
    __slots__ = ["number_of_coefficents", "origin", "time", "x_coefs", "y_coefs", "scale"]

    def _generate_coefficents(self, number_of_coefficents: int, x_data: list, y_data: list) -> Tuple[List[float], List[float]]:
        assert(len(x_data) == len(y_data))

        J = len(x_data)
        
        x_coefs = np.zeros(number_of_coefficents, dtype=(float, 2))
        y_coefs = np.zeros(number_of_coefficents, dtype=(float, 2))

        for n in range(number_of_coefficents):
            sum_cos_x = sum((2 / J * x_data[j] * cos(n * 2 * pi * j / J) for j in range(J)))
            sum_cos_y = sum((2 / J * y_data[j] * cos(n * 2 * pi * j / J) for j in range(J)))
            sum_sin_x = sum((2 / J * x_data[j] * sin(n * 2 * pi * j / J) for j in range(J)))
            sum_sin_y = sum((2 / J * y_data[j] * sin(n * 2 * pi * j / J) for j in range(J)))

            x_coefs[n] = (sqrt(sum_cos_x ** 2 + sum_sin_x ** 2), atan2(sum_sin_x, sum_cos_x)) # cosx, sinx, radius, alpha
            y_coefs[n] = (sqrt(sum_cos_y ** 2 + sum_sin_y ** 2), atan2(sum_sin_y, sum_cos_y)) # cosy, siny, radius, alpha

            if n == 0:
                self.origin = (sum_cos_x, sum_cos_y)

        self.x_coefs = x_coefs
        self.y_coefs = y_coefs

    def __init__(self, number_of_coefficents: int, x_data: list, y_data: list, scale: float = 1):
        self.number_of_coefficents = number_of_coefficents
        self.time = 1
        self.scale = scale
        self._generate_coefficents(number_of_coefficents, x_data, y_data)
    
    def __iter__(self):
        scale = self.scale

        center = (self.origin[0], self.origin[1])
        time = self.time

        def horizontal(n: int, direction: int) -> Tuple[float, float]:
            radius, alpha = self.x_coefs[n]
            x = center[0] + radius / 2 * cos(n * scale * time + alpha)
            y = center[1] + direction * radius / 2 * sin(n * scale * time + alpha)
            center = (x, y)
            return ((x, y, radius), (*center, x, y))
        
        def vertical(n: int, direction: int):
            radius, alpha = self.y_coefs[n]
            x = center[0] + direction * radius / 2 * sin(n * scale * time + alpha)
            y = center[1] + radius / 2 * cos(n * scale * time + alpha)
            center = (x, y)
            return ((x, y, radius), (*center, x, y))

        for i in range(1, self.number_of_coefficents):
            yield horizontal(i, 1)
            yield vertical(i, -1)
            yield horizontal(i, -1)
            yield vertical(i, 1)
        
        return center
    
    def draw(self, circle: Callable, line: Callable) -> Tuple[float, float]:
        points = iter(self)
        try:
            while True:
                    c, l = next(points)
                    circle(*c)
                    line(*l)
        except StopIteration as end:
            return end.value

    def step(self, dt: float):
        self.time += dt

def _main():
    import pygame
    import sys
    
    import example.point_arrays as point_arrays
    
    fourier = Fourier(50, point_arrays.x, point_arrays.y, 0.5)
    old_point = None

    w, h = 800, 480
    hw, hh = w / 2, h / 2

    screen = pygame.display.set_mode((w,h))
    trace = pygame.Surface((w,h))
    screen.fill((100, 30, 170))
    pygame.display.update()
    clock = pygame.time.Clock()

    def circle(x: float, y: float, radius: float, color: Tuple[int, int, int] = (100, 40, 70), surface: pygame.Surface = screen):
        pygame.draw.circle(surface, color, (hw + x, hh + y), radius, width = 2)

    def line(start_x: float, start_y: float, end_x: float, end_y: float, color: Tuple[int, int, int] = (200, 20, 35), surface: pygame.Surface = screen):
        pygame.draw.line(surface, color, (hw + start_x, hh + start_y), (hw + end_x, hh + end_y), width = 3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        screen.fill((100, 30, 170))
        screen.blit(trace, (0, 0))
        
        center = fourier.draw(circle, line)

        if old_point:
            line(old_point[0], old_point[1], center[0], center[1], color = (40, 0, 200), surface = trace)
        old_point = center
        
        fourier.step(0.02)

        clock.tick(100)
        pygame.display.update()

if __name__ == "__main__":
    _main()

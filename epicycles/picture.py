from manim import *
from manim_presentation import Slide
import numpy as np

from fourier.fourier import Fourier

import fourier.example.point_arrays as points_arrays

class Picture(Slide):
    def construct(self):
        """
            Using value trackers and the fourier iterator update line and circle positions
        """

        N = 50

        scale = 14 / 800
        fourier = Fourier(N, points_arrays.x * scale, points_arrays.y * -scale, 0.5)

        circles = []
        lines = []

        centers = np.zeros((N - 1) * 4, dtype=(float, 3))
        points = np.zeros(((N - 1) * 4, 2), dtype=(float, 3))

        for i, data in enumerate(fourier):
            c, l = data
            x, y, radius = c
            sx, sy, ex, ey = l

            centers[i] = (x, y, 10)

            points[i][0] = (sx, sy, 0)
            points[i][1] = (ex, ey, 0)
            
            shape = Circle(radius, color=BLUE, stroke_width=0.5).move_to((x, y, 0)).add_updater(lambda mobject, dt, index=i: mobject.move_to(centers[index]))
            circles.append(shape)

            shape = Line((sx, sy, 0), (ex, ey, 0), stroke_width=0.5, color=YELLOW).add_updater(lambda mobject, dt, index=i: mobject.put_start_and_end_on(points[index][0], points[index][1]))
            lines.append(shape)
        
        def update(dt: float):
            fourier.step(dt)

            for i, data in enumerate(fourier):
                c, l = data
                x, y, _ = c
                sx, sy, ex, ey = l

                centers[i] = (x, y, 10)

                points[i][0] = (sx, sy, 0)
                points[i][1] = (ex, ey, 0)

        self.add(*circles, *lines)
        self.add(Mobject().add_updater(lambda _, dt: update(dt)))

        trail = TracedPath(lambda: points[(N - 1) * 4 - 1][1], dissipating_time = 15, stroke_width = 0.5, stroke_color = PURPLE)
        fade = TracedPath(lambda: points[(N - 1) * 4 - 1][1], dissipating_time = 3, stroke_opacity = [0, 1], stroke_width = 3, stroke_color = PURPLE)
        self.add(trail, fade)
        
        self.wait(20)
        
        self.pause()

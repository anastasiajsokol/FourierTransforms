from manim import *
from manim_slides import Slide

import sys
sys.path.append("../code")

from .. import fourier

class Picture(Slide):
    def construct(self):
        def line(sx, sy, ex, ey):
            self.add(Line([sx, sy, 0], [ex, ey, 0], color="RED"))
        
        def circle(x, y, radius):
            self.add(Circle(radius=radius, color="blue").move_to([x, y, 0]))



        self.wait()

        self.next_slide()

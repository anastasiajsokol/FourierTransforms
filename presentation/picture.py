from manim import *
from manim_slides import Slide

from fourier.fourier import Fourier

class Picture(Slide):
    def construct(self):
        """
            Using value trackers and the fourier iterator update line and circle positions
        """
        
        self.wait()

        self.next_slide()

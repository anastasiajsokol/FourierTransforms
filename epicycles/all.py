from manim import *
from manim_slides import Slide

from intro import *
from note import *
from implimentation import *
from end import *

class All(Slide):
    def construct(self):
        Intro.construct(self)
        self.clear()

        # video

        

        Implimentation.construct(self)
        self.clear()

        # increasing forms

        End.construct(self)
        self.clear()
        
        self.wait()
        self.next_slide()
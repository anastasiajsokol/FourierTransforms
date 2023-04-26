from manim import *
from manim_slides import Slide

class End(Slide):
  def construct(self):
    title = Tex("Thank You")

    title.scale(2)
    
    self.play(Write(title))
    
    self.next_slide()

from manim import *
from manim_slides import Slide

class Intro(Slide):
  def construct(self):
    title = Tex("Fourier Epicycles")
    subtitle = Tex("Drawing pictures with rotating circles")

    title.scale(2)
    subtitle.scale(0.8)
    
    subtitle.next_to(title, direction = DOWN)

    self.play(Write(title))
    self.play(Write(subtitle))

    self.next_slide()

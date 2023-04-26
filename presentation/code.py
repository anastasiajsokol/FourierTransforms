from manim import *
from manim_slides import Slide

class Intro(Slide):
  def construct(self):
    coefs = Code(code="""def _generate_coefficents(self, number_of_coefficents: int, x_data: list, y_data: list) -> Tuple[List[float], List[float]]:
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
        self.y_coefs = y_coefs""", language="python")

    iter = Code(code="""def __iter__(self):
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
        
        return center""", language="python")
    
    self.add(coefs)

    self.next_slide()

    self.remove(coefs)
    self.add(iter)
    
    self.next_slide()

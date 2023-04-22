import path
import outline

transform, data = outline.generate_outline("example/pi.svg")
reader = path.PathReader(data)

f = path.Path()

for command in reader:
    f.add(path.compile(command))

# plot

import matplotlib.pyplot as plt
from numpy import arange

x = []
y = []
for t in arange(0, 1, 0.001):
    a, b = f(t)
    x.append(a)
    y.append(b)

plt.plot(x, y)
plt.show()

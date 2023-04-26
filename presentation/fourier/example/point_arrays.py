from . import treble
import numpy

data = treble.data

x = []
y = []

for i in range(0, len(data), 2):
    x.append(data[i])
    y.append(data[i + 1])

x = numpy.array(x)
y = numpy.array(y)

x *= 4
y *= 4

x -= 120
y -= 180
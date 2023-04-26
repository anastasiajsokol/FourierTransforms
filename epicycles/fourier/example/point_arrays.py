from . import note
import numpy

data = note.data

x = []
y = []

for i in range(0, len(data), 2):
    x.append(data[i])
    y.append(data[i + 1])

x = numpy.array(x)
y = numpy.array(y)

x *= 3
y *= 3

x -= 150
y -= 150
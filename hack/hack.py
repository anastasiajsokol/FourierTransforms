import points
import numpy

data = points.data

x = []
y = []

for i in range(0, len(data), 2 * 4):
    x.append(data[i])
    y.append(data[i + 1])

x = numpy.array(x)
y = numpy.array(y)

x /= 80
y /= -80

x -= 80
y += 20
import numpy as np
import math
import re

class PathError(Exception):
    """Raised if an invalid parameter is passed"""

class Component:
    """symbolic component class"""

class Component:
    __slots__ = []
    """symbolic component class"""

class Path:
    def __init__(self):
        self.path = []
        self.distance = 0
    
    def add(self, item: Component) -> None:
        self.distance += item.distance
        self.path.append(item)
    
    def __call__(self, t: float) -> tuple:
        if not (t >= 0 and t <= 1):
            raise PathError(f"Path unable to extrapolate to parameter [t: {t}], must be in range [0, 1]")
        
        rt = t * self.distance

        start = 0
        for item in self.path:
            end = start + item.distance
            if end >= rt:
                return item((rt - start) / item.distance)
            start = end
        
        raise PathError("huh")

COMMANDS = {
    'M': 2, 'm': 2, # moveto
    'L': 2, 'l': 2, # lineto
    'H': 1, 'h': 1, # horizontal        (pseudo class)
    'V': 1, 'v': 1, # vertical          (pseudo class)
    'C': 6, 'c': 6, # cubic bezier
    'S': 4, 's': 4, # cubic smooth      (pseudo class)
    'Q': 4, 'q': 4, # quadratic bezier
    'T': 2, 't': 2, # smooth qb         (pseudo class)
    'A': 7, 'a': 7, # elliptic arc      (leave to end)
    'Z': 0, 'z': 0, # close line        (... lazy implimentation ok)
}

class PathReader:
    def __init__(self, path: str):
        self.path = [x[0] if len(x[1]) == 0 else int(x[1]) for x in re.findall('([MmLlHhVvCcSsQqTtAaZz])|(-?\d+)', path)]
        self.pos = np.array([0, 0], dtype=np.float32)
        self.start = np.array([0, 0], dtype=np.float32)

    def read_command(self):
        if not len(self.path):
            return []

        if type(self.path[0]) == str:
            tag = self.path[0]
            n = COMMANDS[tag]
            args = np.array(self.path[1:n + 1], dtype=np.float32)
            self.path = self.path[n + 1:]
            return (tag, args)
        else:
            tag = 'l'
            args = np.array(self.path[0:2])
            self.path = self.path[3:]
            return (tag, args)
    
    def normalize(self, command):
        tag, args = command

        begin = self.pos.copy()

        if tag == 'M':
            self.pos = args
            self.start = self.pos.copy()
            return False
        elif tag == 'm':
            self.pos += args
            self.start = self.pos.copy()
            return False
        
        elif tag == 'L':
            self.pos = args
            out = ('L', args)
        elif tag == 'l':
            self.pos += args
            out = ('L', self.pos.copy())
        elif tag == 'H':
            self.pos[0] = args[0]
            out = ('L', self.pos.copy())
        elif tag == 'h':
            self.pos[0] += args[0]
            out = ('L', self.pos.copy())
        elif tag == 'V':
            self.pos[1] = args[0]
            out = ('L', self.pos.copy())
        elif tag == 'v':
            self.pos[1] += args[0]
            out = ('L', self.pos.copy())
        
        elif tag == 'C':
            self.pos = args[-2:]
            out = command
        elif tag == 'c':
            start = args[0:2] + self.pos
            control = args[3:5] + self.pos
            end = args[5:8] + self.pos
            self.pos = end
            start = np.append(start, [control, end])
            out = ('C', start)
        elif tag == 'S':
            start = self.pos.copy()
            control = args[0:2]
            end = args[3:5]
            self.pos = end
            start = np.append(start, [control, end])
            out = ('C', start)
        elif tag == 's':
            start = self.pos.copy()
            control = args[0:2] + self.pos
            end = args[3:5] + self.pos
            self.pos = end
            start = np.append(start, [control, end])
            out = ('C', start)
        
        elif tag == 'z':
            out = ('L', self.start)

        else:
            raise NotImplementedError(f"hey... sorry but tag [{tag}] is not implimented yet")

        tag, args = out
        return (tag, begin, args)

    def __iter__(self):
        while len(self.path) != 0:
            n = self.normalize(self.read_command())
            if n:
                yield n

class Line(Component):
    __slots__ = ['x1', 'y1', 'x2', 'y2', 'distance']
    def __init__(self, A, B):
        self.x1, self.y1 = A
        self.x2, self.y2 = B

        dx = B[0] - A[0]
        dy = B[1] - A[1]

        self.distance = math.sqrt(dx * dx + dy * dy)

    def __call__(self, t):
        def lerp(a, b):
            return a * (1 - t) + b * t
        return (lerp(self.x1, self.x2), lerp(self.y1, self.y2))

class CubicBezier(Component):
    __slots__ = ['sx', 'sy', 'csx', 'csy', 'cex', 'cey', 'ex', 'ey', 'distance']

    def __init__(self, S, CCE):
        self.sx, self.sy = S
        self.csx, self.csy, self.cex, self.cey, self.ex, self.ey = CCE

        self.distance = 0
        dt = 0.001
        for t in np.arange(0, 1, dt):
            x, y = self(t)
            self.distance += math.sqrt(x * x + y * y) * dt

    def __call__(self, t: float) -> tuple:
        nt = 1 - t
        
        a = nt ** 3
        b = 3 * t * (nt ** 2)
        c = 3 * (t ** 2) * nt
        d = t ** 3

        x = a * self.sx + b * self.csx + c * self.cex + d * self.ex
        y = a * self.sy + b * self.csy + c * self.cey + d * self.ey

        return (x, y)

COMMAND_MAP = {
    'L': Line,
    'C': CubicBezier,
}

def compile(component: list) -> Component:
    tag, begin, args = component
    if tag in COMMAND_MAP:
        return COMMAND_MAP[tag](begin, args)

    raise NotImplementedError(f"hey... sorry but tag [{tag}] is not implimented yet and can not be compiled")

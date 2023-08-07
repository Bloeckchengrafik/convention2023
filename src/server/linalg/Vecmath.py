import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def angle(self, other):
        return math.atan2(self.cross(other), self.dot(other))

    def rotate(self, angle):
        return Vector2(
            self.x * math.cos(angle) - self.y * math.sin(angle),
            self.x * math.sin(angle) + self.y * math.cos(angle)
        )

    def distance(self, other):
        return (self - other).length()

    def distance_to_line(self, p1, p2):
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x0, y0 = self.x, self.y
        return abs((x2-x1)*(y1-y0)-(x1-x0)*y2-y1)/(math.sqrt((x2-x1)**2+(y2-y1)**2))
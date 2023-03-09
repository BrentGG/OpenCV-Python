import random


class Meatball:
    radius = 10
    remove = False

    def __init__(self, width):
        self.x = random.randint(0 + self.radius, width - self.radius)
        self.y = self.radius
        self.good = random.choice([True, False])
        self.speed = random.randint(5, 10)

    def move(self):
        self.y += self.speed

    def getPosition(self):
        return self.x, self.y

    def getRadius(self):
        return self.radius

    def isGood(self):
        return self.good

    def setRemove(self):
        self.remove = True

    def getRemove(self):
        return self.remove

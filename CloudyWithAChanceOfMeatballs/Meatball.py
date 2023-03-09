import random


class Meatball:
    remove = False

    def __init__(self, spawnWidth, radius, minSpeed, maxSpeed):
        self.radius = radius
        self.x = random.randint(0 + self.radius, spawnWidth - self.radius)
        self.y = self.radius
        self.good = random.choice([True, False])
        self.speed = random.randint(minSpeed, maxSpeed)

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

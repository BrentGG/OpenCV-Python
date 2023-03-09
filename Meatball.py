import random


class Meatball:
    radius = 10

    def __init__(self, width):
        self.x = random.randint(0 + self.radius, width - self.radius)
        self.y = self.radius
        self.good = random.choice([True, False])
        self.speed = random.randint(1, 5)

    def move(self):
        self.y += self.speed

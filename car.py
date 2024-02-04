import pygame

from random import randint as rnd

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# car_2 -> up
# car_4 -> right
# car_9 -> down
# car_8 -> left

# car_7 -> left+up
# car_3 -> right+up
# car_10 -> right+down
# car_13 -> left+down


class Car:
    def __init__(self, position: tuple[int, int], direction=(1 << UP)):
        self.position = position
        self.direction = direction

        self.sprites = {
            (1 << UP): pygame.image.load("./assets/cars/car_2.png"),
            (1 << UP) | (1 << RIGHT): pygame.image.load("./assets/cars/car_3.png"),
            (1 << RIGHT): pygame.image.load("./assets/cars/car_4.png"),
            (1 << RIGHT) | (1 << DOWN): pygame.image.load("./assets/cars/car_10.png"),
            (1 << DOWN): pygame.image.load("./assets/cars/car_9.png"),
            (1 << DOWN) | (1 << LEFT): pygame.image.load("./assets/cars/car_13.png"),
            (1 << LEFT): pygame.image.load("./assets/cars/car_8.png"),
            (1 << LEFT) | (1 << UP): pygame.image.load("./assets/cars/car_7.png"),
        }

    @property
    def current_image(self):
        return self.sprites[self.direction]

    def update(self): ...

    def move(self):
        x, y = self.position
        nx = 132 / 10
        ny = 101 / 10
        if self.direction & (1 << UP):
            y -= ny / 3
            x -= nx / 2
        if self.direction & (1 << RIGHT):
            x += nx / 2
            y -= ny / 3
        if self.direction & (1 << DOWN):
            y += ny / 3
            x += nx / 2
        if self.direction & (1 << LEFT):
            x -= nx / 2
            y += ny / 3
        self.position = (x, y)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen, camera):
        x, y = self.position
        screen.blit(self.current_image, camera + (x, y))

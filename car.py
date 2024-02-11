import pygame


from random import randint as rnd

from util import pixel_to_tile


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

    def get_grid(self) -> list[tuple[int, int]]:
        x, y = self.position

        nx = 132 / 2 / 2
        ny = 101 / 3 / 2

        grid = [
            (x + nx, y - ny),
            (x + nx, y + ny),
            (x - nx, y + ny),
            (x - nx, y - ny),
            (x + nx, y),
            (x, y + ny),
            (x - nx, y),
            (x, y - ny),
            (x + 2 * nx, y - 2 * ny),
            (x + 2 * nx, y + 2 * ny),
            (x - 2 * nx, y + 2 * ny),
            (x - 2 * nx, y - 2 * ny),
            (x + 2 * nx, y),
            (x, y + 2 * ny),
            (x - 2 * nx, y),
            (x, y - 2 * ny),
            (x + 3 * nx, y - 3 * ny),
            (x + 3 * nx, y + 3 * ny),
            (x - 3 * nx, y + 3 * ny),
            (x - 3 * nx, y - 3 * ny),
            (x + 3 * nx, y),
            (x, y + 3 * ny),
            (x - 3 * nx, y),
            (x, y - 3 * ny),
        ]

        return grid

    def move(self):
        if not self.direction:
            return False

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

        tx, ty = pixel_to_tile((x, y))

        if tx >= 4 or ty >= 4:
            return True

        if tx < 0 or ty < 0:
            return True

        self.position = (x, y)
        return False

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen, camera):
        x, y = self.position
        w, h = self.current_image.get_rect().size
        screen.blit(self.current_image, camera + (x, y) - (w / 2, h / 2))

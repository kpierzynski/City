import pygame

from random import randint as rnd
from pygame import Vector2
import math

from util import pixel_to_tile

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

to_right = {
    (1 << UP): (1 << RIGHT) | (1 << UP),
    (1 << UP) | (1 << RIGHT): (1 << RIGHT),
    (1 << RIGHT): (1 << DOWN) | (1 << RIGHT),
    (1 << RIGHT) | (1 << DOWN): (1 << DOWN),
    (1 << DOWN): (1 << LEFT) | (1 << DOWN),
    (1 << DOWN) | (1 << LEFT): (1 << LEFT),
    (1 << LEFT): (1 << UP) | (1 << LEFT),
    (1 << LEFT) | (1 << UP): (1 << UP),
}

to_left = {
    (1 << UP): (1 << LEFT) | (1 << UP),
    (1 << UP) | (1 << LEFT): (1 << LEFT),
    (1 << LEFT): (1 << DOWN) | (1 << LEFT),
    (1 << LEFT) | (1 << DOWN): (1 << DOWN),
    (1 << DOWN): (1 << RIGHT) | (1 << DOWN),
    (1 << DOWN) | (1 << RIGHT): (1 << RIGHT),
    (1 << RIGHT): (1 << UP) | (1 << RIGHT),
    (1 << RIGHT) | (1 << UP): (1 << UP),
}


class Car:
    def __init__(self, position: tuple[int, int], direction=(1 << UP), map_size=(4, 4)):
        self.position = position
        self.direction = direction
        self.map_size = map_size

        self.acceleration = 2
        self.speed = 0
        self.max_speed = 2

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

    def cast_ray(self, angle, max_distance, check_road):
        x, y = self.position

        is_car_on_road = check_road(self.position)

        d = pygame.math.Vector2(math.cos(angle), -math.sin(angle)).normalize()
        end = (x, y)

        while pygame.math.Vector2((x, y)).distance_to(end) <= max_distance:
            if is_car_on_road:
                if not check_road(end):
                    return end
            else:
                if check_road(end):
                    return end

            end += d

        return end

    def update(self, dt):
        x, y = self.position
        nx = 132 * self.speed * dt
        ny = 101 * self.speed * dt

        if self.speed < 0:
            self.speed = 0

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
        mx, my = self.map_size

        if tx >= mx or ty >= my or tx < 0 or ty < 0:
            self.speed = 0
            return

        self.position = (x, y)

    def turn(self, direction):
        match direction:
            case "left":
                self.direction = to_left[self.direction]
            case "right":
                self.direction = to_right[self.direction]
            case "forward":
                pass
            case _:
                raise ValueError("Invalid direction")

    def accelerate(self, dt):
        if self.speed < self.max_speed:
            self.speed += self.acceleration * dt

    def brake(self, dt):
        if self.speed > 0:
            self.speed -= 1 / 2 * self.acceleration * dt

            if self.speed < 0:
                self.speed = 0

    def draw(self, screen, camera):
        x, y = self.position
        w, h = self.current_image.get_rect().size
        screen.blit(self.current_image, camera + (x, y) - (w / 2, h / 2))

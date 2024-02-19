import pygame

from pygame import Vector2

from map import Map
from details import Details
from car import Car, UP, DOWN, RIGHT, LEFT, to_left, to_right

from math import sqrt, fabs as abs
from random import randint as rnd, random
from math import atan2

from util import tile_to_pixel, pixel_to_tile

from config import CONFIG

COLORS = CONFIG["COLORS"]

angles = {
    (1 << LEFT): atan2(-101 / 3, -132 / 2),
    (1 << UP): atan2(101 / 3, -132 / 2),
    (1 << DOWN): atan2(-101 / 3, 132 / 2),
    (1 << RIGHT): atan2(101 / 3, 132 / 2),
    (1 << DOWN) | (1 << RIGHT): atan2(0, 1),
    (1 << UP) | (1 << LEFT): atan2(0, -1),
    (1 << DOWN) | (1 << LEFT): atan2(-1, 0),
    (1 << UP) | (1 << RIGHT): atan2(1, 0),
}


class Game:
    def __init__(self, map_size=(4, 4)):
        self.map_size = map_size

        self.map = Map(map_size)
        self.car = Car((0, 150), map_size=map_size)

        self.font = pygame.font.Font(None, 36)
        self.details = Details("assets/details")
        self.trees = []

        for x in range(map_size[0]):
            for y in range(map_size[1]):
                if random() < 0.2:
                    px, py = tile_to_pixel((x, y))
                    self.trees.append((px, py + 101 // 2))

        self.game_number = 0

        self.time_elapsed = 0

    def update(self, dt):
        self.map.update()
        self.car.update(dt)

        self.time_elapsed += dt

    def distance(self, v1, v2):
        x, y = v1
        x2, y2 = v2
        return sqrt((x - x2) ** 2 + (y - y2) ** 2)

    def reset(self):
        map_x, map_y = self.map_size

        while True:
            x, y = tile_to_pixel((rnd(1, map_x - 1), rnd(1, map_y - 1)))

            if self.map.get_tile(x, y).kind == "road_empty":
                continue
            self.target_coords = (x, y)
            break

        x, y = tile_to_pixel((rnd(1, map_x - 1), rnd(1, map_y - 1)))
        self.car.position = Vector2(x, y)

        self.car.speed = 0
        self.game_number += 1
        self.time_elapsed = 0

    def get_car_rays(self):
        rays = []

        for angle in [
            angles[self.car.direction],
            angles[to_right[self.car.direction]],
            angles[to_right[to_right[self.car.direction]]],
            angles[to_left[self.car.direction]],
            angles[to_left[to_left[self.car.direction]]],
            angles[to_left[to_left[to_left[to_left[self.car.direction]]]]],
        ]:
            end = self.car.cast_ray(angle, 132, self.map.is_on_road)
            dist = pygame.math.Vector2(self.car.position).distance_to(end)

            rays.append((end, dist))

        return rays

    def draw(self, screen, camera):
        self.map.draw(screen, camera)
        self.car.draw(screen, camera)

        for tree in self.trees:
            x, y = tree
            tw, th = self.details["tree"].get_size()
            screen.blit(self.details["tree"], camera + (x - tw / 2, y - th))

        text = self.font.render(
            f"Game: {self.game_number}, Car: ({self.car.position[0]:.2f},{self.car.position[1]:.2f})",
            True,
            COLORS["BLACK"],
        )
        screen.blit(text, (10, 10))

        text = self.font.render(
            f"Car speed: {self.car.speed:.2f}",
            True,
            COLORS["BLACK"],
        )

        screen.blit(text, (10, 10 + 36 + 10))

        for ray in self.get_car_rays():
            end, _ = ray
            pygame.draw.line(
                screen, (255, 0, 0), camera + self.car.position, camera + end, 1
            )

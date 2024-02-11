import pygame
from pygame import Vector2

import numpy as np

from math import sqrt, fabs as abs
from random import choice, randint as rnd

from sheet import Sheet
from tile import Tile
from map import Map
from road_tiles import Road
from car import Car, UP, RIGHT, DOWN, LEFT
from util import tile_to_pixel

from config import CONFIG

COLORS = CONFIG["COLORS"]
SCREEN = CONFIG["SCREEN"]


class Game:
    def __init__(self, map_size=(4, 4), target_coords=(100, 100)):
        self.map_size = map_size
        self.target_coords = target_coords

        self.map = Map(map_size)
        self.car = Car((0, 150))

        self.font = pygame.font.Font(None, 36)

        self.game_number = 0

    def update(self, dt):
        self.map.update()
        self.car.update(dt)

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

        self.game_number += 1

    def draw(self, screen, camera):
        self.map.draw(screen, camera)
        self.car.draw(screen, camera)

        pygame.draw.circle(screen, COLORS["RED"], camera + self.target_coords, 4)

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


def main():
    pygame.init()
    clock = pygame.time.Clock()

    camera = Vector2(400, 200)

    size = [SCREEN["WIDTH"], SCREEN["HEIGHT"]]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("AI CITY")

    timer_interval = 7500
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, timer_interval)

    game = Game((4, 4))

    dt = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == timer_event:
                game.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game.car.turn("left")
                if event.key == pygame.K_d:
                    game.car.turn("right")

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            camera += (0, 5)
        if pressed[pygame.K_LEFT]:
            camera += (5, 0)
        if pressed[pygame.K_DOWN]:
            camera += (0, -5)
        if pressed[pygame.K_RIGHT]:
            camera += (-5, 0)

        if pressed[pygame.K_w]:
            game.car.accelerate(dt)
        else:
            game.car.brake(dt)

        if pressed[pygame.K_s]:
            game.car.brake(dt)

        game.update(dt)

        screen.fill(COLORS["SKYBLUE"])

        game.draw(screen, camera)

        pygame.display.flip()

        dt = clock.tick(CONFIG["SCREEN"]["FPS"])
        dt /= 1000


if __name__ == "__main__":
    main()

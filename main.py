import pygame
from pygame import Vector2

import numpy as np

from math import sqrt, fabs as abs
from random import choice, randint as rnd

from game import Game

from config import CONFIG

COLORS = CONFIG["COLORS"]
SCREEN = CONFIG["SCREEN"]


def main():
    pygame.init()
    clock = pygame.time.Clock()

    camera = Vector2(400, 200)

    size = (SCREEN["WIDTH"], SCREEN["HEIGHT"])
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("AI CITY")

    timer_interval = 10000
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, timer_interval)

    game = Game((50, 50))

    dt = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == timer_event:
                reseting = False
                if reseting:
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

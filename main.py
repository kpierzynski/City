import pygame
from pygame import Vector2

from math import sqrt

from sheet import Sheet
from tile import Tile
from road_tiles import Road
from car import Car, UP, RIGHT, DOWN, LEFT

from wave_function_collapse import wave_function_collapse, Cell, Rule
from config import CONFIG

COLORS = CONFIG["COLORS"]
SCREEN = CONFIG["SCREEN"]


def main():
    print("Hello, World!")

    # Initialize the game engine
    pygame.init()
    clock = pygame.time.Clock()

    camera = Vector2(0, 0)

    # Set the height and width of the screen
    size = [SCREEN["WIDTH"], SCREEN["HEIGHT"]]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("AI CITY")

    n = 5
    rules = [
        Rule("road_empty", [0, 0, 0, 0]),
        Rule("road_3way", [1, 1, 0, 1]),
        Rule("road_3way_1", [0, 1, 1, 1]),
        Rule("road_3way_2", [1, 0, 1, 1]),
        Rule("road_3way_3", [1, 1, 1, 0]),
        Rule("road_4way", [1, 1, 1, 1]),
        # Rule("road_dead", [1, 0, 0, 0]),
        # Rule("road_dead_1", [0, 1, 0, 0]),
        # Rule("road_dead_2", [0, 0, 0, 1]),
        # Rule("road_dead_3", [0, 0, 1, 0]),
        Rule("road_2way", [0, 1, 0, 1]),
        Rule("road_2way_1", [1, 0, 1, 0]),
        Rule("road_turn", [0, 0, 1, 1]),
        Rule("road_turn_1", [0, 1, 1, 0]),
        Rule("road_turn_2", [1, 0, 0, 1]),
        Rule("road_turn_3", [1, 1, 0, 0]),
    ]
    grid = wave_function_collapse((n, n), rules)

    roads = []
    for item in grid:
        x, y = item.id % n, item.id // n
        if item.kind:
            roads.append(Road(item.kind, (x, y)))
        else:
            roads.append(Road("EMPTY", (x, y)))

    car = Car((400, 200))

    # PyGame main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        direction = 0
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
            direction |= 1 << UP
        if pressed[pygame.K_d]:
            direction |= 1 << RIGHT
        if pressed[pygame.K_s]:
            direction |= 1 << DOWN
        if pressed[pygame.K_a]:
            direction |= 1 << LEFT
        if pressed[pygame.K_SPACE]:
            car.move()

        if direction:
            car.set_direction(direction)

        car.update()

        # Set the screen background
        screen.fill(COLORS["SKYBLUE"])

        for y in range(n - 1, -1, -1):
            for x in range(n):
                roads[y + n * x].draw(screen, camera)

        car.draw(screen, camera)

        # Flip the display
        pygame.display.flip()
        clock.tick(CONFIG["SCREEN"]["FPS"])


if __name__ == "__main__":
    main()

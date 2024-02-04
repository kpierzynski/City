import pygame

from math import sqrt

from sheet import Sheet
from tile import Tile
from road_tiles import Road

from wave_function_collapse import wave_function_collapse, Cell, Rule
from config import CONFIG

COLORS = CONFIG["COLORS"]
SCREEN = CONFIG["SCREEN"]


def main():
    print("Hello, World!")

    # Initialize the game engine
    pygame.init()
    clock = pygame.time.Clock()

    # Set the height and width of the screen
    size = [SCREEN["WIDTH"], SCREEN["HEIGHT"]]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("AI CITY")

    rules = [
        Rule(
            "road_4way",
            {
                "up": ["road_4way", "road_3way_3"],
                "down": ["road_4way", "road_3way_3", "road_dead"],
                "left": ["road_4way", "road_3way_3", "road_2way"],
                "right": ["road_4way", "road_2way"],
            },
        ),
        Rule(
            "road_3way_3",
            {
                "up": ["road_4way", "road_3way_3"],
                "down": ["road_4way", "road_3way_3", "road_dead"],
                "left": ["road_empty", "road_dead"],
                "right": ["road_4way", "road_2way"],
            },
        ),
        Rule(
            "road_2way",
            {
                "up": ["road_empty"],
                "down": ["road_empty", "road_2way"],
                "left": ["road_4way", "road_3way_3", "road_2way"],
                "right": ["road_4way", "road_2way"],
            },
        ),
        Rule(
            "road_dead",
            {
                "up": ["road_4way", "road_3way_3"],
                "down": ["road_empty", "road_2way"],
                "left": ["road_empty", "road_dead"],
                "right": ["road_empty", "road_dead", "road_3way_3"],
            },
        ),
        Rule(
            "road_empty",
            {
                "up": ["road_empty", "road_dead", "road_2way"],
                "down": ["road_empty", "road_2way"],
                "left": ["road_empty", "road_dead"],
                "right": ["road_empty", "road_dead", "road_3way_3"],
            },
        ),
    ]
    n = 6
    tiles = ["road_4way", "road_3way_3", "road_2way", "road_dead", "road_empty"]
    grid = []
    while True:
        try:
            grid = wave_function_collapse((n, n), rules, tiles)
            break
        except:
            ...

    roads = []
    for item in grid:
        x, y = item.id % n, item.id // n
        if item.kind:
            roads.append(Road(item.kind, (x, y)))
        else:
            roads.append(Road("EMPTY", (x, y)))

    # PyGame main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Set the screen background
        screen.fill(COLORS["SKYBLUE"])

        for y in range(n - 1, -1, -1):
            for x in range(n):
                roads[y + n * x].draw(screen)

        # Flip the display
        pygame.display.flip()
        clock.tick(CONFIG["SCREEN"]["FPS"])


if __name__ == "__main__":
    main()

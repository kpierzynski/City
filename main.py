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

    n = 10
    rules = [
        Rule("road_empty", [0, 0, 0, 0]),
        Rule("road_3way", [1, 1, 0, 1]),
        Rule("road_3way_1", [0, 1, 1, 1]),
        Rule("road_3way_2", [1, 0, 1, 1]),
        Rule("road_3way_3", [1, 1, 1, 0]),
    ]
    options = ["road_3way_3", "road_3way_2", "road_3way_1", "road_3way", "road_empty"]
    grid = wave_function_collapse((n, n), rules, options)

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

import pygame
from pygame import Vector2

from math import sqrt

from sheet import Sheet
from tile import Tile
from map import Map
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

    font = pygame.font.Font(None, 36)

    camera = Vector2(400, 200)

    # Set the height and width of the screen
    size = [SCREEN["WIDTH"], SCREEN["HEIGHT"]]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("AI CITY")

    map = Map((4, 4))
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

        if direction:
            car.set_direction(direction)
            car.move()

        x, y = car.position
        car_on_tile = map.get_tile(x, y)
        x, y = car_on_tile.x, car_on_tile.y

        map.update()
        car.update()

        # Set the screen background
        screen.fill(COLORS["SKYBLUE"])

        map.draw(screen, camera, car_on_tile)
        car.draw(screen, camera)

        # draw text
        text = font.render(
            f"Car: ({car.position[0]:.2f},{car.position[1]:.2f}), on: {car_on_tile.kind}",
            True,
            COLORS["BLACK"],
        )
        screen.blit(text, (10, 10))

        # Flip the display
        pygame.display.flip()
        clock.tick(CONFIG["SCREEN"]["FPS"])


if __name__ == "__main__":
    main()

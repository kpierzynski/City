import pygame

from config import CONFIG

TILE = CONFIG["TILE"]


class Tile:
    def __init__(self, image: pygame.Surface, coords: tuple[int, int]) -> None:
        self.image = image

        self.x, self.y = coords
        self.width, self.height = image.get_rect().size

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, (self.x, self.y))

import pygame
from random import choice

from tile import Tile
from sheet import Sheet

sheet = Sheet("assets/roads")


class Road(Tile):
    def __init__(self, kind, coords: tuple[int, int]) -> None:
        image = sheet.get_image(kind)
        self.kind = kind
        w, h = image.get_rect().size
        x, y = coords

        x, y = (x - y) * w / 2, (x + y) * h / 3

        super().__init__(image, (x, y))

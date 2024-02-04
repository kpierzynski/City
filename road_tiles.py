import pygame
from random import choice

from tile import Tile
from sheet import Sheet

sheet = Sheet("assets/roads")


class Road(Tile):
    def __init__(self, kind, coords: tuple[int, int]) -> None:
        image = sheet.get_image(kind)
        w, h = image.get_rect().size
        x, y = coords
        x_offset = w / 2
        y_offset = -h / 3

        x, y = x * w / 2 + x_offset * (y), y * h / 3 + y_offset * (x - 4)
        super().__init__(image, (x, y))

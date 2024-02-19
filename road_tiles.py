import pygame
from random import choice

from tile import Tile
from sheet import Sheet
from util import tile_to_pixel

sheet = Sheet("assets/roads")


class Road(Tile):
    def __init__(self, kind, coords: tuple[int, int]) -> None:
        self.image = sheet.get_image(kind)
        self.kind = kind

        self.x, self.y = tile_to_pixel(coords)

        super().__init__(self.image, (self.x, self.y))

    def _is_dark_color(self, rgb):
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000

        return brightness < 128

    def is_on_road(self, coords: tuple[int, int]) -> bool:
        try:
            pixel = self.image.get_at(coords)
        except IndexError:
            return False

        if self._is_dark_color(pixel):
            return True
        return False


if __name__ == "__main__":
    road = Road("road_4way", (0, 0))
    res = road.image.get_at((65, 31))
    print(res)

import pygame
from random import choice

from tile import Tile
from sheet import Sheet
from util import tile_to_pixel

sheet = Sheet("assets/roads")


class Road(Tile):
    def __init__(self, kind, coords: tuple[int, int]) -> None:
        self.image = sheet.get_image(kind)
        self.mask = sheet.get_mask(kind)
        self.kind = kind

        self.x, self.y = tile_to_pixel(coords)

        super().__init__(self.image, (self.x, self.y))

    def _is_on_road(self, coords: tuple[int, int]) -> bool:
        try:
            pixel = self.image.get_at(coords)
        except IndexError:
            return False

        if pixel[0] == pixel[1] == pixel[2] and 80 < pixel[0] < 120:
            return True
        return False

    def is_on_road(self, coords: tuple[int, int]) -> bool:
        pixel = self.mask.getpixel(coords)

        if pixel < 128:
            return True

        return False


if __name__ == "__main__":
    road = Road("road_4way", (0, 0))
    res = road.image.get_at((65, 31))
    print(res)

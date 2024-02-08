import pygame

from math import fabs as abs

from road_tiles import Road
from util import pixel_to_tile, tile_to_pixel
from wave_function_collapse import wave_function_collapse, Cell, Rule


class Map:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.rules = [
            Rule("road_empty", [0, 0, 0, 0]),
            Rule("road_3way", [1, 0, 1, 1]),
            Rule("road_3way_1", [1, 1, 1, 0]),
            Rule("road_3way_2", [0, 1, 1, 1]),
            Rule("road_3way_3", [1, 1, 0, 1]),
            Rule("road_4way", [1, 1, 1, 1]),
            # Rule("road_dead", [1, 0, 0, 0]),
            # Rule("road_dead_1", [0, 1, 0, 0]),
            # Rule("road_dead_2", [0, 0, 0, 1]),
            # Rule("road_dead_3", [0, 0, 1, 0]),
            Rule("road_2way", [1, 0, 1, 0]),
            Rule("road_2way_1", [0, 1, 0, 1]),
            Rule("road_turn", [0, 1, 1, 0]),
            Rule("road_turn_1", [1, 1, 0, 0]),
            Rule("road_turn_2", [0, 0, 1, 1]),
            Rule("road_turn_3", [1, 0, 0, 1]),
        ]
        self.grid = wave_function_collapse(size, self.rules)

        self.roads = []
        for item in self.grid:
            x, y = item.id % size[0], item.id // size[1]
            self.roads.append(Road(item.kind, (x, y)))

    def __getitem__(self, index: int) -> Road:
        return self.roads[index]

    def is_on_road(self, coords: tuple[int, int]) -> bool:
        cx, cy = coords
        try:
            tile = self.get_tile(cx, cy)
        except:
            return False

        x = abs(cx - tile.x)
        y = abs(cy - tile.y)

        x = int(x)
        y = int(y)

        try:
            is_on_road = tile.is_on_road((x, y))
        except:
            return False

        return is_on_road

    def get_tile(self, x: int, y: int) -> Road:
        iso_x, iso_y = pixel_to_tile((x, y))

        return self.roads[iso_y * self.size[0] + iso_x]

    def update(self) -> None: ...

    def draw(self, screen: pygame.Surface, camera: pygame.Vector2) -> None:
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.roads[y + self.size[0] * x].draw(screen, camera)

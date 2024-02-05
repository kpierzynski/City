import pygame
from road_tiles import Road
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

    def get_tile(self, x: int, y: int) -> Road:
        w, h = 132, 101

        iso_x = (x / (w / 2) + y / (h / 3)) // 2
        iso_y = (y / (h / 3) - x / (w / 2)) // 2

        iso_x = int(iso_x)
        iso_y = int(iso_y)

        return self.roads[iso_y * self.size[0] + iso_x]

    def update(self) -> None: ...

    def draw(self, screen: pygame.Surface, camera: pygame.Vector2, skip) -> None:
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.roads[y + self.size[0] * x] == skip:
                    continue
                self.roads[y + self.size[0] * x].draw(screen, camera)

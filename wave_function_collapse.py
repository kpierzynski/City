from random import randint as rnd
from random import choice


class Cell:
    def __init__(self, id, kind=None, options=[]) -> None:
        self.kind = kind
        self.id = id
        self.options = list(options)

        self.collapsed = False

    def collapse(self):
        self.collapsed = True
        self.kind = choice(self.options)
        self.options = []
        return self.kind

    def __repr__(self) -> str:
        return f"Cell_{self.id}(kind={self.kind}, options={self.options}, collapsed={self.collapsed})\r\n"


class Rule:
    def __init__(self, kind, patterns: dict) -> None:
        self.kind = kind
        self.patterns = patterns

    def __repr__(self) -> str:
        return f"Rule_{self.kind}(patterns={self.patterns})\r\n"


def wave_function_collapse(grid_size: tuple[int, int], rules: list[Rule], tiles: list):
    w, h = grid_size
    grid = [-1 for _ in range(w * h)]
    for i in range(len(grid)):
        grid[i] = Cell(id=i, kind=None, options=tiles)

    while not all(map(lambda cell: cell.collapsed, grid)):
        not_collapsed = list(filter(lambda cell: not cell.collapsed, grid))
        entropy = list(map(lambda cell: len(cell.options), not_collapsed))
        min_entropy = min(entropy)

        pick = choice(
            list(filter(lambda cell: len(cell.options) == min_entropy, not_collapsed))
        )
        x, y = pick.id % w, pick.id // w

        kind = grid[x + y * w].collapse()

        neighbors = {
            "up": (x, y - 1),
            "down": (x, y + 1),
            "left": (x - 1, y),
            "right": (x + 1, y),
        }

        rule = next(filter(lambda r: r.kind == kind, rules))

        for direction, (neighbor_x, neighbor_y) in neighbors.items():
            if neighbor_x < 0 or neighbor_x >= w or neighbor_y < 0 or neighbor_y >= h:
                continue

            if grid[neighbor_x + w * neighbor_y].collapsed:
                continue

            to_remove = []
            for option in grid[neighbor_x + w * neighbor_y].options:
                if option not in rule.patterns[direction]:
                    to_remove.append(option)
                    # grid[neighbor_x + w * neighbor_y].options.remove(option)
            for option in to_remove:
                grid[neighbor_x + w * neighbor_y].options.remove(option)

        print(grid)

    return grid


if __name__ == "__main__":
    rules = [Rule(0, [1, 2]), Rule(1, [0, 2]), Rule(2, [0, 1]), Rule(3, [0, 1, 2])]
    tiles = [0, 1, 2, 3]
    grid = wave_function_collapse((5, 5), rules, tiles)
    print(grid)

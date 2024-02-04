from random import randint as rnd
from random import choice


class Rule:
    def __init__(self, kind, hands: dict) -> None:
        self.kind = kind
        # clockwise up,right,down,left, 1 means connection, 0 means no connection
        self.hands = list(hands)

    def __repr__(self) -> str:
        return f"Rule({self.kind}: {self.hands})\r\n"


class Cell:
    def __init__(self, kind, id, options: list[int]) -> None:
        self.kind = kind
        self.id = id
        self.options = list(options)
        self.collapsed = False

    def collapse(self):
        self.kind = choice(self.options)
        self.collapsed = True
        self.options = [self.kind]
        return self.kind

    def __repr__(self) -> str:
        return f"Cell({self.kind}): collapsed={self.collapsed}, options={self.options})\r\n"


def wave_function_collapse(size: tuple[int, int], rules: list[Rule], all_options: list):
    w, h = size
    size = w * h
    grid = [Cell(None, id, all_options) for id in range(w * h)]

    # loopy
    while True:
        not_collapsed = list(filter(lambda cell: not cell.collapsed, grid))

        if len(not_collapsed) == 0:
            break

        entropy_grid = map(lambda cell: len(cell.options), not_collapsed)
        min_entropy = min(entropy_grid)

        lowest_entropy_cells = list(
            filter(lambda cell: len(cell.options) == min_entropy, grid)
        )

        pick = choice(lowest_entropy_cells)

        x, y = pick.id % w, pick.id // w

        cell = grid[x + y * w]
        cell.collapse()

        neighbors = {
            0: (0, -1),
            1: (1, 0),
            2: (0, 1),
            3: (-1, 0),
        }

        rule = next(filter(lambda r: r.kind == cell.kind, rules))

        for direction, (nx, ny) in neighbors.items():
            cx, cy = x + nx, y + ny

            if cx < 0 or cx >= w or cy < 0 or cy >= h:
                continue

            neighbor = grid[cx + cy * w]

            if neighbor.collapsed:
                continue

            to_remove = []
            for option in neighbor.options:
                option_rule = next(filter(lambda r: r.kind == option, rules))

                if rule.hands[direction] != option_rule.hands[(direction + 2) % 4]:
                    to_remove.append(option)

            for option in to_remove:
                neighbor.options.remove(option)

    return grid


if __name__ == "__main__":
    rules = [
        Rule("up", [1, 1, 0, 1]),
        Rule("right", [1, 1, 1, 0]),
        Rule("down", [0, 1, 1, 1]),
        Rule("left", [1, 0, 1, 1]),
        Rule("empty", [0, 0, 0, 0]),
    ]
    options = ["up", "right", "down", "left", "empty"]
    grid = wave_function_collapse((3, 3), rules, options)

    print(grid)

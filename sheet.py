import pygame

from wave_function_collapse import Rule
from PIL import Image
from pathlib import Path

from random import choice


class Sheet:
    def __init__(self, path: str) -> None:
        self.tiles = {}

        for element in Path(path).iterdir():
            if element.is_file():
                continue

            if element.stem not in self.tiles:
                self.tiles[element.stem] = []

            for file in element.iterdir():
                if file.is_file() and file.suffix == ".png":
                    img = pygame.image.load(file)
                    self.tiles[element.stem].append(img)

    def get_image(self, kind: str) -> pygame.Surface:
        return choice(self.tiles[kind])

    def get_rules(self) -> list[str]:
        keys = self.tiles.keys()

        rules = []

        for key in keys:
            rules.append(Rule(key, [num for num in key]))

        return rules


if __name__ == "__main__":
    sheet = Sheet("assets/roads")
    print(sheet.tiles)

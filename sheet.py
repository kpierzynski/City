import pygame

from pathlib import Path


class Sheet:
    def __init__(self, path: str) -> None:
        self.tiles = {}

        for file in Path(path).iterdir():
            if file.is_file() and file.suffix == ".png":
                img = pygame.image.load(file)
                self.tiles[file.stem] = img

    def get_image(self, kind: str) -> pygame.Surface:
        return self.tiles[kind]


if __name__ == "__main__":
    sheet = Sheet("assets/roads")
    print(sheet.tiles)
    print(sheet.tiles["road_4way"].get_rect().size)

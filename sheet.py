import pygame

from PIL import Image
from pathlib import Path


class Sheet:
    def __init__(self, path: str) -> None:
        self.tiles = {}
        self.masks = {}

        for file in Path(path).iterdir():
            if file.is_file() and file.suffix == ".png":
                if "mask" in file.stem:
                    img = Image.open(file).convert("L")
                    self.masks[file.stem[:-5]] = img
                else:
                    img = pygame.image.load(file)
                    self.tiles[file.stem] = img

    def get_image(self, kind: str) -> pygame.Surface:
        return self.tiles[kind]

    def get_mask(self, kind: str) -> Image.Image:
        return self.masks[kind]


if __name__ == "__main__":
    sheet = Sheet("assets/roads")
    print(sheet.tiles)
    print(sheet.tiles["road_4way"].get_rect().size)

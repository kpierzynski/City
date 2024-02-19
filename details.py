import pygame

from pathlib import Path


class Details:
    def __init__(self, path: str) -> None:
        self.details = {}

        for file in Path(path).iterdir():
            if file.is_file() and file.suffix == ".png":
                img = pygame.image.load(file)
                self.details[file.stem] = img

    def __getitem__(self, key: str) -> pygame.Surface:
        return self.details[key]

    def get_image(self, kind: str) -> pygame.Surface:
        return self.tiles[kind]

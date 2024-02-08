"""
        w, h = 132, 101

        iso_x = (x / (w / 2) + y / (h / 3)) // 2
        iso_y = (y / (h / 3) - x / (w / 2)) // 2

        iso_x = int(iso_x)
        iso_y = int(iso_y)

        return self.roads[iso_y * self.size[0] + iso_x]
"""


def pixel_to_tile(coords: tuple[int, int]) -> tuple[int, int]:
    x, y = coords
    w, h = 132, 101

    iso_x = (x / (w / 2) + y / (h / 3)) // 2
    iso_y = (y / (h / 3) - x / (w / 2)) // 2

    iso_x = int(iso_x)
    iso_y = int(iso_y)

    return (iso_x, iso_y)


def tile_to_pixel(coords: tuple[int, int]) -> tuple[int, int]:
    x, y = coords
    w, h = 132, 101

    x, y = (x - y) * w / 2, (x + y) * h / 3

    x -= w / 2

    return (x, y)

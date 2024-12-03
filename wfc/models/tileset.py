from dataclasses import dataclass
from functools import cached_property

import numpy as np


@dataclass(frozen=True)
class Tile:
    uid: int
    pixels: np.ndarray
    frequency: float

    @cached_property
    def size(self) -> int:
        return self.pixels.shape[0]

    def __hash__(self):
        return hash(self.uid)


@dataclass(frozen=True)
class Tileset:
    tile_size: int
    tiles: dict[int, Tile]
    color_pallet: set[int]

    @property
    def n_tiles(self) -> int:
        return len(self.tiles)

    @property
    def n_colors(self) -> int:
        return len(self.color_pallet)

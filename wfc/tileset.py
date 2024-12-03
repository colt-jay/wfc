from dataclasses import dataclass

import numpy as np
import structlog

log = structlog.get_logger()


@dataclass(frozen=True)
class Tile:
    uid: int
    pixels: np.ndarray
    frequency: float

    @property
    def size(self) -> int:
        return self.pixels.shape[0]

    def __hash__(self):
        return hash(self.uid)


Tileset = dict[int, Tile]


def convert_int_tensor_to_tileset(
    int_tensor: np.ndarray,
    tile_size: int = 3,
) -> Tileset:
    """Convert a 2D int tensor to a tileset of tiles."""
    color_pallet: set[int] = set(list(map(int, np.unique(int_tensor.flatten()))))
    n_pixels: int = int_tensor.shape[0] * int_tensor.shape[1]

    tile_fingerprints = set()
    tile_pixels_map = {}
    tile_count = {}
    log.info("Building tileset of %sx%s tiles from the sample.", tile_size, tile_size)
    for i in range(int_tensor.shape[0]):
        for j in range(int_tensor.shape[1]):
            tile_pixels = np.empty(shape=(tile_size, tile_size), dtype=np.int32)

            for k in range(tile_size):
                for l in range(tile_size):
                    # Use modulo to wrap around the edges of the sample
                    tile_pixels[k, l] = int_tensor[
                        (i + k) % int_tensor.shape[0],
                        (j + l) % int_tensor.shape[1],
                    ]
                    fingerprint = tuple(tile_pixels.flatten())

            # print(fingerprint)
            # print(tile_pixels)
            tile_fingerprints.add(fingerprint)
            tile_count[fingerprint] = tile_count.get(fingerprint, 0) + 1
            if fingerprint not in tile_pixels_map:
                tile_pixels_map[fingerprint] = tile_pixels

    tiles = set(
        Tile(
            uid=i,
            pixels=tile_pixels_map[fingerprint],
            frequency=tile_count[fingerprint] / n_pixels,
        )
        for i, fingerprint in enumerate(tile_fingerprints)
    )

    tileset = {tile.uid: tile for tile in tiles}

    log.info("Number of pixels: %s", n_pixels)
    log.info("Number of tiles: %s", len(tileset))
    log.info("Unique colors (%s): %s", len(color_pallet), color_pallet)

    return tileset

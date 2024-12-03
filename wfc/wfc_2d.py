import functools
import json
import pprint
from math import inf
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import structlog

from wfc.candidates import compute_candidates
from wfc.image_tools import convert_rgb_tensor_to_int_tensor, load_image_to_rgb_tensor
from wfc.models.tileset import Tileset
from wfc.tileset import convert_int_tensor_to_tileset

log = structlog.get_logger()


def wfc_2d(
    source_sample: Path,
    *,
    target_shape: tuple[int, int] = (100, 100),
    tile_size: int = 3,
):
    """Run the WFC Algorithm using the given sample and a target array.

    :param source_sample: Path to the source sample file.
    :param shape: Desired shape of the generated 2D Tensor.
    """
    log.info("Running 2D WFC Algorithm.")
    log.info("Target shape: %s", target_shape)

    rgb_sample: np.ndarray = load_image_to_rgb_tensor(source_sample)
    int_sample: np.ndarray = convert_rgb_tensor_to_int_tensor(rgb_sample)
    tileset: Tileset = convert_int_tensor_to_tileset(int_sample, tile_size)
    tileset_candidates = compute_candidates(tileset)
    tile_candidates = tileset_candidates[0]

    # _, figs = plt.subplots(5, 10)
    # for i, offset in enumerate(tile_candidates):
    #     if i >= 5:
    #         break
    #     for j, tile_id in enumerate(tile_candidates[offset]):
    #         if j >= 10:
    #             break

    #         pixels = tileset.tiles[tile_id].pixels
    #         pixels[*offset] = -1

    #         figs[i][j].imshow(pixels)
    # plt.show()

    # propagate = functools.partial(_propagate, rules)
    # random_collapse = functools.partial(_random_collapse, rules)

    # entropy = inf
    # while entropy > 0:
    #     output_tensor = random_collapse(output_tensor)
    #     output_tensor = propagate(output_tensor)
    #     entropy = compute_entropy(output_tensor)

import json

import structlog

from wfc.models.tileset import Tile, Tileset

log = structlog.get_logger()

Offset = tuple[int, int]
TileCandidates = dict[Offset, set[int]]
TilesetCandidates = dict[int, TileCandidates]


def is_candidate_overlap_valid(
    tile_a: Tile, tile_b: Tile, offset: tuple[int, int]
) -> bool:
    """Check if the overlap between two tiles is compatible."""
    """
            for y1 in 0..DIMENSION.height as isize {
            for x1 in 0..DIMENSION.width as isize {
                let (x_offset, y_offset) = offset;
                let x2 = x1 + x_offset;
                let y2 = y1 + y_offset;
                if x2 < 0 || x2 >= 3 || y2 < 0 || y2 >= 3 {
                    continue;
                }
                let pixel_1 = other.get_pixel(Idx2D::from((x1 as usize, y1 as usize)));
                let pixel_2 = self.get_pixel(Idx2D::from((x2 as usize, y2 as usize)));
                if pixel_1 == color::WILDCARD || pixel_2 == color::WILDCARD {
                    continue;
                }
                if pixel_1 != pixel_2 {
                    return false;
                }
            }
        }
        true
    """
    _range = range(tile_a.size)
    pixel_indicies = [(x, y) for x in _range for y in _range]

    for x1, y1 in pixel_indicies:
        x_offset, y_offset = offset
        x2 = x1 + x_offset
        y2 = y1 + y_offset

        if x2 < 0 or x2 >= tile_a.size or y2 < 0 or y2 >= tile_a.size:
            continue

        pixel_a = tile_a.pixels[x1, y1]
        pixel_b = tile_b.pixels[x2, y2]

        if pixel_a != pixel_b:
            return False

    return True


def compute_candidates(tileset: Tileset) -> TilesetCandidates:
    """Compute the adjacency rules for the given tileset."""
    log.info("Computing rules for the given tileset.")

    n_adjacency_positions = (((tileset.tile_size * 2) - 1) ** 2) - 1
    log.info("Number of adjacency positions: %s", n_adjacency_positions)

    n_potential_candidates_per_tile = n_adjacency_positions * tileset.n_tiles
    log.info(
        "Number of potential candidates per tile: %s", n_potential_candidates_per_tile
    )

    n_potential_candidates = n_potential_candidates_per_tile * tileset.n_tiles
    log.info("Number of potential candidates: %s", n_potential_candidates)

    offset_range = range(1 - tileset.tile_size, tileset.tile_size)
    offsets: list[tuple[int, int]] = [
        (i, j) for i in offset_range for j in offset_range
    ]

    candidiates = {}
    n_candidiates = 0

    for tile_id in tileset.tiles:
        tile_candidiates = candidiates.get(tile_id, {})

        for offset in offsets:
            if offset == (0, 0):
                continue

            offset_candidiates = tile_candidiates.get(offset, set())

            for candidate_tile_id in tileset.tiles:
                tile = tileset.tiles[tile_id]
                candidate_tile = tileset.tiles[candidate_tile_id]
                if is_candidate_overlap_valid(tile, candidate_tile, offset):
                    offset_candidiates.add(candidate_tile_id)
                    n_candidiates += 1

            tile_candidiates[offset] = offset_candidiates

        candidiates[tile.uid] = tile_candidiates

    log.info("Number of computed candidates: %s", n_candidiates)

    return candidiates

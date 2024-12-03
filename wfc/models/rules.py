from wfc.models.tileset import Tileset


class TilesetRules:
    tileset: Tileset
    rules: dict[int, set[int]]

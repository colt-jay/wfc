from pathlib import Path

import numpy as np
import pytest

from wfc.image_tools import load_image_to_rgb_tensor, rgb_to_hex


def test_load_image_to_rgb_tensor_file_not_found():
    # WITH
    test_image_path = Path("tests/data/notfound.png")

    # WHEN & THEN
    with pytest.raises(FileNotFoundError):
        load_image_to_rgb_tensor(test_image_path)


def test_load_image_to_rgb_tensor():
    # WITH
    test_image_path = Path("tests/data/testimage.png")

    # WHEN
    image_tensor = load_image_to_rgb_tensor(test_image_path)

    # THEN
    assert image_tensor.shape == (12, 62, 3)
    assert image_tensor.dtype == "uint8"
    assert int(image_tensor[0, 0, 0]) == 126


@pytest.mark.parametrize(
    "rgb_vector, hex_code",
    [
        ([0, 0, 0], "#000000"),
        ([255, 255, 255], "#ffffff"),
        ([25, 56, 123], "#19387b"),
        ([2, 3, 4], "#020304"),
    ],
)
def test_rgb_to_hex(rgb_vector, hex_code):
    # WITH
    np_rgb_vector = np.array(rgb_vector, dtype=np.uint)

    # WHEN
    _hex_code = rgb_to_hex(np_rgb_vector)

    # THEN
    assert _hex_code == hex_code

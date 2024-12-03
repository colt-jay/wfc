from pathlib import Path

import cv2
import numpy as np
import structlog

log = structlog.get_logger()


def load_image_to_rgb_tensor(image_path: Path) -> np.ndarray:
    """Load an image from disk as a 3 channel numpy tensor."""
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    log.info("Loading image: %s", image_path)
    rgb_tensor: np.ndarray = cv2.imread(str(image_path))
    log.info("Image shape (hight, width, channels): %s", rgb_tensor.shape)

    return rgb_tensor


def rgb_to_hex(rgb_vector: np.ndarray) -> str:
    """Return color as #rrggbb for the given color values."""
    return "#%02x%02x%02x" % (rgb_vector[0], rgb_vector[1], rgb_vector[2])


def rgbtoint32(rgb: list[int]) -> int:
    color = 0
    for c in rgb[::-1]:
        color = (color << 8) + c
    return color


def int32torgb(color_int: int) -> list[int]:
    rgb = []
    for _ in range(3):
        rgb.append(color & 0xFF)
        color = color >> 8
    return rgb


def convert_rgb_tensor_to_int_tensor(rgb_tensor: np.ndarray) -> np.ndarray:
    """Convert a 3 channel RGB tensor to a 2D tensor of int color values."""
    if rgb_tensor.ndim != 3 or rgb_tensor.shape[2] != 3:
        raise ValueError("Input tensor must be a 3D, 3 channel RGB tensor.")
    log.info("Converting RGB tensor to 2D int tensor.")
    f = lambda x: rgbtoint32(x.tolist())
    return np.apply_along_axis(f, 2, rgb_tensor)


def load_image_to_int_tensor(image_path: Path) -> np.ndarray:
    """Load an image from disk as a 2D tensor of hex color values."""
    rgb_tensor = load_image_to_rgb_tensor(image_path)
    return convert_rgb_tensor_to_int_tensor(rgb_tensor)


def convert_int_tensor_to_rgb_tensor(int_tensor: np.ndarray) -> np.ndarray:
    """Convert a 2D tensor of hex color values to a 3 channel RGB tensor."""
    if int_tensor.ndim != 2:
        raise ValueError("Input tensor must be a 2D tensor.")
    log.info("Converting 2D hex tensor to RGB tensor.")
    return np.vectorize(int32torgb)(int_tensor)

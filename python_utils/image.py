import numpy as np
from PIL import Image


def get_image(filepath):
    """Retrieves a PIL Image from filepath."""
    if isinstance(filepath, Image.Image):
        return filepath
    image = Image.open(filepath)
    return image


def array_to_image(X):
    if X.ndim == 3 and X.shape[-1] == 1:
        X = np.squeeze(X)
    return Image.fromarray(X)
import numpy as np
from scipy.ndimage import convolve
from skimage.transform import resize

def upscale_chunk(chunk: np.ndarray[float], scale_factor: float):
    """
    Upscales a chunk of the image by the specified scale factor.

    Args:
        chunk (ndarray): The input image chunk to be upscaled. Shape: (Height, Width, Depth).
        scale_factor (float): The scale factor to upscale the chunk.

    Returns:
        ndarray: The upscaled chunk. Shape: (New_Height, New_Width, Depth).
    """
    # Check if the input is grayscale (2D)
    if len(chunk.shape) == 2:
        # Expand dimensions to handle grayscale as 3D with a single channel
        chunk = chunk[..., np.newaxis]

    height, width, depth = chunk.shape
    new_height, new_width = int(height * scale_factor), int(width * scale_factor)

    # Upscale each channel individually
    upscaled_chunk = np.zeros((new_height, new_width, depth), dtype=chunk.dtype)
    for d in range(depth):
        upscaled_chunk[:, :, d] = resize(
            chunk[:, :, d],
            (new_height, new_width),
            order=3,  # Bicubic interpolation
            mode="reflect",
            preserve_range=True
        )

    return upscaled_chunk


def apply_sharpening(image: np.ndarray[float], strength: float=1.0) -> np.ndarray:
    """
    Applies a sharpening filter to the given image or single channel.

    Args:
        image (ndarray): The input image or channel to sharpen.
        strength (float): The strength of the sharpening effect (default: 1.0).

    Returns:
        ndarray: The sharpened image or channel.
    """
    # sharpening kernel
    sharpening_kernel: np.ndarray[int] = np.array(
        [
            [0, -1, 0],
            [-1, 5 + strength, -1],
            [0, -1, 0]
        ]
    )

    # Apply convolution with the sharpening kernel
    sharpened_image = convolve(image, sharpening_kernel, mode="reflect")

    # Clip values to valid range (important for TIFF files)
    return np.clip(sharpened_image, 0, 255).astype(image.dtype)

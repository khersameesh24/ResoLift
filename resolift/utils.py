import scipy.ndimage as nd

def upscale_chunk(chunk, scale_factor):
    """
    Upscales a chunk of the image using interpolation.

    Parameters:
        chunk (ndarray): The image chunk to be upscaled.
        scale_factor (float): The scaling factor for resolution increase.

    Returns:
        ndarray: The upscaled chunk.
    """
    return nd.zoom(chunk, scale_factor, order=3)

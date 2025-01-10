from pathlib import Path
import tifffile as tiff
import numpy as np
from multiprocessing import Pool
from .utils import upscale_chunk, apply_sharpening


class TiffUpscaler:
    def __init__(self, input_path, output_path, scale_factor=2.0, chunk_size=1024, sharpen_strength=0.5):
        """
        Initializes the TiffUpscaler.

        ARgs:
            input_path (path): Path to the input TIFF file.
            output_path (path): Path to save the upscaled TIFF file.
            scale_factor (float): Factor by which to upscale the image.
            chunk_size (int): Number of rows to process in each chunk.
            sharpen_strength (float): Strength of the sharpening effect (default: 1.0).
        """
        self.input_path: Path = input_path
        self.output_path: Path = output_path
        self.scale_factor: float = scale_factor
        self.chunk_size: int = chunk_size
        self.sharpen_strength: float = sharpen_strength

    def process_chunk(self, args) -> np.ndarray:
        """
        Processes a single chunk (used in parallel execution).

        Args:
            args (tuple): A tuple containing (chunk, scale_factor).

        Returns:
            ndarray: The upscaled chunk.
        """
        chunk, scale_factor = args
        return upscale_chunk(chunk, scale_factor)

    def upscale(self) -> None:
        """
        Upscales the 3D TIFF image using multicore processing and applies sharpening.
        """
        # Open the input TIFF file
        with tiff.TiffFile(self.input_path) as tif:
            image: np.ndarray = tif.asarray()

        # Get the shape of the image (Height, Width, Depth)
        # Convert 2D grayscale to 3D for consistency
        if len(image.shape) == 2:
            image: np.ndarray = image[..., np.newaxis]

        height: int
        width: int
        depth: int

        height, width, depth = image.shape
        print(f"Image Shape: {image.shape}")
        new_height, new_width = int(height * self.scale_factor), int(width * self.scale_factor)

        # Prepare output array with upscaled dimensions
        upscaled_image: np.ndarray[float] = np.zeros((new_height, new_width, depth), dtype=image.dtype)

        # Split the image into chunks along the rows
        print("Splitting image into chunks")
        chunks: list = [
            (image[start_row:min(start_row + self.chunk_size, height), :, :], self.scale_factor)
            for start_row in range(0, height, self.chunk_size)
        ]

        # Process chunks in parallel using a multiprocessing Pool
        print("Upscaling image chunks")
        with Pool() as pool:
            upscaled_chunks: list[np.ndarray] = pool.map(self.process_chunk, chunks)

        # Merge upscaled chunks into the output image
        print("Merging image chunks")
        current_row: int = 0
        for upscaled_chunk in upscaled_chunks:
            chunk_height = upscaled_chunk.shape[0]

            upscaled_image[current_row:current_row + chunk_height, :, :] = upscaled_chunk
            current_row += chunk_height

        # Apply sharpening to the entire upscaled image
        print("Sharpening final image")
        sharpened_image: np.ndarray[float] = np.zeros_like(upscaled_image)
        for d in range(depth):
            sharpened_image[:, :, d] = apply_sharpening(upscaled_image[:, :, d], self.sharpen_strength)

        # Save the sharpened image to a TIFF file
        print(f"Saving final image at {self.output_path}")

        with tiff.TiffWriter(self.output_path) as writer:
            writer.write(sharpened_image, photometric="rgb" if depth == 3 else "minisblack")

        return None

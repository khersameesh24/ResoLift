from pathlib import Path
import tifffile
from resolift.utils import upscale_chunk

class TiffUpscaler:
    def __init__(self, input_path, output_path, scale_factor, chunk_size) -> None:
        """
        Initializes the TiffUpscaler class

        Args:
            input_path (str): Path to the input TIFF file.
            output_path (str): Path to save the upscaled TIFF file.
            scale_factor (float): The scaling factor for resolution increase.
            chunk_size (int): The size of each chunk to process (in rows).
        """
        self.input_path: Path = input_path
        self.output_path: Path = output_path
        self.scale_factor: float = scale_factor
        self.chunk_size: int = chunk_size
        self.original_shape = None

    def _load_image(self) -> None:
        """
        Loads the TIFF image and retrieves metadata
        """
        print("Loading image...")
        with tifffile.TiffFile(self.input_path) as tif:
            self.image = tif.asarray()
            self.metadata = tif.pages[0].tags
        self.original_shape = self.image.shape
        print(f"Original shape: {self.original_shape}")

    def _process_and_save(self):
        """
        Processes the image in chunks and writes the upscaled data to a new TIFF file
        """
        print("Processing and saving upscaled image...")
        with tifffile.TiffWriter(self.output_path, bigtiff=True) as tiff_writer:
            for start_row in range(0, self.original_shape[0], self.chunk_size):
                end_row = min(start_row + self.chunk_size, self.original_shape[0])
                chunk = self.image[start_row:end_row, :]

                # Upscale a chunk
                upscaled_chunk = upscale_chunk(chunk, self.scale_factor)

                # Write the upscaled chunk
                tiff_writer.write(upscaled_chunk, contiguous=True)
                print(f"Processed rows {start_row} to {end_row}")

        print(f"Upscaled image saved to {self.output_path}")

    def upscale(self):
        """Main method to upscale the TIFF image."""
        self._load_image()
        self._process_and_save()

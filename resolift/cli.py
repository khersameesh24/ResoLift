import sys
import argparse
from resolift.resolift import TiffUpscaler
from importlib.metadata import version


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the TIFF upscaler.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Upscale (enhance resolution) large TIFF images with chunk-based processing.",
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the input TIFF file."
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Path to save the upscaled TIFF file."
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=float,
        default=2.0,
        help="Scaling factor for resolution increase (default: 2.0).",
    )
    parser.add_argument(
        "-c",
        "--chunk-size",
        type=int,
        default=1024,
        help="Number of rows to process at a time (default: 1024).",
    )
    parser.add_argument('-v', '--version', action='version', version=version('resolift'))

    return parser.parse_args()

def run_upscaler() -> None:
    """
    Runs the TIFF upscaling process using command-line arguments.
    """
    args  = parse_arguments()
    
    upscaler = TiffUpscaler(args.input, args.output, args.scale, args.chunk_size)
    upscaler.upscale()

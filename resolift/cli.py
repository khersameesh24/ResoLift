import argparse
from resolift.resolift import TiffUpscaler

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for ResoLift.
    """
    parser = argparse.ArgumentParser(
        prog="ResoLift",
        description="Upscale large TIFF images using chunk-based processing and sharpening.",
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
    parser.add_argument(
        "-p",
        "--sharpen",
        type=float,
        default=1.0,
        help="Strength of the sharpening effect (default: 1.0).",
    )
    return parser.parse_args()

def run_upscaler() -> None:
    """
    Runs ResoLift using command-line arguments.
    """
    args = parse_arguments()
    upscaler = TiffUpscaler(
        args.input, args.output, args.scale, args.chunk_size, args.sharpen
    )
    upscaler.upscale()

## ResoLift

Upscale large TIFFs using chunk-based image processing and sharpening

Helper package for the (Spatialxe)[https://github.com/nf-core/spatialxe] pipeline.

The package can be used as a pre-processing step in the image-based segmentation approach in the spatialxe pipeline and is available as a local nextflow module in the pipeline.

For a standalone use case scenario

```bash
$ resolift --help
    usage: ResoLift [-h] -i INPUT -o OUTPUT [-s SCALE] [-c CHUNK_SIZE] [-p SHARPEN]

    Upscale large TIFF images using chunk-based processing and sharpening.

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
                            Path to the input TIFF file.
    -o OUTPUT, --output OUTPUT
                            Path to save the upscaled TIFF file.
    -s SCALE, --scale SCALE
                            Scaling factor for resolution increase (default: 2.0).
    -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                            Number of rows to process at a time (default: 1024).
    -p SHARPEN, --sharpen SHARPEN
                            Strength of the sharpening effect (default: 1.0).

```

Simplest command line use case

```bash
$ resolift --input <input.tif> --output <output.tif>
```

To increase chunk size for very large tiff (default: 1024)

```bash
$ resolift --input <input.tif> --output <output.tif> --chunk-size 2048
```

To increase sharpness strength (default: 0.5)

```bash
$ resolift --input <input.tif> --output <output.tif>
--sharpen 1.0
```

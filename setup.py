from setuptools import setup, find_packages

setup(
    name="resolift",
    version="1.0",
    description="ResoLift: Upscale (enhance resolution) large TIFF images with chunk-based processing.",
    author="Sameesh Kher",
    author_email=["khersameesh24@gmail.com", "sameesh.kher@dkfz-heidelberg.de"],
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "tifffile",
    ],
    entry_points={
        "console_scripts": [
            "resolift=resolift.cli:run_upscaler",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)



# version-1-imagemagick.py

- Version to fast test it.
- Hardcoded: url to folder with tiles, number of rows and columns.
- Uses external tool `ImageMagick` to merge tiles.


# version-1-pillow.py

- Version to fast test it.
- Hardcoded: url to folder with tiles, zoom level, number of rows and columns.
- Uses python module `pillow` to merge tiles.

# version-2-imagemagick.py

- Version to fast test it.
- Hardcoded: url to folder with tiles (second url in commented).
- Hardcoded: zoom level, number of rows and columns but now as variables.
- Uses external tool `ImageMagick` to merge tiles.


# version-3-pillow-args-xml.py

- Use `argparse` to run with parameters: url to page with map, output file, local folder for tiles,
- Finds url to folder with tiles.
- Loads `.xml` to find zoom level, image size and calculate number of rows and columns.
- Uses python module `pillow` to merge tiles.


# version-X-imagemagick-args.py

- Some cleanings in code.


# run-version-3.sh

runs version 3 with two urls to test it


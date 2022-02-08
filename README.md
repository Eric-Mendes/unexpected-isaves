# Unexpected Image Saves
[![PyPI version](https://badge.fury.io/py/unexpected-isaves.svg)](https://badge.fury.io/py/unexpected-isaves)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/unexpected-isaves)](https://pypi.org/project/unexpected-isaves/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/Eric-Mendes/unexpected-isaves/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Unconventional ways to save an image :smile:

Have you ever been bored by the same old `.png`, `.jpg`, `.jpeg`, `.gif` and all other image extensions? Have you ever wanted something different - goofy - but also clever? Then this is the package for you! :sparkles:

## What does this package do :thinking:
With this package you can save any image opened with the [`PIL.Image` module](https://pillow.readthedocs.io/en/stable/reference/Image.html) on a given `path` as a
- Spreadsheet;
- Minecraft Pixel Art Datapack.

You can also manipulate your image's colors with the function available at the `image_utilities` module. Just keep in mind that it is quite an expensive function and takes a long time to run.

## How to use it :computer:
First you install it in your environment like so
```bash
pip install unexpected-isaves
```
Then you can start using it already! Open any image you've got locally with PIL and try to save it using our functions!
```python
from unexpected_isaves import save_image
from PIL import Image


save_image.to_excel(
    image=Image.open("my_image.png"),
    path="/home/user/Documents/my_image.xlsx"
)
```

## Contributing :pencil:
Contributions are welcome and appreciated. Make sure to read our [guide for contributing](https://github.com/Eric-Mendes/unexpected_isaves/blob/main/CONTRIBUTING.md) and don't forget to check out our [code of conduct](https://github.com/Eric-Mendes/unexpected_isaves/blob/main/CODE_OF_CONDUCT.md).

Have fun!

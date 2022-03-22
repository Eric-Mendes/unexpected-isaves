<div id="header" align="center">
    <img src="https://user-images.githubusercontent.com/42689328/159303554-70eaea67-8840-4889-8683-b54fa7b815cb.png" alt="unexpected-isaves" width=300 />
    <h1> Unexpected Image Saves </h1>
    <a href="https://badge.fury.io/py/unexpected-isaves">
        <img src="https://badge.fury.io/py/unexpected-isaves.svg" alt="PyPI version"/>
    </a>
    <a href="https://pypi.org/project/unexpected-isaves/">
        <img src="https://img.shields.io/pypi/dm/unexpected-isaves" alt="PyPI - Downloads"/>
    </a>
    <a href="https://github.com/Eric-Mendes/unexpected-isaves/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/license-MIT-blue" alt="License"/>
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"/>
    </a>
</div>
<br/>
Unconventional ways to save an image :smile:

Have you ever been bored by the same old `.png`, `.jpg`, `.jpeg`, `.gif` and all other image extensions? Have you ever wanted something different - goofy - but also clever? Then this is the package for you! :sparkles:

## Table of contents
- [What does this package do :thinking:](https://github.com/Eric-Mendes/unexpected-isaves#what-does-this-package-do-thinking);
- [How to use it :computer:](https://github.com/Eric-Mendes/unexpected-isaves#how-to-use-it-computer);
- [Why unexpected-isaves?](https://github.com/Eric-Mendes/unexpected-isaves#why-unexpected-isaves);
- [Contributing :pencil:](https://github.com/Eric-Mendes/unexpected-isaves#contributing-pencil).

<hr/>

## What does this package do :thinking:
With this package you can save any image opened with the [`PIL.Image` module](https://pillow.readthedocs.io/en/stable/reference/Image.html) on a given `path` as a
- Spreadsheet:
![this_is_fine](https://user-images.githubusercontent.com/42689328/159305173-7946f75e-999d-479d-8ac6-cd09e89097c0.png)

- Minecraft Pixel Art Datapack:
![naruto](https://user-images.githubusercontent.com/42689328/159305299-12f8086d-0ef4-4e7a-9960-29ad777f8a7f.png)


## How to use it :computer:
First you install it in your environment like this
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

## Why unexpected-isaves?
You might be wondering: why would I ever need such a useless lib? The answer is: you wouldn't. This lib was created for learning purposes, and it was never my intention to make it useful. It might be a nice way to impress your friends on your Minecraft server, or to make an important presentation lighter with a fun spreadsheet art, though. Be creative!

You can read our [wiki](https://github.com/Eric-Mendes/unexpected-isaves/wiki) for more information about this project if you want.

## Contributing :pencil:
Just like Minecraft, everything's better when shared and built together.

Contributions are welcome and appreciated. Make sure to read our [guide for contributing](https://github.com/Eric-Mendes/unexpected_isaves/blob/main/CONTRIBUTING.md) and don't forget to check out our [code of conduct](https://github.com/Eric-Mendes/unexpected_isaves/blob/main/CODE_OF_CONDUCT.md).

Have fun!

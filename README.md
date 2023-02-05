<div id="header" align="center">
    <img src="https://user-images.githubusercontent.com/42689328/159303554-70eaea67-8840-4889-8683-b54fa7b815cb.png" alt="unexpected-isaves" width=300 />
    <h2> Unexpected image saves </h2>
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
    <a href="https://saythanks.io/to/Eric-Mendes">
        <img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg" alt="Say Thanks!"/>
    </a>
</div>
<br/>

<h1> Generate images as a spreadsheet, a Minecraft pixel art, or an ascii art using Python </h1>

A quick scroll through social media and you'll find very talented people making portraits out of dice, rubik's cube, in minecraft as pixel art, or even using MIDI notes on a Digital Audio Workstation (DAW). This package gives you the ability to do the same, with or without talent.
Currently it can only generate arts using minecraft, the cells of a spreadsheet, or ascii art, but if you have any ideas that fit into the project's goal please [let me know](https://github.com/Eric-Mendes/unexpected-isaves/issues/10), or - even better - submit a merge request with your work!

## Table of contents
- [What does this package do :thinking:](https://github.com/Eric-Mendes/unexpected-isaves#what-does-this-package-do-thinking);
- [How to use it :computer:](https://github.com/Eric-Mendes/unexpected-isaves#how-to-use-it-computer);
- [Why unexpected-isaves?](https://github.com/Eric-Mendes/unexpected-isaves#why-unexpected-isaves);
- [Contributing :pencil:](https://github.com/Eric-Mendes/unexpected-isaves#contributing-pencil);
- [Into the wild](https://github.com/Eric-Mendes/unexpected-isaves#into-the-wild)

<hr/>

## What does this package do :thinking:
With this package you can save any `image` on a given `path` as a
- Spreadsheet:
![this_is_fine-meme-python-excel-spreadsheet-unexpected-isaves](https://user-images.githubusercontent.com/42689328/159305173-7946f75e-999d-479d-8ac6-cd09e89097c0.png)

- Minecraft Pixel Art Datapack:
![naruto-anime-python-minecraft-pixel-art-data-pack-unexpected-isaves](https://user-images.githubusercontent.com/42689328/159305299-12f8086d-0ef4-4e7a-9960-29ad777f8a7f.png)

- Ascii Art:
![capybara-ascii-art](https://user-images.githubusercontent.com/42689328/216817867-b2f30809-6ae8-46f3-87d2-6c8f95a0a761.png)



## How to use it :computer:
First you install it in your environment like this
```bash
pip install unexpected-isaves
```
Then you can start using it already! Pass the path of any image you've got locally and try to save it using our functions!
```python
from unexpected_isaves import save_image


save_image.to_excel(
    image="my_image.png",
    path="/home/user/Documents/my_image.xlsx"
)
```

## Why unexpected-isaves?
You might be wondering: why would I ever need such a useless lib? The answer is: you wouldn't. This lib was created for learning purposes, and it was never my intention to make it useful. It might be a nice way to impress your friends on your Minecraft server, or to make an important presentation lighter with a fun spreadsheet art, though. Be creative!

You can read our [wiki](https://github.com/Eric-Mendes/unexpected-isaves/wiki) for more information about this project if you want.

## Contributing :pencil:
Just like Minecraft, everything's better when shared and built together.

Contributions are welcome and appreciated. Make sure to read our [guide for contributing](https://github.com/Eric-Mendes/unexpected_isaves/blob/main/CONTRIBUTING.md) and don't forget to check out our [code of conduct](https://github.com/Eric-Mendes/unexpected_isaves/blob/main/CODE_OF_CONDUCT.md).

## Into the wild
So you've used this tool to create the most awesome art ever, and now you want to share it in your social media? Please use *#unexpected_isaves* when you post it.

Have fun!

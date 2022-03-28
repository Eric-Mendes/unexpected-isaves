<h1> unexpected-isaves </h1>

This is the official documentation for the [unexpected-isaves](https://pypi.org/project/unexpected-isaves/) project.

With this Python library you can save any image opened with [PIL's `Image` module](https://pillow.readthedocs.io/en/stable/reference/Image.html) in different ways. Currently only supporting as a spreadsheet (by painting its pixels on each cell) or a minecraft data pack containing it's pixel art.

### Contributing
Just like the project itself, these docs also accept contributions. In fact, if you add functionality to the source code, besides pydoc, it's good practice to document it here as well.

### Functions
- `to_excel(image: Image, path: str, lower_image_size_by: int = 10, **spreadsheet_kwargs) -> None`

This function receives an `ìmage` and it outputs a `.xlsx` file on a given `path`. The file contains the `image` "painted" throughout the cells.

#### to_excel parameters
* :param image: Your image opened using the `PIL.Image` module;
* :param path: The path that you want to save your output file.
Example: `/home/user/Documents/my_image.xlsx`;
* :param lower_image_size_by: A factor that the function will divide
your image's dimensions by. Defaults to `10`;
 * It is very important that you lower your image's dimensions because a big image might take the function a long time to process plus your spreadsheet will probably take a long time to load on any software that you use to open it;
* :param **spreadsheet_kwargs: See below.

##### Spreadsheet Kwargs
Optional parameters to tweak the spreadsheet's appearance.
* :param row_height (`float`): the rows' height. Defaults to `15`;
* :param column_width (`float`): the columns' width. Defaults to `2.3`;
 * The default values on `row_height` and `column_width` were specifically thought out so that they make the cells squared, however - as any hardcoded value - they might not do the trick on your device. That is when you might want to tweak them a little bit.
* :param delete_cell_value (`bool`): wheter to keep or not the text corresponding to that color. Defaults to `True`;
* :param zoom_scale (`int`): how much to zoom in or out on the spreadsheet. Defaults to `20` which seems to be the default max zoom out on most spreadsheet softwares.
##### Return
* :return: `None`, but outputs a `.xlsx` file on the given `path`.

---
- `to_minecraft(image: Image, path: str, lower_image_size_by: int = 10, player_pos: Tuple[int, int, int] = (0, 0, 0),) -> None`

This function receives an `ìmage` and it outputs a folder structure with some files inside it on a given `path`. The folders make up a data pack.

#### to_minecraft parameters
* :param image: Your image opened using the `PIL.Image` module;
* :param path: The path that you want to save your datapack.
Example: `/home/user/Documents/my_image_datapack`;
* :param lower_image_size_by: A factor that the function will divide
your image's dimensions by. Defaults to `10`;
* :param player_pos: The player's (x, y, z) position. Defaults to `(0, 0, 0)`.
##### Return
* :return: `None`, but outputs a datapack on the given `path`.

---
### Inspiration
You can find the inspiration behind this project [here](https://github.com/Eric-Mendes/unexpected-isaves/wiki#inspiration).

### Examples
Here's some art generated with `unexpected-isaves`. You can contribute to this project by adding your own art here!

![python-to_excel-spreadsheet-this_is_fine](https://user-images.githubusercontent.com/42689328/159305173-7946f75e-999d-479d-8ac6-cd09e89097c0.png)
![python-to_minecraft-pixel-art-data-pack-naruto](https://user-images.githubusercontent.com/42689328/159305299-12f8086d-0ef4-4e7a-9960-29ad777f8a7f.png)

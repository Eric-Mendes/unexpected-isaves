Usage
=====

.. _installation:

Installation
------------

To use unexpected-isaves, first install it using pip:

.. code-block:: console

   (.venv) $ pip install unexpected-isaves

Creating a spreadsheet art
----------------

To create a spreadsheet art out of any image you want,
you can use the ``save_image.to_excel()`` function:

.. autofunction:: save_image.to_excel

- The ``image`` parameter is your image opened using the `PIL.Image` module;
- The ``path`` parameter is the path that you want to save the output file;
- The ``lower_image_size_by`` parameter is a factor that the function will divide your image's dimensions by. Defaults to `10`;
    - It is very important that you lower your image's dimensions because a big image might take the function a long time to process plus your spreadsheet will probably take a long time to load on any software that you use to open it.
- The ``spreadsheet_kwargs`` are optional parameters to tweak the spreadsheet's appearance.
    - The ``row_height`` parameter (`float`): the rows' height. Defaults to `15`;
    - The ``column_width`` parameter (`float`): the columns' width. Defaults to `2.3`;
       - The default values on `row_height` and `column_width` were specifically thought out so that they make the cells squared, however - as any hardcoded value - they might not do the trick on your device. That is when you might want to tweak them a little bit.
    - The ``delete_cell_value`` parameter (`bool`): wheter to keep or not the text corresponding to that color. Defaults to `True`;
    - The ``zoom_scale`` parameter (`int`): how much to zoom in or out on the spreadsheet. Defaults to `20` which seems to be the default max zoom out on most spreadsheet softwares.

It returns `None` but outputs a `.xlsx` file on the given `path`.


Creating a Minecraft pixel art
----------------

To create a spreadsheet art out of any image you want,
you can use the ``save_image.to_minecraft()`` function:

.. autofunction:: save_image.to_minecraft

- The ``image`` parameter is your image opened using the `PIL.Image` module;
- The ``path`` parameter is the path that you want to save the output datapack;
- The ``lower_image_size_by`` parameter is a factor that the function will divide your image's dimensions by. Defaults to `10`;
- The ``player_pos`` are the player's (x, y, z) position. Defaults to `(0, 0, 0)`.
    
It returns `None` but outputs a datapack on the given `path`.


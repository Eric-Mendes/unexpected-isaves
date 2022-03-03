import json
import os
from contextlib import suppress
from math import sqrt
from typing import Tuple

import numpy as np
import pandas as pd
from openpyxl import load_workbook, styles, utils
from PIL import Image


def to_excel(
    image: Image, path: str, lower_image_size_by: int = 10, **spreadsheet_kwargs
) -> None:
    """
    - Added on release 0.0.1;
    - Coded originally on https://github.com/Eric-Mendes/image2excel

    Saves an image as a `.xlsx` file by coloring its cells each pixel's color.

    ## Parameters
    * :param image: Your image opened using the `PIL.Image` module;
    * :param path: The path that you want to save your output file.
    Example: `/home/user/Documents/my_image.xlsx`;
    * :param lower_image_size_by: A factor that the function will divide
    your image's dimensions by. Defaults to `10`;
       * It is very important that you lower your image's dimensions because a big image might take the function a long time to process plus your spreadsheet will probably take a long time to load on any software that you use to open it;
    * :param **spreadsheet_kwargs: See below.

    ## Spreadsheet Kwargs
    Optional parameters to tweak the spreadsheet's appearance.

    * :param row_height (`float`): the rows' height. Defaults to `15`;
    * :param column_width (`float`): the columns' width. Defaults to `2.3`;
       * The default values on `row_height` and `column_width` were specifically thought out so that they make the cells squared, however - as any hardcoded value - they might not do the trick on your device. That is when you might want to tweak them a little bit.
    * :param delete_cell_value (`bool`): wheter to keep or not the text corresponding to that color. Defaults to `True`;
    * :param zoom_scale (`int`): how much to zoom in or out on the spreadsheet. Defaults to `20` which seems to be the default max zoom out on most spreadsheet softwares.

    ## Return
    * :return: `None`, but outputs a `.xlsx` file on the given `path`.
    """
    image = image.convert("RGB")

    # Resizing image
    image = image.resize(
        (image.size[0] // lower_image_size_by, image.size[1] // lower_image_size_by)
    )

    # OpenPyxl colors work in a weird way
    image_colors_processed = [
        ["%02x%02x%02x" % tuple(item) for item in row]
        for row in np.array(image).tolist()
    ]

    df = pd.DataFrame(image_colors_processed)
    image_name = os.path.splitext(os.path.split(path)[1])[0]

    # Saving a DataFrame where each cell has a text corresponding to the RGB color its background should be
    df.to_excel(path, index=False, header=False)

    # Loading the excel file, painting each cell with its color and saving the updates
    wb = load_workbook(path)

    ws = wb.active
    ws.title = image_name

    for row in range(1, df.shape[0] + 1):
        for col in range(1, df.shape[1] + 1):
            cell = ws.cell(row=row, column=col)
            # Makes cells squared
            ws.row_dimensions[row].height = spreadsheet_kwargs.get("row_height", 15)
            ws.column_dimensions[
                utils.get_column_letter(col)
            ].width = spreadsheet_kwargs.get("column_width", 2.3)

            # Painting the cell
            cell.fill = styles.PatternFill(
                start_color=cell.value, end_color=cell.value, fill_type="solid"
            )
            if spreadsheet_kwargs.get("delete_cell_value", True):
                cell.value = None  # Deletes the text from the cell

    # Saves spreadsheet already zoomed in or out
    ws.sheet_view.zoomScale = spreadsheet_kwargs.get("zoom_scale", 20)
    wb.save(path)


def to_minecraft(
    image: Image,
    path: str,
    lower_image_size_by: int = 10,
    player_pos: Tuple[int, int, int] = (0, 0, 0),
) -> None:
    """
    - Added on release 0.0.1;
    - Coded originally on https://github.com/Eric-Mendes/pixel-art-map

    Saves an image as a minecraft datapack that when loaded into your world will build a pixel art of it on the player's position.

    ## Parameters
    * :param image: Your image opened using the `PIL.Image` module;
    * :param path: The path that you want to save your datapack.
    Example: `/home/user/Documents/my_image_datapack`;
    * :param lower_image_size_by: A factor that the function will divide
    your image's dimensions by. Defaults to `10`;
    * :param player_pos: The player's (x, y, z) position. Defaults to `(0, 0, 0)`.

    ## Return
    * :return: `None`, but outputs a datapack on the given `path`.
    """
    image = image.convert("RGB")

    # Makes the commands that the datapack will run when loaded
    def script(df, **kwargs):
        player_pos = [
            kwargs.get("player_x", 0),
            kwargs.get("player_y", 0),
            kwargs.get("player_z", 0),
        ]
        z = (df != df.shift()).cumsum()
        zri = z.reset_index()
        ix_name = z.index.name
        co_name = z.columns.name
        for i in z:
            v = zri.groupby(i)[ix_name].agg(["first", "last"])
            s = {co_name: i}
            e = {co_name: i}
            for _, r in v.iterrows():
                s[ix_name] = r["first"]
                e[ix_name] = r["last"]
                material = df.loc[r["first"], i]
                yield f'fill {s["x"] + player_pos[0]} {0 + player_pos[1]} {s["z"] + player_pos[2]} {e["x"] + player_pos[0]} {0 + player_pos[1]} {e["z"] + player_pos[2]} {material.split(",")[0].strip()}'

    # Helper function. Loads the blocks an the colors they have when looked at via map,
    # and maps the pixels to the blocks
    blocks = [
        {
            "rgb": (127, 178, 56),
            "blocks": ("grass_block", "slime_block"),
        },
        {
            "rgb": (247, 233, 163),
            "blocks": ("sand", "birch_planks", "birch_log[axis=y]", "stripped_birch_log[axis=x]", "birch_wood", "stripped_birch_wood", "birch_sign", "birch_pressure_plate", "birch_trapdoor", "birch_stairs", "birch_slab", "birch_fence_gate", "birch_fence", "birch_door", "sandstone", "glowstone", "end_stone", "end_stone_brick_slab", "end_stone_brick_stairs", "end_stone_brick_wall", "bone_block", "turtle_egg", "scaffolding", "candle"),
        },
        {
            "rgb": (199, 199, 199),
            "blocks": ("mushroom_stem", "cobweb", "white_bed[part=head]", "white_candle"),
        },
        {
            "rgb": (255, 0, 0),
            "blocks": ("redstone_block", "tnt", "lava", "fire"),
        },
        {
            "rgb": (160, 160, 255),
            "blocks": ("ice", "frosted_ice", "packed_ice", "blue_ice"),
        },
        {
            "rgb": (167, 167, 167),
            "blocks": ("iron_block", "iron_door", "brewing_stand", "heavy_weighted_pressure_plate", "iron_trapdoor", "lantern", "anvil", "grindstone", "soul_lantern", "lodestone"),
        },
        {
            "rgb": (0, 124, 0),
            "blocks": ("oak_sapling", "spruce_sapling", "birch_sapling", "jungle_sapling", "acacia_sapling", "dark_oak_sapling", "dandelion", "poppy", "blue_orchid", "allium", "azure_bluet", "red_tulip", "orange_tulip", "white_tulip", "pink_tulip", "oxeye_daisy", "cornflower", "lily_of_the_valley", "wither_rose", "sunflower", "lilac", "rose_bush", "peony", "wheat[age=7]", "sugar_cane[age=9]", "pumpkin_stem[age=7]", "melon_stem[age=7]", "lily_pad", "cocoa[age=2]", "carrots[age=7]", "potatoes[age=7]", "beetroots[age=7]", "sweet_berry_bush[age=3]", "grass", "fern", "vine", "oak_leaves", "spruce_leaves", "birch_leaves", "jungle_leaves", "acacia_leaves", "dark_oak_leaves", "azalea_leaves", "flowering_azalea_leaves", "cactus[age=9]", "bamboo[age=1]", "cave_vines", "spore_blossom", "flowering_azalea", "big_dripleaf", "small_dripleaf"),
        },
        {
            "rgb": (255, 255, 255),
            "blocks": ("snow", "snow_block", "white_bed[part=foot]", "white_wool", "white_stained_glass", "white_carpet", "white_shulker_box", "white_glazed_terracotta", "white_concrete", "white_concrete_powder", "powder_snow"),
        },
        {
            "rgb": (164, 168, 184),
            "blocks": ("clay", "infested_chiseled_stone_bricks", "infested_cobblestone", "infested_cracked_stone_bricks", "infested_mossy_stone_bricks", "infested_stone", "infested_stone_bricks"),
        },
        {
            "rgb": (151, 109, 77),
            "blocks": ("coarse_dirt", "dirt", "farmland", "dirt_path", "granite_slab", "granite_stairs", "granite_wall", "polished_granite_slab", "polished_granite_stairs", "jungle_planks", "jungle_log[axis=y]", "stripped_jungle_log[axis=x]", "jungle_wood", "stripped_jungle_wood", "jungle_sign", "jungle_pressure_plate", "jungle_trapdoor", "jungle_stairs", "jungle_slab", "jungle_fence_gate", "jungle_fence", "jungle_door", "jukebox", "brown_mushroom_block", "rooted_dirt", "hanging_roots"),
        },
        {
            "rgb": (112, 112, 112),
            "blocks": ("stone", "stone_slab", "stone_stairs", "andesite_slab", "andesite_stairs", "andesite_wall", "polished_andesite_slab", "polished_andesite_stairs", "cobblestone_slab", "cobblestone_stairs", "cobblestone_wall", "bedrock", "gold_ore", "iron_ore", "coal_ore", "lapis_lazuli_ore", "dispenser", "mossy_cobblestone_slab", "mossy_cobblestone_stairs", "mossy_cobblestone_wall", "spawner", "diamond_ore", "furnace", "stone_pressure_plate", "redstone_ore", "stone_bricks", "emerald_ore", "ender_chest", "dropper", "smooth_stone_slab", "observer", "smoker", "blast_furnace", "stonecutter", "sticky_piston", "piston", "piston_head", "gravel", "acacia_log[axis=z]", "cauldron", "hopper", "copper_ore"),
        },
        {
            "rgb": (64, 64, 255),
            "blocks": ("water", "kelp", "seagrass", "bubble_column"),
        },
        {
            "rgb": (143, 119, 72),
            "blocks": ("oak_planks", "oak_log[axis=y]", "stripped_oak_log[axis=x]", "oak_wood", "stripped_oak_wood", "oak_sign", "oak_pressure_plate", "oak_trapdoor", "oak_stairs", "oak_slab", "oak_fence_gate", "oak_fence", "oak_door", "note_block", "bookshelf", "chest", "crafting_table", "trapped_chest", "daylight_detector", "loom", "barrel", "cartography_table", "fletching_table", "lectern", "smithing_table", "composter", "bamboo_sapling", "dead_bush", "petrified_oak_slab", "beehive", "white_banner"),
        },
        {
            "rgb": (255, 252, 245),
            "blocks": ("quartz_block", "diorite_stairs", "diorite_slab", "diorite_wall", "polished_diorite_stairs", "polished_diorite_slab", "birch_log[axis=x]", "sea_lantern", "target"),
        },
        {
            "rgb": (216, 127, 51),
            "blocks": ("acacia_planks", "acacia_log[axis=y]", "stripped_acacia_log[axis=x]", "acacia_wood", "stripped_acacia_wood", "acacia_sign", "acacia_pressure_plate", "acacia_trapdoor", "acacia_stairs", "acacia_slab", "acacia_fence_gate", "acacia_fence", "acacia_door", "red_sand", "orange_wool", "orange_carpet", "orange_shulker_box", "orange_bed[part=foot]", "orange_stained_glass", "orange_glazed_terracotta", "orange_concrete", "orange_concrete_powder", "orange_candle", "pumpkin", "carved_pumpkin", "jack_o_lantern", "terracotta", "red_sandstone", "honey_block", "honeycomb_block", "copper_block", "lightning_rod", "raw_copper_block"),
        },
        {
            "rgb": (178, 76, 216),
            "blocks": ("magenta_wool", "magenta_carpet", "magenta_shulker_box", "magenta_bed[part=foot]", "magenta_stained_glass", "magenta_glazed_terracotta", "magenta_concrete", "magenta_concrete_powder", "magenta_candle", "purpur_block"),
        },
        {
            "rgb": (102, 153, 216),
            "blocks": ("light_blue_wool", "light_blue_carpet", "light_blue_shulker_box", "light_blue_bed[part=foot]", "light_blue_stained_glass", "light_blue_glazed_terracotta", "light_blue_concrete", "light_blue_concrete_powder", "light_blue_candle", "soul_fire"),
        },
        {
            "rgb": (229, 229, 51),
            "blocks": ("sponge", "wet_sponge", "yellow_wool", "yellow_carpet", "yellow_shulker_box", "yellow_bed[part=foot]", "yellow_stained_glass", "yellow_glazed_terracotta", "yellow_concrete", "yellow_concrete_powder", "yellow_candle", "hay_bale", "horn_coral_block[waterlogged=true]", "bee_nest"),
        },
        {
            "rgb": (127, 204, 25),
            "blocks": ("lime_wool", "lime_carpet", "lime_shulker_box", "lime_bed[part=foot]", "lime_stained_glass", "lime_glazed_terracotta", "lime_concrete", "lime_concrete_powder", "lime_candle", "melon"),
        },
        {
            "rgb": (242, 127, 165),
            "blocks": ("pink_wool", "pink_carpet", "pink_shulker_box", "pink_bed[part=foot]", "pink_stained_glass", "pink_glazed_terracotta", "pink_concrete", "pink_concrete_powder", "pink_candle", "brain_coral_block[waterlogged=true]"),
        },
        {
            "rgb": (76, 76, 76),
            "blocks": ("acacia_wood", "gray_wool", "gray_carpet", "gray_shulker_box", "gray_bed[part=foot]", "gray_stained_glass", "gray_glazed_terracotta", "gray_concrete", "gray_concrete_powder", "gray_candle", "dead_coral_block", "tinted_glass"),
        },
        {
            "rgb": (153, 153, 153),
            "blocks": ("light_gray_wool", "light_gray_carpet", "light_gray_shulker_box", "light_gray_bed[part=foot]", "light_gray_stained_glass", "light_gray_glazed_terracotta", "light_gray_concrete", "light_gray_concrete_powder", "light_gray_candle", "structure_block", "jigsaw"),
        },
        {
            "rgb": (76, 127, 153),
            "blocks": ("cyan_wool", "cyan_carpet", "cyan_shulker_box", "cyan_bed[part=foot]", "cyan_stained_glass", "cyan_glazed_terracotta", "cyan_concrete", "cyan_concrete_powder", "cyan_candle", "prismarine_slab", "prismarine_stairs", "prismarine_wall", "warped_roots", "warped_fungus", "twisting_vines", "nether_sprouts", "sculk_sensor"),
        },
        {
            "rgb": (127, 63, 178),
            "blocks": ("shulker_box", "purple_wool", "purple_carpet", "purple_shulker_box", "purple_bed[part=foot]", "purple_stained_glass", "purple_glazed_terracotta", "purple_concrete", "purple_concrete_powder", "purple_candle", "mycelium", "chorus_plant", "chorus_flower", "repeating_command_block", "bubble_coral_block", "amethyst_block", "budding_amethyst", "amethyst_cluster"),
        },
        {
            "rgb": (51, 76, 178),
            "blocks": ("blue_wool", "blue_carpet", "blue_shulker_box", "blue_bed[part=foot]", "blue_stained_glass", "blue_glazed_terracotta", "blue_concrete", "blue_concrete_powder", "blue_candle", "tube_coral_block"),
        },
        {
            "rgb": (102, 76, 51),
            "blocks": ("dark_oak_planks", "dark_oak_log[axis=y]", "stripped_dark_oak_log[axis=x]", "dark_oak_wood", "stripped_dark_oak_wood", "dark_oak_sign", "dark_oak_pressure_plate", "dark_oak_trapdoor", "dark_oak_stairs", "dark_oak_slab", "dark_oak_fence_gate", "dark_oak_fence", "dark_oak_door", "spruce_log[axis=x]", "brown_wool", "brown_carpet", "brown_shulker_box", "brown_bed[part=foot]", "brown_stained_glass", "brown_glazed_terracotta", "brown_concrete", "brown_concrete_powder", "brown_candle", "soul_sand", "command_block", "brown_mushroom", "soul_soil"),
        },
        {
            "rgb": (102, 127, 51),
            "blocks": ("green_wool", "green_carpet", "green_shulker_box", "green_bed[part=foot]", "green_stained_glass", "green_glazed_terracotta", "green_concrete", "green_concrete_powder", "green_candle", "end_portal_frame", "chain_command_block", "sea_pickle", "moss_carpet", "moss_block", "dried_kelp_block"),
        },
        {
            "rgb": (153, 51, 51),
            "blocks": ("red_wool", "red_carpet", "red_shulker_box", "red_bed[part=foot]", "red_stained_glass", "red_glazed_terracotta", "red_concrete", "red_concrete_powder", "red_candle", "brick_slab", "brick_stairs", "brick_wall", "red_mushroom_block", "nether_wart", "enchanting_table", "nether_wart_block", "fire_coral_block", "red_mushroom", "shroomlight"),
        },
        {
            "rgb": (25, 25, 25),
            "blocks": ("black_wool", "black_carpet", "black_shulker_box", "black_bed[part=foot]", "black_stained_glass", "black_glazed_terracotta", "black_concrete", "black_concrete_powder", "black_candle", "obsidian", "end_portal", "dragon_egg", "coal_block", "end_gateway", "basalt", "polished_basalt", "smooth_basalt", "netherite_block", "crying_obsidian", "respawn_anchor", "blackstone", "gilded_blackstone"),
        },
        {
            "rgb": (250, 238, 77),
            "blocks": ("gold_block", "light_weighted_pressure_plate", "bell", "raw_gold_block"),
        },
        {
            "rgb": (92, 219, 213),
            "blocks": ("diamond_block", "beacon", "prismarine_brick_slab", "prismarine_brick_stairs", "dark_prismarine_slab", "dark_prismarine_stairs", "conduit"),
        },
        {
            "rgb": (74, 128, 255),
            "blocks": ("lapis_lazuli_block"),
        },
        {
            "rgb": (0, 217, 58),
            "blocks": ("emerald_block"),
        },
        {
            "rgb": (129, 86, 49),
            "blocks": ("podzol", "spruce_planks", "spruce_log[axis=y]", "stripped_spruce_log[axis=x]", "spruce_wood", "stripped_spruce_wood", "spruce_sign", "spruce_pressure_plate", "spruce_trapdoor", "spruce_stairs", "spruce_slab", "spruce_fence_gate", "spruce_fence", "spruce_door", "oak_log[axis=x]", "jungle_log[axis=x]", "campfire", "soul_campfire"),
        },
        {
            "rgb": (112, 2, 0),
            "blocks": ("netherrack", "nether_brick_fence", "nether_brick_slab", "nether_brick_stairs", "nether_brick_wall", "nether_brick_chiseled", "nether_brick_cracked", "nether_gold_ore", "nether_quartz_ore", "magma_block", "red_nether_brick_slab", "red_nether_brick_stairs", "red_nether_brick_wall", "crimson_roots", "crimson_fungus", "weeping_vines"),
        },
        {
            "rgb": (209, 177, 161),
            "blocks": ("white_terracotta", "calcite"),
        },
        {
            "rgb": (159, 82, 36),
            "blocks": ("orange_terracotta"),
        },
        {
            "rgb": (149, 87, 108),
            "blocks": ("magenta_terracotta"),
        },
        {
            "rgb": (112, 108, 138),
            "blocks": ("light_blue_terracotta"),
        },
        {
            "rgb": (186, 133, 36),
            "blocks": ("yellow_terracotta"),
        },
        {
            "rgb": (103, 117, 53),
            "blocks": ("lime_terracotta"),
        },
        {
            "rgb": (160, 77, 78),
            "blocks": ("pink_terracotta"),
        },
        {
            "rgb": (57, 41, 35),
            "blocks": ("gray_terracotta", "tuff"),
        },
        {
            "rgb": (135, 107, 98),
            "blocks": ("light_gray_terracotta", "exposed_copper"),
        },
        {
            "rgb": (87, 92, 92),
            "blocks": ("cyan_terracotta"),
        },
        {
            "rgb": (122, 73, 88),
            "blocks": ("purple_terracotta", "purple_shulker_box"),
        },
        {
            "rgb": (76, 62, 92),
            "blocks": ("blue_terracotta"),
        },
        {
            "rgb": (76, 50, 35),
            "blocks": ("brown_terracotta", "pointed_dripstone", "dripstone_block"),
        },
        {
            "rgb": (76, 82, 42),
            "blocks": ("green_terracotta"),
        },
        {
            "rgb": (142, 60, 46),
            "blocks": ("red_terracotta"),
        },
        {
            "rgb": (37, 22, 16),
            "blocks": ("black_terracotta"),
        },
        {
            "rgb": (189, 48, 49),
            "blocks": ("crimson_nylium"),
        },
        {
            "rgb": (148, 63, 97),
            "blocks": ("crimson_planks", "crimson_log[axis=y]", "stripped_crimson_log[axis=x]", "crimson_wood", "stripped_crimson_wood", "crimson_sign", "crimson_pressure_plate", "crimson_trapdoor", "crimson_stairs", "crimson_slab", "crimson_fence_gate", "crimson_fence", "crimson_door"),
        },
        {
            "rgb": (92, 25, 29),
            "blocks": ("crimson_hyphae", "stripped_crimson_hyphae"),
        },
        {
            "rgb": (22, 126, 134),
            "blocks": ("warped_nylium", "oxidized_copper"),
        },
        {
            "rgb": (58, 142, 140),
            "blocks": ("warped_planks", "warped_log[axis=y]", "stripped_warped_log[axis=x]", "warped_wood", "stripped_warped_wood", "warped_sign", "warped_pressure_plate", "warped_trapdoor", "warped_stairs", "warped_slab", "warped_fence_gate", "warped_fence", "warped_door", "weathered_copper"),
        },
        {
            "rgb": (86, 44, 62),
            "blocks": ("warped_hyphae", "stripped_warped_hyphae"),
        },
        {
            "rgb": (20, 180, 133),
            "blocks": ("warped_wart_block"),
        },
        {
            "rgb": (100, 100, 100),
            "blocks": ("deepslate"),
        },
        {
            "rgb": (216, 175, 147),
            "blocks": ("raw_iron_block"),
        },
        {
            "rgb": (127, 167, 150),
            "blocks": ("glow_lichen"),
        },
    ]

    def to_minecraft_color(pxl):
        color = None
        min_distance = None
        for item in blocks:
            # Calculates the "distance" between two RGB colors as if they
            # were points in a 3-dimensional space.
            # The closer they are, the more they look like each other.
            euclidean_distance = sqrt(sum([pow(p - c, 2) for p, c in zip(item["rgb"], pxl)]))

            if min_distance is None or euclidean_distance < min_distance:
                min_distance = euclidean_distance
                color = ", ".join("minecraft:"+block for block in item["blocks"])
        return color

    # Resizing the image and mapping each pixel's color to a minecraft color
    image = image.resize(
        (image.size[0] // lower_image_size_by, image.size[1] // lower_image_size_by)
    )
    image_colors_processed = [
        [to_minecraft_color(pixel) for pixel in row] for row in np.array(image)
    ]

    # Getting the name that the image should have via the given path
    image_name = os.path.splitext(os.path.split(path)[1])[0]

    df = pd.DataFrame(image_colors_processed)

    # Creates - in an error proof manner - the folder structure of the datapack
    with suppress(FileExistsError):
        os.makedirs(f"{path}/data/minecraft/tags/functions")
        os.makedirs(f"{path}/data/pixelart-map/functions")

    pack_mcmeta = {
        "pack": {
            "pack_format": 8,
            "description": f"This datapack will generate the image ({image_name}) in your world",
        }
    }
    load_json = {"values": ["pixelart-map:load"]}
    tick_json = {"values": ["pixelart-map:tick"]}

    with open(f"{path}/pack.mcmeta", "w") as file:
        file.write(json.dumps(pack_mcmeta, indent=4))
    with open(f"{path}/data/minecraft/tags/functions/load.json", "w") as file:
        file.write(json.dumps(load_json, indent=4))
    with open(f"{path}/data/minecraft/tags/functions/tick.json", "w") as file:
        file.write(json.dumps(tick_json, indent=4))

    with open(f"{path}/data/pixelart-map/functions/tick.mcfunction", "w") as file:
        file.write("")

    # Making the commands that when ran will build the image's pixel art.
    # This part's had a huge contribution from this thread: https://stackoverflow.com/questions/70512775/how-to-group-elements-in-dataframe-by-row/70546452#70546452
    df = df.rename_axis(index="z", columns="x")

    a = list(
        script(
            df,
            player_x=player_pos[0],
            player_y=player_pos[1],
            player_z=player_pos[2],
        )
    )
    b = list(
        script(
            df.T,
            player_x=player_pos[0],
            player_y=player_pos[1],
            player_z=player_pos[2],
        )
    )
    res = min([a, b], key=len)
    with open(f"{path}/data/pixelart-map/functions/load.mcfunction", "w") as file:
        file.write("\n".join(res))

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
    * :param delete_cell_value(`bool`): wheter to keep or not the text corresponding to that color. Defaults to `True`;
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
    player_pos: Tuple[int] = (0, 0, 0),
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

    # Helper function. Calculates the "distance" between two RGB colors as if they
    # were points in a 3-dimensional space.
    # The closer they are, the more they look like each other.
    euclidean_distance = lambda pixel, color: sqrt(
        sum([pow(p - c, 2) for p, c in zip(pixel, color)])
    )

    # Helper function. Loads the blocks an the colors they have when looked at via map,
    # and maps the pixels to the blocks
    blocks = [
        {
            "color_name": "NONE",
            "rgb": ["Transparent"],
            "blocks": "Air, Void Air, Cave Air, Barrier, Redstone Lamp, Cake (including cake with Candles), Powered Rail, Detector Rail, Torch, Redstone Wire, Ladder, Rail, Lever, Redstone Torch, Buttons, Repeater, Tripwire Hook, Tripwire, Flower Pot (including potted plants), Head, Comparator, Activator Rail, End Rod, Glass, Glass Pane, Nether Portal, Stained Glass Pane (all colors), Structure Void, Iron Bars, Soul Fire Torch, Chain, Light Block",
        },
        {
            "color_name": "GRASS",
            "rgb": ["127", "178", "56"],
            "blocks": "minecraft:grass_block, minecraft:slime_block",
        },
        {
            "color_name": "SAND",
            "rgb": ["247", "233", "163"],
            "blocks": "minecraft:sand, minecraft:birch_planks, minecraft:birch_log[axis=y], minecraft:stripped_birch_log[axis=x], minecraft:birch_wood, minecraft:stripped_birch_wood, minecraft:birch_sign, minecraft:birch_pressure_plate, minecraft:birch_trapdoor, minecraft:birch_stairs, minecraft:birch_slab, minecraft:birch_fence_gate, minecraft:birch_fence, minecraft:birch_door, minecraft:sandstone, minecraft:glowstone, minecraft:end_stone, minecraft:end_stone_brick_slab, minecraft:end_stone_brick_stairs, minecraft:end_stone_brick_wall, minecraft:bone_block, minecraft:turtle_egg, minecraft:scaffolding, minecraft:candle",
        },
        {
            "color_name": "WOOL",
            "rgb": ["199", "199", "199"],
            "blocks": "minecraft:mushroom_stem, minecraft:cobweb, minecraft:white_bed[part=head], minecraft:white_candle",
        },
        {
            "color_name": "FIRE",
            "rgb": ["255", "0", "0"],
            "blocks": "minecraft:redstone_block, minecraft:tnt, minecraft:lava, minecraft:fire",
        },
        {
            "color_name": "ICE",
            "rgb": ["160", "160", "255"],
            "blocks": "minecraft:ice, minecraft:frosted_ice, minecraft:packed_ice, minecraft:blue_ice",
        },
        {
            "color_name": "METAL",
            "rgb": ["167", "167", "167"],
            "blocks": "minecraft:iron_block, minecraft:iron_door, minecraft:brewing_stand, minecraft:heavy_weighted_pressure_plate, minecraft:iron_trapdoor, minecraft:lantern, minecraft:anvil, minecraft:grindstone, minecraft:soul_lantern, minecraft:lodestone",
        },
        {
            "color_name": "PLANT",
            "rgb": ["0", "124", "0"],
            "blocks": "minecraft:oak_sapling, minecraft:spruce_sapling, minecraft:birch_sapling, minecraft:jungle_sapling, minecraft:acacia_sapling, minecraft:dark_oak_sapling, minecraft:dandelion, minecraft:poppy, minecraft:blue_orchid, minecraft:allium, minecraft:azure_bluet, minecraft:red_tulip, minecraft:orange_tulip, minecraft:white_tulip, minecraft:pink_tulip, minecraft:oxeye_daisy, minecraft:cornflower, minecraft:lily_of_the_valley, minecraft:wither_rose, minecraft:sunflower, minecraft:lilac, minecraft:rose_bush, minecraft:peony, minecraft:wheat[age=7], minecraft:sugar_cane[age=9], minecraft:pumpkin_stem[age=7], minecraft:melon_stem[age=7], minecraft:lily_pad, minecraft:cocoa[age=2], minecraft:carrots[age=7], minecraft:potatoes[age=7], minecraft:beetroots[age=7], minecraft:sweet_berry_bush[age=3], minecraft:grass, minecraft:fern, minecraft:vine, minecraft:oak_leaves, minecraft:spruce_leaves, minecraft:birch_leaves, minecraft:jungle_leaves, minecraft:acacia_leaves, minecraft:dark_oak_leaves, minecraft:azalea_leaves, minecraft:flowering_azalea_leaves, minecraft:cactus[age=9], minecraft:bamboo[age=1], minecraft:cave_vines, minecraft:spore_blossom, minecraft:flowering_azalea, minecraft:big_dripleaf, minecraft:small_dripleaf",
        },
        {
            "color_name": "SNOW",
            "rgb": ["255", "255", "255"],
            "blocks": "minecraft:snow, minecraft:snow_block, minecraft:white_bed[part=foot], minecraft:white_wool, minecraft:white_stained_glass, minecraft:white_carpet, minecraft:white_shulker_box, minecraft:white_glazed_terracotta, minecraft:white_concrete, minecraft:white_concrete_powder, minecraft:powder_snow",
        },
        {
            "color_name": "CLAY",
            "rgb": ["164", "168", "184"],
            "blocks": "minecraft:clay, minecraft:infested_chiseled_stone_bricks, minecraft:infested_cobblestone, minecraft:infested_cracked_stone_bricks, minecraft:infested_mossy_stone_bricks, minecraft:infested_stone, minecraft:infested_stone_bricks",
        },
        {
            "color_name": "DIRT",
            "rgb": ["151", "109", "77"],
            "blocks": "minecraft:coarse_dirt, minecraft:dirt, minecraft:farmland, minecraft:dirt_path, minecraft:granite_slab, minecraft:granite_stairs, minecraft:granite_wall, minecraft:polished_granite_slab, minecraft:polished_granite_stairs, minecraft:jungle_planks, minecraft:jungle_log[axis=y], minecraft:stripped_jungle_log[axis=x], minecraft:jungle_wood, minecraft:stripped_jungle_wood, minecraft:jungle_sign, minecraft:jungle_pressure_plate, minecraft:jungle_trapdoor, minecraft:jungle_stairs, minecraft:jungle_slab, minecraft:jungle_fence_gate, minecraft:jungle_fence, minecraft:jungle_door, minecraft:jukebox, minecraft:brown_mushroom_block, minecraft:rooted_dirt, minecraft:hanging_roots",
        },
        {
            "color_name": "STONE",
            "rgb": ["112", "112", "112"],
            "blocks": "minecraft:stone, minecraft:stone_slab, minecraft:stone_stairs, minecraft:andesite_slab, minecraft:andesite_stairs, minecraft:andesite_wall, minecraft:polished_andesite_slab, minecraft:polished_andesite_stairs, minecraft:cobblestone_slab, minecraft:cobblestone_stairs, minecraft:cobblestone_wall, minecraft:bedrock, minecraft:gold_ore, minecraft:iron_ore, minecraft:coal_ore, minecraft:lapis_lazuli_ore, minecraft:dispenser, minecraft:mossy_cobblestone_slab, minecraft:mossy_cobblestone_stairs, minecraft:mossy_cobblestone_wall, minecraft:spawner, minecraft:diamond_ore, minecraft:furnace, minecraft:stone_pressure_plate, minecraft:redstone_ore, minecraft:stone_bricks, minecraft:emerald_ore, minecraft:ender_chest, minecraft:dropper, minecraft:smooth_stone_slab, minecraft:observer, minecraft:smoker, minecraft:blast_furnace, minecraft:stonecutter, minecraft:sticky_piston, minecraft:piston, minecraft:piston_head, minecraft:gravel, minecraft:acacia_log[axis=z], minecraft:cauldron, minecraft:hopper, minecraft:copper_ore",
        },
        {
            "color_name": "WATER",
            "rgb": ["64", "64", "255"],
            "blocks": "minecraft:water, minecraft:kelp, minecraft:seagrass, minecraft:bubble_column",
        },
        {
            "color_name": "WOOD",
            "rgb": ["143", "119", "72"],
            "blocks": "minecraft:oak_planks, minecraft:oak_log[axis=y], minecraft:stripped_oak_log[axis=x], minecraft:oak_wood, minecraft:stripped_oak_wood, minecraft:oak_sign, minecraft:oak_pressure_plate, minecraft:oak_trapdoor, minecraft:oak_stairs, minecraft:oak_slab, minecraft:oak_fence_gate, minecraft:oak_fence, minecraft:oak_door, minecraft:note_block, minecraft:bookshelf, minecraft:chest, minecraft:crafting_table, minecraft:trapped_chest, minecraft:daylight_detector, minecraft:loom, minecraft:barrel, minecraft:cartography_table, minecraft:fletching_table, minecraft:lectern, minecraft:smithing_table, minecraft:composter, minecraft:bamboo_sapling, minecraft:dead_bush, minecraft:petrified_oak_slab, minecraft:beehive, minecraft:white_banner",
        },
        {
            "color_name": "QUARTZ",
            "rgb": ["255", "252", "245"],
            "blocks": "minecraft:quartz_block, minecraft:diorite_stairs, minecraft:diorite_slab, minecraft:diorite_wall, minecraft:polished_diorite_stairs, minecraft:polished_diorite_slab, minecraft:birch_log[axis=x], minecraft:sea_lantern, minecraft:target",
        },
        {
            "color_name": "COLOR_ORANGE",
            "rgb": ["216", "127", "51"],
            "blocks": "minecraft:acacia_planks, minecraft:acacia_log[axis=y], minecraft:stripped_acacia_log[axis=x], minecraft:acacia_wood, minecraft:stripped_acacia_wood, minecraft:acacia_sign, minecraft:acacia_pressure_plate, minecraft:acacia_trapdoor, minecraft:acacia_stairs, minecraft:acacia_slab, minecraft:acacia_fence_gate, minecraft:acacia_fence, minecraft:acacia_door, minecraft:red_sand, minecraft:orange_wool, minecraft:orange_carpet, minecraft:orange_shulker_box, minecraft:orange_bed[part=foot], minecraft:orange_stained_glass, minecraft:orange_glazed_terracotta, minecraft:orange_concrete, minecraft:orange_concrete_powder, minecraft:orange_candle, minecraft:pumpkin, minecraft:carved_pumpkin, minecraft:jack_o_lantern, minecraft:terracotta, minecraft:red_sandstone, minecraft:honey_block, minecraft:honeycomb_block, minecraft:copper_block, minecraft:lightning_rod, minecraft:raw_copper_block",
        },
        {
            "color_name": "COLOR_MAGENTA",
            "rgb": ["178", "76", "216"],
            "blocks": "minecraft:magenta_wool, minecraft:magenta_carpet, minecraft:magenta_shulker_box, minecraft:magenta_bed[part=foot], minecraft:magenta_stained_glass, minecraft:magenta_glazed_terracotta, minecraft:magenta_concrete, minecraft:magenta_concrete_powder, minecraft:magenta_candle, minecraft:purpur_block",
        },
        {
            "color_name": "COLOR_LIGHT_BLUE",
            "rgb": ["102", "153", "216"],
            "blocks": "minecraft:light_blue_wool, minecraft:light_blue_carpet, minecraft:light_blue_shulker_box, minecraft:light_blue_bed[part=foot], minecraft:light_blue_stained_glass, minecraft:light_blue_glazed_terracotta, minecraft:light_blue_concrete, minecraft:light_blue_concrete_powder, minecraft:light_blue_candle, minecraft:soul_fire",
        },
        {
            "color_name": "COLOR_YELLOW",
            "rgb": ["229", "229", "51"],
            "blocks": "minecraft:sponge, minecraft:wet_sponge, minecraft:yellow_wool, minecraft:yellow_carpet, minecraft:yellow_shulker_box, minecraft:yellow_bed[part=foot], minecraft:yellow_stained_glass, minecraft:yellow_glazed_terracotta, minecraft:yellow_concrete, minecraft:yellow_concrete_powder, minecraft:yellow_candle, minecraft:hay_bale, minecraft:horn_coral_block[waterlogged=true], minecraft:bee_nest",
        },
        {
            "color_name": "COLOR_LIGHT_GREEN",
            "rgb": ["127", "204", "25"],
            "blocks": "minecraft:lime_wool, minecraft:lime_carpet, minecraft:lime_shulker_box, minecraft:lime_bed[part=foot], minecraft:lime_stained_glass, minecraft:lime_glazed_terracotta, minecraft:lime_concrete, minecraft:lime_concrete_powder, minecraft:lime_candle, minecraft:melon",
        },
        {
            "color_name": "COLOR_PINK",
            "rgb": ["242", "127", "165"],
            "blocks": "minecraft:pink_wool, minecraft:pink_carpet, minecraft:pink_shulker_box, minecraft:pink_bed[part=foot], minecraft:pink_stained_glass, minecraft:pink_glazed_terracotta, minecraft:pink_concrete, minecraft:pink_concrete_powder, minecraft:pink_candle, minecraft:brain_coral_block[waterlogged=true]",
        },
        {
            "color_name": "COLOR_GRAY",
            "rgb": ["76", "76", "76"],
            "blocks": "minecraft:acacia_wood, minecraft:gray_wool, minecraft:gray_carpet, minecraft:gray_shulker_box, minecraft:gray_bed[part=foot], minecraft:gray_stained_glass, minecraft:gray_glazed_terracotta, minecraft:gray_concrete, minecraft:gray_concrete_powder, minecraft:gray_candle, minecraft:dead_coral_block, minecraft:tinted_glass",
        },
        {
            "color_name": "COLOR_LIGHT_GRAY",
            "rgb": ["153", "153", "153"],
            "blocks": "minecraft:light_gray_wool, minecraft:light_gray_carpet, minecraft:light_gray_shulker_box, minecraft:light_gray_bed[part=foot], minecraft:light_gray_stained_glass, minecraft:light_gray_glazed_terracotta, minecraft:light_gray_concrete, minecraft:light_gray_concrete_powder, minecraft:light_gray_candle, minecraft:structure_block, minecraft:jigsaw",
        },
        {
            "color_name": "COLOR_CYAN",
            "rgb": ["76", "127", "153"],
            "blocks": "minecraft:cyan_wool, minecraft:cyan_carpet, minecraft:cyan_shulker_box, minecraft:cyan_bed[part=foot], minecraft:cyan_stained_glass, minecraft:cyan_glazed_terracotta, minecraft:cyan_concrete, minecraft:cyan_concrete_powder, minecraft:cyan_candle, minecraft:prismarine_slab, minecraft:prismarine_stairs, minecraft:prismarine_wall, minecraft:warped_roots, minecraft:warped_fungus, minecraft:twisting_vines, minecraft:nether_sprouts, minecraft:sculk_sensor",
        },
        {
            "color_name": "COLOR_PURPLE",
            "rgb": ["127", "63", "178"],
            "blocks": "minecraft:shulker_box, minecraft:purple_wool, minecraft:purple_carpet, minecraft:purple_shulker_box, minecraft:purple_bed[part=foot], minecraft:purple_stained_glass, minecraft:purple_glazed_terracotta, minecraft:purple_concrete, minecraft:purple_concrete_powder, minecraft:purple_candle, minecraft:mycelium, minecraft:chorus_plant, minecraft:chorus_flower, minecraft:repeating_command_block, minecraft:bubble_coral_block, minecraft:amethyst_block, minecraft:budding_amethyst, minecraft:amethyst_cluster",
        },
        {
            "color_name": "COLOR_BLUE",
            "rgb": ["51", "76", "178"],
            "blocks": "minecraft:blue_wool, minecraft:blue_carpet, minecraft:blue_shulker_box, minecraft:blue_bed[part=foot], minecraft:blue_stained_glass, minecraft:blue_glazed_terracotta, minecraft:blue_concrete, minecraft:blue_concrete_powder, minecraft:blue_candle, minecraft:tube_coral_block",
        },
        {
            "color_name": "COLOR_BROWN",
            "rgb": ["102", "76", "51"],
            "blocks": "minecraft:dark_oak_planks, minecraft:dark_oak_log[axis=y], minecraft:stripped_dark_oak_log[axis=x], minecraft:dark_oak_wood, minecraft:stripped_dark_oak_wood, minecraft:dark_oak_sign, minecraft:dark_oak_pressure_plate, minecraft:dark_oak_trapdoor, minecraft:dark_oak_stairs, minecraft:dark_oak_slab, minecraft:dark_oak_fence_gate, minecraft:dark_oak_fence, minecraft:dark_oak_door, minecraft:spruce_log[axis=x], minecraft:brown_wool, minecraft:brown_carpet, minecraft:brown_shulker_box, minecraft:brown_bed[part=foot], minecraft:brown_stained_glass, minecraft:brown_glazed_terracotta, minecraft:brown_concrete, minecraft:brown_concrete_powder, minecraft:brown_candle, minecraft:soul_sand, minecraft:command_block, minecraft:brown_mushroom, minecraft:soul_soil",
        },
        {
            "color_name": "COLOR_GREEN",
            "rgb": ["102", "127", "51"],
            "blocks": "minecraft:green_wool, minecraft:green_carpet, minecraft:green_shulker_box, minecraft:green_bed[part=foot], minecraft:green_stained_glass, minecraft:green_glazed_terracotta, minecraft:green_concrete, minecraft:green_concrete_powder, minecraft:green_candle, minecraft:end_portal_frame, minecraft:chain_command_block, minecraft:sea_pickle, minecraft:moss_carpet, minecraft:moss_block, minecraft:dried_kelp_block",
        },
        {
            "color_name": "COLOR_RED",
            "rgb": ["153", "51", "51"],
            "blocks": "minecraft:red_wool, minecraft:red_carpet, minecraft:red_shulker_box, minecraft:red_bed[part=foot], minecraft:red_stained_glass, minecraft:red_glazed_terracotta, minecraft:red_concrete, minecraft:red_concrete_powder, minecraft:red_candle, minecraft:brick_slab, minecraft:brick_stairs, minecraft:brick_wall, minecraft:red_mushroom_block, minecraft:nether_wart, minecraft:enchanting_table, minecraft:nether_wart_block, minecraft:fire_coral_block, minecraft:red_mushroom, minecraft:shroomlight",
        },
        {
            "color_name": "COLOR_BLACK",
            "rgb": ["25", "25", "25"],
            "blocks": "minecraft:black_wool, minecraft:black_carpet, minecraft:black_shulker_box, minecraft:black_bed[part=foot], minecraft:black_stained_glass, minecraft:black_glazed_terracotta, minecraft:black_concrete, minecraft:black_concrete_powder, minecraft:black_candle, minecraft:obsidian, minecraft:end_portal, minecraft:dragon_egg, minecraft:coal_block, minecraft:end_gateway, minecraft:basalt, minecraft:polished_basalt, minecraft:smooth_basalt, minecraft:netherite_block, minecraft:crying_obsidian, minecraft:respawn_anchor, minecraft:blackstone, minecraft:gilded_blackstone",
        },
        {
            "color_name": "GOLD",
            "rgb": ["250", "238", "77"],
            "blocks": "minecraft:gold_block, minecraft:light_weighted_pressure_plate, minecraft:bell, minecraft:raw_gold_block",
        },
        {
            "color_name": "DIAMOND",
            "rgb": ["92", "219", "213"],
            "blocks": "minecraft:diamond_block, minecraft:beacon, minecraft:prismarine_brick_slab, minecraft:prismarine_brick_stairs, minecraft:dark_prismarine_slab, minecraft:dark_prismarine_stairs, minecraft:conduit",
        },
        {
            "color_name": "LAPIS",
            "rgb": ["74", "128", "255"],
            "blocks": "minecraft:lapis_lazuli_block",
        },
        {
            "color_name": "EMERALD",
            "rgb": ["0", "217", "58"],
            "blocks": "minecraft:emerald_block",
        },
        {
            "color_name": "PODZOL",
            "rgb": ["129", "86", "49"],
            "blocks": "minecraft:podzol, minecraft:spruce_planks, minecraft:spruce_log[axis=y], minecraft:stripped_spruce_log[axis=x], minecraft:spruce_wood, minecraft:stripped_spruce_wood, minecraft:spruce_sign, minecraft:spruce_pressure_plate, minecraft:spruce_trapdoor, minecraft:spruce_stairs, minecraft:spruce_slab, minecraft:spruce_fence_gate, minecraft:spruce_fence, minecraft:spruce_door, minecraft:oak_log[axis=x], minecraft:jungle_log[axis=x], minecraft:campfire, minecraft:soul_campfire",
        },
        {
            "color_name": "NETHER",
            "rgb": ["112", "2", "0"],
            "blocks": "minecraft:netherrack, minecraft:nether_brick_fence, minecraft:nether_brick_slab, minecraft:nether_brick_stairs, minecraft:nether_brick_wall, minecraft:nether_brick_chiseled, minecraft:nether_brick_cracked, minecraft:nether_gold_ore, minecraft:nether_quartz_ore, minecraft:magma_block, minecraft:red_nether_brick_slab, minecraft:red_nether_brick_stairs, minecraft:red_nether_brick_wall, minecraft:crimson_roots, minecraft:crimson_fungus, minecraft:weeping_vines",
        },
        {
            "color_name": "TERRACOTTA_WHITE",
            "rgb": ["209", "177", "161"],
            "blocks": "minecraft:white_terracotta, minecraft:calcite",
        },
        {
            "color_name": "TERRACOTTA_ORANGE",
            "rgb": ["159", "82", "36"],
            "blocks": "minecraft:orange_terracotta",
        },
        {
            "color_name": "TERRACOTTA_MAGENTA",
            "rgb": ["149", "87", "108"],
            "blocks": "minecraft:magenta_terracotta",
        },
        {
            "color_name": "TERRACOTTA_LIGHT_BLUE",
            "rgb": ["112", "108", "138"],
            "blocks": "minecraft:light_blue_terracotta",
        },
        {
            "color_name": "TERRACOTTA_YELLOW",
            "rgb": ["186", "133", "36"],
            "blocks": "minecraft:yellow_terracotta",
        },
        {
            "color_name": "TERRACOTTA_LIGHT_GREEN",
            "rgb": ["103", "117", "53"],
            "blocks": "minecraft:lime_terracotta",
        },
        {
            "color_name": "TERRACOTTA_PINK",
            "rgb": ["160", "77", "78"],
            "blocks": "minecraft:pink_terracotta",
        },
        {
            "color_name": "TERRACOTTA_GRAY",
            "rgb": ["57", "41", "35"],
            "blocks": "minecraft:gray_terracotta, minecraft:tuff",
        },
        {
            "color_name": "TERRACOTTA_LIGHT_GRAY",
            "rgb": ["135", "107", "98"],
            "blocks": "minecraft:light_gray_terracotta, minecraft:exposed_copper",
        },
        {
            "color_name": "TERRACOTTA_CYAN",
            "rgb": ["87", "92", "92"],
            "blocks": "minecraft:cyan_terracotta",
        },
        {
            "color_name": "TERRACOTTA_PURPLE",
            "rgb": ["122", "73", "88"],
            "blocks": "minecraft:purple_terracotta, minecraft:purple_shulker_box",
        },
        {
            "color_name": "TERRACOTTA_BLUE",
            "rgb": ["76", "62", "92"],
            "blocks": "minecraft:blue_terracotta",
        },
        {
            "color_name": "TERRACOTTA_BROWN",
            "rgb": ["76", "50", "35"],
            "blocks": "minecraft:brown_terracotta, minecraft:pointed_dripstone, minecraft:dripstone_block",
        },
        {
            "color_name": "TERRACOTTA_GREEN",
            "rgb": ["76", "82", "42"],
            "blocks": "minecraft:green_terracotta",
        },
        {
            "color_name": "TERRACOTTA_RED",
            "rgb": ["142", "60", "46"],
            "blocks": "minecraft:red_terracotta",
        },
        {
            "color_name": "TERRACOTTA_BLACK",
            "rgb": ["37", "22", "16"],
            "blocks": "minecraft:black_terracotta",
        },
        {
            "color_name": "CRIMSON_NYLIUM",
            "rgb": ["189", "48", "49"],
            "blocks": "minecraft:crimson_nylium",
        },
        {
            "color_name": "CRIMSON_STEM",
            "rgb": ["148", "63", "97"],
            "blocks": "minecraft:crimson_planks, minecraft:crimson_log[axis=y], minecraft:stripped_crimson_log[axis=x], minecraft:crimson_wood, minecraft:stripped_crimson_wood, minecraft:crimson_sign, minecraft:crimson_pressure_plate, minecraft:crimson_trapdoor, minecraft:crimson_stairs, minecraft:crimson_slab, minecraft:crimson_fence_gate, minecraft:crimson_fence, minecraft:crimson_door",
        },
        {
            "color_name": "CRIMSON_HYPHAE",
            "rgb": ["92", "25", "29"],
            "blocks": "minecraft:crimson_hyphae, minecraft:stripped_crimson_hyphae",
        },
        {
            "color_name": "WARPED_NYLIUM",
            "rgb": ["22", "126", "134"],
            "blocks": "minecraft:warped_nylium, minecraft:oxidized_copper",
        },
        {
            "color_name": "WARPED_STEM",
            "rgb": ["58", "142", "140"],
            "blocks": "minecraft:warped_planks, minecraft:warped_log[axis=y], minecraft:stripped_warped_log[axis=x], minecraft:warped_wood, minecraft:stripped_warped_wood, minecraft:warped_sign, minecraft:warped_pressure_plate, minecraft:warped_trapdoor, minecraft:warped_stairs, minecraft:warped_slab, minecraft:warped_fence_gate, minecraft:warped_fence, minecraft:warped_door, minecraft:weathered_copper",
        },
        {
            "color_name": "WARPED_HYPHAE",
            "rgb": ["86", "44", "62"],
            "blocks": "minecraft:warped_hyphae, minecraft:stripped_warped_hyphae",
        },
        {
            "color_name": "WARPED_WART_BLOCK",
            "rgb": ["20", "180", "133"],
            "blocks": "minecraft:warped_wart_block",
        },
        {
            "color_name": "DEEPSLATE",
            "rgb": ["100", "100", "100"],
            "blocks": "minecraft:deepslate",
        },
        {
            "color_name": "RAW_IRON",
            "rgb": ["216", "175", "147"],
            "blocks": "minecraft:raw_iron_block",
        },
        {
            "color_name": "GLOW_LICHEN",
            "rgb": ["127", "167", "150"],
            "blocks": "minecraft:glow_lichen",
        },
    ]
    df_blocks = pd.read_json(json.dumps(blocks))
    df_blocks.drop([0], inplace=True)

    def to_minecraft_color(pxl):
        df_blocks["distance"] = df_blocks["rgb"].apply(
            lambda rgb: euclidean_distance([int(i) for i in rgb], pxl)
        )

        df_blocks.sort_values(by="distance", inplace=True)
        return df_blocks.iloc[0]["blocks"]

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

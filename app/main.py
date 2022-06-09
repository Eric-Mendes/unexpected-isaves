from PIL import Image

from src.unexpected_isaves import save_image


if __name__ == "__main__":
    valid_save_type = False
    while not valid_save_type:
        save_type = input("How do you want to save your image?: ")
        try:
            save_kwargs = {
                "image": Image.open("images/" + input("Please type the name path of your image with its extension like `my_image.png`: ")), 
                "path": "saves/" + input("Please type the name that you want to give your 'unexpected-isave' (with the extension when saving it as a spreadsheet): "),
                "lower_image_size_by": int(input("Please type the factor to lower your image's size by: ")),
            }
            if save_type == "pixel_art":
                save_kwargs["player_pos"] = tuple(map(int, input("Please type the player's position (x, y, z) separated by a space: ").split()))
                save_image.to_minecraft(**save_kwargs)
                valid_save_type = True
            elif save_type == "spreadsheet":
                save_image.to_excel(**save_kwargs)
                valid_save_type = True
            else:
                print("Invalid save_type! Available save_types are `pixel_art` or `spreadsheet`. Please try again...")
                raise ValueError
        except ValueError:
            pass

from PIL import Image
import os
import shutil

IMAGE_FOLDER_NAME = "./CharacterSpriteSheet"

def resize_image(image, target_width):
    width, height = image.size
    # Calculate the new height to maintain aspect ratio
    width_percent = (target_width / float (width))
    new_height = int((float(height) * float(width_percent)))
    return image.resize((target_width, new_height), Image.Resampling.LANCZOS)

# Normalize images to be the same height for spritesheets
def add_padding_top(image, padding_height):
    original_width, original_height = image.size
    # Create a new image with extra height for padding
    new_height = original_height + padding_height
    new_image = Image.new("RGBA", (original_width, new_height), (0, 0, 0, 0))  # Fully transparent background
    # Paste the original image onto the new image, positioned at the bottom
    new_image.paste(image, (0, padding_height))
    return new_image

# Normalize images to be the same width for spritesheets
def add_padding_left(image, padding_width):
    original_width, original_height = image.size
    # Create a new image with extra width for padding
    new_width = original_width + padding_width
    new_image = Image.new("RGBA", (new_width, original_height), (0, 0, 0, 0))  # Fully transparent background
    # Paste the original image onto the new image, positioned on the right
    new_image.paste(image, (padding_width, 0))
    return new_image

def remove_irrelevant_files(allowed_filenames):
    for filename in os.listdir(IMAGE_FOLDER_NAME):
        if filename not in allowed_filenames:
            filepath = os.path.join(IMAGE_FOLDER_NAME, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
                print(f"Deleted folder and its contents: {filepath}")

def find_max_dimensions():
    max_width = 0
    max_height = 0
    # Iterate over each file in the folder
    for filename in os.listdir(IMAGE_FOLDER_NAME):
        filepath = os.path.join(IMAGE_FOLDER_NAME, filename)
        is_image = os.path.isfile(filepath) and filename.lower().endswith(('.png'))
        if is_image:
            with Image.open(filepath) as img:
                width, height = img.size
                if width > max_width:
                    max_width = width
                if height > max_height:
                    max_height = height
    return max_width, max_height

# Function to display instructions after the script completes
def print_instructions(target_width, target_height):
    print("\n" + "=" * 50)
    print("  Instructions ")
    print("=" * 50)
    print("1. Open StreamAvatars.")
    print("2. Click the 'Open Folder' icon nad navigate to /avatars")
    print("3. Drag the generated 'spritesheet.png' into the folder.")
    print("4. Save & Reload.")
    print("5. Update Scale to 0.2 (may need to adjust accordingly).")
    print(f"6. Set Width to {target_width} and Height to {target_height}.")
    print("7. Set Idle FPS to 2 FPS.")
    print("8. Set Walk FPS to 4 FPS.")
    print("9. Connect and test new avatar")
    print("\n" + "=" * 50)
    print("Spritesheet setup is complete! Enjoy using your new MapleStory avatar :)")
    print("=" * 50)

# Default exported names for spritesheets on maples.im
allowed_filenames = [
    "stand1_0.png", "stand1_1.png", "stand1_2.png", "stand1_3.png",
    "walk1_0.png", "walk1_1.png", "walk1_2.png", "walk1_3.png",
    "sit_0.png", "jump_0.png"
]

remove_irrelevant_files(allowed_filenames)

target_width, target_height = find_max_dimensions()

# Normalize file dimensions
for filename in os.listdir(IMAGE_FOLDER_NAME):
    filepath = os.path.join(IMAGE_FOLDER_NAME, filename)
    if os.path.isfile(filepath):
        img = Image.open(filepath)
        # Add padding to images to resize heights to max height
        if (img.height < target_height):
            padded_image = add_padding_top(img, target_height-img.height)
            padded_image.save(filepath)
        # Add padding to images to resize width to max width
        if (img.width < target_width):
            padded_image = add_padding_left(img, target_width-img.width)
            padded_image.save(filepath)

# Taken from docs: https://docs.streamavatars.com/stream-avatars/content-creating/creating-avatars#sprite-sheet-format
SPRITESHEET_FORMAT = [
    ["stand1_0.png", "stand1_1.png", "stand1_2.png", "stand1_3.png"],
    ["walk1_0.png", "walk1_1.png", "walk1_2.png", "walk1_3.png"],
    ["sit_0.png", None, None, None],
    ["stand1_0.png", None, None, None],
    ["jump_0.png", None, None, None]   
]

total_width = target_width * 4
total_height = target_height * 5
spritesheet = Image.new("RGBA", (total_width, total_height))

# Iterate through the layout and paste images into the spritesheet
for row_index, row in enumerate(SPRITESHEET_FORMAT):
    for col_index, filename in enumerate(row):
        if filename is not None:
            filepath = os.path.join(IMAGE_FOLDER_NAME, filename)
            if os.path.isfile(filepath):
                img = Image.open(filepath)
                x = col_index * target_width
                y = row_index * target_height
                spritesheet.paste(img, (x, y))

spritesheet.save("./CharacterSpriteSheet/spritesheet.png")
print("Spritesheet created successfully as 'spritesheet.png'") # TODO: make output file name a console arg
print_instructions(target_width, target_height)
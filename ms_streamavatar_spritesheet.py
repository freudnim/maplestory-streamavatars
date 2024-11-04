from PIL import Image
import os
import shutil

IMAGE_FOLDER = "./CharacterSpriteSheet"
OUTPUT_FILE = "spritesheet.png"

# Add transparent padding to match target width and height.
def add_padding(image, target_width, target_height):
    new_image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
    new_image.paste(image, ((target_width - image.width) // 2, (target_height - image.height) // 2))
    return new_image

def delete_irrelevant_files(allowed_filenames):
    for filename in os.listdir(IMAGE_FOLDER):
        if filename not in allowed_filenames:
            path = os.path.join(IMAGE_FOLDER, filename)
            (os.remove if os.path.isfile(path) else shutil.rmtree)(path)
            print(f"Deleted: {path}")

def get_max_dimensions():
    max_width, max_height = 0, 0
    # Iterate over each file in the folder
    for filename in filter(lambda f: f.endswith('.png'), os.listdir(IMAGE_FOLDER)):
        with Image.open(os.path.join(IMAGE_FOLDER, filename)) as img:
            max_width, max_height = max(max_width, img.width), max(max_height, img.height)
    return max_width, max_height

# Function to display instructions after the script completes
def print_instructions(target_width, target_height):
    instructions = f"""
{"="*50}
  Instructions
{"="*50}
1. Open StreamAvatars.
2. Click the 'Open Folder' icon and navigate to /avatars.
3. Drag the generated '{OUTPUT_FILE}' into the folder.
4. Save & Reload.
5. Update Scale to 0.2 (may need adjustment).
6. Set Width to {target_width} and Height to {target_height}.
7. Set Idle FPS to 2 FPS.
8. Set Walk FPS to 4 FPS.
9. Connect and test the new avatar.
{"="*50}
Spritesheet setup is complete! Enjoy using your new MapleStory avatar :)
{"="*50}
"""
    print(instructions)

# Default exported names for spritesheets on maples.im
allowed_filenames = [
    "stand1_0.png", "stand1_1.png", "stand1_2.png", "stand1_3.png",
    "walk1_0.png", "walk1_1.png", "walk1_2.png", "walk1_3.png",
    "sit_0.png", "jump_0.png"
]

delete_irrelevant_files(allowed_filenames)

target_width, target_height = get_max_dimensions()

# Pad images to max dimensions
for filename in os.listdir(IMAGE_FOLDER):
    filepath = os.path.join(IMAGE_FOLDER, filename)
    if os.path.isfile(filepath):
        with Image.open(filepath) as img:
            padded_image = add_padding(img, target_width, target_height)
            padded_image.save(filepath)

# Taken from docs: https://docs.streamavatars.com/stream-avatars/content-creating/creating-avatars#sprite-sheet-format
SPRITESHEET_FORMAT = [
    ["stand1_0.png", "stand1_1.png", "stand1_2.png", "stand1_3.png"],
    ["walk1_0.png", "walk1_1.png", "walk1_2.png", "walk1_3.png"],
    ["sit_0.png", None, None, None],
    ["stand1_0.png", None, None, None],
    ["jump_0.png", None, None, None]   
]

spritesheet = Image.new("RGBA", (target_width * 4, target_height * 5))
for row_index, row in enumerate(SPRITESHEET_FORMAT):
    for col_index, filename in enumerate(row):
        if filename:
            filepath = os.path.join(IMAGE_FOLDER, filename)
            if os.path.isfile(filepath):
                img = Image.open(filepath)
                x = col_index * target_width
                y = row_index * target_height
                spritesheet.paste(img, (x, y))

spritesheet.save(os.path.join(IMAGE_FOLDER, OUTPUT_FILE))
print(f"Spritesheet created successfully as '{OUTPUT_FILE}'")
print_instructions(target_width, target_height)
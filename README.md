uses pillow library to generate custom spritesheets usable for StreamAvatars using https://maples.im/ to create maplestory avatars

## instructions
make character at https://maples.im/

set the following additional options:
- Animate (enabled)
- Zoom (4)
- Flip Horizontal (enabled)

export as minimal spreadsheet

drag unzipped folder (should be called CharacterSpriteSheet) in same dir as this script

`python ms_streamavatar_spritesheet.py`

at this point all sprites should have the same dimensions. sometimes it misses one (🍝), so just rerun the script again 

follow instructions printed to console

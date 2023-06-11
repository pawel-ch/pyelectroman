import copy
import glob
import json
import os
import sys

import png

folder = os.path.join("..", "data")
names = []
screens = []
sprites = [None] * 128


def load_sprite(filename):
    filename = filename.encode("ascii")
    if os.path.exists(filename):
        r = png.Reader(filename=filename)
        sprite = r.asRGBA()
        assert sprite[0] == 24
        assert sprite[1] == 24
        return list(sprite[2])
    else:
        return None


def load_sprites(set1, set2):
    global sprites
    print(f"Loading sprite sets: {set1}, {set2}")
    sprites_in_set = 64
    for sprite_index in range(1, 128):
        sprite_set = set1 if sprite_index < sprites_in_set else set2
        sprite_set_index = sprite_index % sprites_in_set
        sprite_set_path = os.path.join(folder, sprite_set, f"{sprite_set}_{sprite_set_index:02d}.png")
        sprites[sprite_index] = load_sprite(sprite_set_path)


def load_level(filename):
    with open(filename, "rt", encoding="ascii") as f:
        level = json.load(f)
    print("Loading level:", filename)
    global names, screens
    names = level["names"]
    screens = level["screens"]
    load_sprites(names[0], names[1])


def combine_screen_layers(s):
    screen = screens[s]
    line = [0] * (13 * 24 * 3)
    png_data = []
    for i in range(8 * 24):
        png_data.append(copy.deepcopy(line))
    if not screen:
        sys.stdout.write("-")
    else:
        sys.stdout.write("+")
        for layer in range(4):
            if screen[layer]:
                for y in range(8):
                    for x in range(13):
                        o = screen[layer][y * 13 + x]
                        sprite = sprites[o]
                        if sprite:
                            for r in range(24):
                                row = sprite[r]
                                for c in range(24):
                                    dc = c * 4
                                    if row[dc + 3] != 0:
                                        px = x * 24 * 3 + c * 3
                                        py = y * 24 + r
                                        png_data[py][px + 0] = row[dc + 0]
                                        png_data[py][px + 1] = row[dc + 1]
                                        png_data[py][px + 2] = row[dc + 2]
    if (s + 1) % 16 == 0:
        print()
    return png_data


TY = 16


def main():
    levels = glob.glob(os.path.join(folder, "*.ebl"))
    output_dir = os.path.join("..", "maps")
    for level in levels:
        png_screens = []
        level_name = os.path.splitext(os.path.split(level)[1])[0]
        load_level(level)
        print("Processing screens...")
        for s in range(TY * 16):
            png_screens.append(combine_screen_layers(s))
        print("Preparing big image data...")
        png_data = []
        for srow in range(24 * 8 * TY):
            png_data.append([])
            y = srow // (24 * 8)
            prow = srow % (24 * 8)
            for x in range(16):
                data = png_screens[y * 16 + x][prow]
                png_data[srow].extend(data)
        print("Writing %s file..." % (level_name + ".png"))
        with open(os.path.join(output_dir, f"{level_name}.png"), "wb") as f:
            w = png.Writer(width=24 * 13 * 16, height=24 * 8 * TY, alpha=False, greyscale=False)
            w.write(f, png_data)
    print("Done.")


if __name__ == "__main__":
    main()

## Overview

PyElectroMan is an unfinished Python rewrite of 1992 PC game Electro Man (aka Electro Body, a cult game in Poland where it was developed).

The project has been started to improve author's Python skills rather than to eventually become a released game, but it's fate will be determined by those who decide to take it further.

The port uses art assets from the original game (licensed under CC BY-SA).

The project intends to recreate the functionality of the original to some extent. The port is based on the original source code (which hasn't been publicly released) but due to its complex nature (to put it mildly) the exact conversion may not be feasible. Also the quality of the original code affects the quality of Python code - at this moment the conversion accuracy takes precedence over quality and style.

This is author's side project - the updates are when the time is permitting him to work on it.

Dependencies: Python 3.x (tested in Python 3.11), pygame and pypng.

## Running

Create a virtualenv in any way you like, ie.

```shell
pyenv install 3.11.4
pyenv local 3.11.4
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python em.py
```

## Helpful scripts

- `conversion` directory – all results for scripts from this directory are already in repository (except for one level which was modified by original author to avoid crashes)
  - `convert_sprites.py` – converts sprites to PNG
  - `convert_levels.py` – converts levels to JSON format (files with .ebl extension)
  - `display_levels.py` – converts levels to PNG format, so you can preview them easily in any software you like
- `sprite_info.py` – lets you preview all the sprites in convenient way

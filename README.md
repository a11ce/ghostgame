# ghostGame

A game in which you explore a house and run away from ghosts.

## Setup

- Download the project with `git clone https://github.com/a11ce/ghostgame.git`.
- Run with `python3 ghostGameV2.py` or `./ghostGameV2.py`

## How to play

(Colors are displayed with ANSI codes, so they may vary by system)

- You are represented by `@`, ghosts are `X`.
- Your torch has a range of 10 units. Visible (lit) empty spaces are grey, and visible walls are light red.
- As you move through the house, you will reveal more of the map. Discovered but currently not visible tiles (walls or spaces) are slightly darker than when lit.
- Undiscovered tiles are marked with a `-`. You win when you discover every empty tile inside the house.
- Both you and each ghost may move one tile per turn. Turns only advance when you make a move.
- Move with `WASD`.
- You lose if a ghost eats you by touching you.
- If you win, you will get a score based on the number of ghosts and your speed. Scores are not really indicative of anything yet.
- Press `q` to quit at any time.

## File summary

- `ghostGameV2.py`: Game logic and main loop, including movement
- `houseGen.py`: Map generator
- `graphics.py`: Console rendering of the map, player, ghosts, and HUD. Easily replaceable to add sprite graphics.
- `fov.py`: Visibility and field of view calculations for the torch, and discovery
- `getch.py`: Cross-platform getch-like function. See URL at top of file
--- 
- `ghostGameV1.py`: First version of ghostGame, buggy and relies on tdl. Also a hard-to-edit mess.
- `colors.py`: Color definitions for `ghostGameV1.py`

---

All contributions are welcome by pull request or issue.

ghostGame is licensed under GNU General Public License v3.0. See [LICENSE](../master/LICENSE) for full text.
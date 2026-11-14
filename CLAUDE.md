# The Ninefold Seal: notes for AI collaborators

Eric directs, Claude builds. Eric does not hand-write code.
Design brief (story, 18 rooms, mechanics catalog, milestones): https://claude.ai/artifact/XBSD4YXYsjNEh4fK9UwhS8

## Game
Escape rooms and nested puzzle boxes, The Room style, Lovecraftian. You play Elias Thorne, breaking nine seals.
2.5D pixel art: real 3D boxes and rooms whose faces are pixel art textures. Fez-like look. Puzzles grow more cursed act by act.

## Locked decisions
- Godot 4.5, GL Compatibility renderer. Ships as a web build on Vercel (web/), later phones and Steam.
- Touch first. Mouse emulates touch on desktop.
- 16 texels per world unit everywhere. Whole-number zoom only: room view 1 game px per texel, boxes 2, zoomed furniture 2 to 4.
- Orthographic camera. Every resting view is straight on. Lighting unshaded, quantized to 4 steps (shaders/pixel_surface.gdshader).
- Hybrid rotation: boxes and rooms follow the finger, snap to 90 degrees, commit past 30 degrees.
- Nested boxes: zoom the camera into the small box, then swap in its full-size twin (game.gd dive()).
- No fail states, no timers. Two honest hint tiers, then the Whisper's bargain (costs a journal page, counted for the ending).

## Code map
- scripts/game.gd: camera, modes (ROOM, ZOOM, BOX), input, HUD, hints and bargains, journal, audio, autotest.
- scripts/state.gd: autoload `State`. Flags, inventory, journal, bargains. Saved after every change.
- scripts/room.gd: base room. Walls, furniture, sprites, hero boxes, facing, Lens.
- scripts/data_room.gd: builds and runs any room from its JSON file. Puzzle kinds, bindings, actions.
- scripts/pixel_box.gd: any box from six pixel faces. Parts, hinges.
- data/rooms/*.json: one file per room, listed in data/rooms/index.json. No room has its own code. Format: docs/puzzle-format.md.
- data/items.json: every item's name and examine text.
- Rooms are boxes too: four walls plus optional floor and ceiling (drag up and down to see them).

## Adding a room or a puzzle
1. Art in tools/make_room_art.py (seal I), tools/make_seal2_art.py (seal II), tools/make_seal3_art.py (seal III), tools/make_seal4_art.py, tools/make_seal5_art.py, tools/make_seal6_art.py, tools/make_seal7_art.py, tools/make_sealN_art.py (room authoring scripts in tools/rooms/) for later seals; shared helpers in tools/artkit.py. 16 texels per unit. New color ramps: `python3 tools/art_lint.py palette` rebuilds the palette. Run it, then `python3 tools/art_lint.py check` (must be 0 problems).
2. Describe it in the room's JSON: objects, puzzles, bindings (every visual follows flags), interactions.
3. Main-path puzzles get a step: done condition, two hints, and the solve actions the Whisper's bargain uses.
4. walkthrough: the real taps that solve it. The autotest plays it.
5. New rooms: add to data/rooms/index.json. Every new seal also gets a main-menu shortcut: one line in SEAL_STARTS in game.gd (Eric, Nov 2026). New items: data/items.json plus an item_<id>.png icon.
6. Depth bar (Eric, Nov 2026: seal I was too simple): 12 to 16 steps per room, 3 nested layers, at least 5 puzzle types, clues that must be combined, and use the room itself (floor, ceiling, room state).

## Puzzle rules (from Eric's playtests, Nov 2026)
- The Lens reveals clues, never answers. Everything it shows must be combined with something seen without it (a cipher key, a chart, a log).
- Nothing clicks open on the right setting. Anything with settings is tried only when the player commits (winds the clock, presses the catch, taps the glass): combos use "commit", and a wrong try doesn't say which part is wrong.
- Sequences with decoys are "silent": no reset until the whole sequence is in, so they can't be solved one tap at a time.
- A clue-solved puzzle needs enough possibilities (about 100 or more) that guessing is worse than thinking.
- No puzzle type twice in one seal. A type that comes back in a later seal needs a twist.
- Everything the player can see responds to touch, even if only with a line of text. Dead taps read as bugs.
- Floor and ceiling are seen from whichever wall you were facing, so their art can appear turned round: no text or digits there that change meaning upside down (6 and 9).
- The first touch on a part of a piece of furniture zooms in; parts are worked up close. Furniture worked from the room view sets "zoom": false.
Art brief (style, sizes, palette rules): https://claude.ai/artifact/7zvHBNiA8YfQN7kr6eGhwy

## Verify every change
- After adding art or sound: `godot --headless --path . --import` first.
- `xvfb-run -a godot --path . --rendering-driver opengl3 -- --autotest` plays every room with real taps, saves screenshots to user://shots, prints AUTOTEST FAILS. It must be 0.
- Rebuild web: `godot --headless --path . --export-release "Web" web/index.html`. Pushing to main deploys to Vercel.

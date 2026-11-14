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
- data/rooms/roomN_*.json: one file per room. No room has its own code. Format: docs/puzzle-format.md.

## Adding a room or a puzzle
1. Art in tools/make_room_art.py (16 texels per unit). Run it, then `python3 tools/art_lint.py check` (must be 0 problems).
2. Describe it in the room's JSON: objects, puzzles, bindings (every visual follows flags), interactions.
3. Main-path puzzles get a step: done condition, two hints, and the solve actions the Whisper's bargain uses.
4. walkthrough: the real taps that solve it. The autotest plays it.
5. New rooms: register in game.gd ROOMS.
Art brief (style, sizes, palette rules): https://claude.ai/artifact/7zvHBNiA8YfQN7kr6eGhwy

## Verify every change
- `xvfb-run -a godot --path . --rendering-driver opengl3 -- --autotest` plays every room with real taps, saves screenshots to user://shots, prints AUTOTEST FAILS. It must be 0.
- Rebuild web: `godot --headless --path . --export-release "Web" web/index.html`. Pushing to main deploys to Vercel.

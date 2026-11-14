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
- scripts/room.gd: base room. Walls, furniture, sprites, hero boxes, steps, walkthrough.
- scripts/pixel_box.gd: any box from six pixel faces. Parts, hinges.
- scripts/rooms/roomN_*.gd: one file per room. build(), apply_state(), on_tap(), on_use(), steps, walkthrough.

## Adding a room
1. Art in tools/make_room_art.py (16 texels per unit). Run it.
2. Room script: build the walls and objects, write apply_state() so every visual follows flags.
3. steps: each with done(), two hints, and a solve() used by the bargain.
4. walkthrough: the real taps that solve the room. The autotest plays it.
5. Register it in game.gd ROOMS.

## Verify every change
- `xvfb-run -a godot --path . --rendering-driver opengl3 -- --autotest` plays every room with real taps, saves screenshots to user://shots, prints AUTOTEST FAILS. It must be 0.
- Rebuild web: `godot --headless --path . --export-release "Web" web/index.html`. Pushing to main deploys to Vercel.

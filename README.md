# Puzzle Box (prototype)

A nested puzzle box with pixel art on real 3D surfaces. Godot 4.5, touch first.

## Run it
1. Unzip anywhere. In Godot 4.5, click Import and pick `project.godot`.
2. Press F5. A mouse works like a finger on desktop.

## Play
- Drag the box: it follows your finger, then snaps to the next face.
- Tap parts to interact. Tap the slot at the bottom to select the key.
- Solution: back face clue -> set the left dials -> right panel slides up -> take the key -> select it -> tap the front lock -> tap the inner box.

## How the look works
- 16 texels per world unit on every surface. Textures use nearest filtering, no mipmaps.
- The game renders at 270x480 and scales up by whole numbers, so pixels stay square.
- Orthographic camera. At rest a face points straight at you, like Fez.
- Shader `shaders/pixel_surface.gdshader` snaps lighting to 4 steps as faces turn away.
- Nested boxes: the camera zooms into the 0.4 scale inner box, then swaps it in at full size. The swap is invisible.

## Files
- `scripts/pixel_box.gd` reusable box: 6 faces, optional hinged lid, tappable parts.
- `scripts/main.gd` level 1 puzzle logic, input, HUD, autotest.
- `tools/make_textures.py` generates all art in `assets/` (placeholder art, swap freely).

## Automated check
`godot --path . -- --autotest` plays the whole level and saves screenshots to `user://shots`.

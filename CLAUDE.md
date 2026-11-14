# Puzzle Box: notes for AI collaborators

Eric directs, Claude builds. Eric does not hand-write code.

## Game
The Room style nested puzzle boxes with escape room logic. 2.5D pixel art: real 3D boxes whose faces are pixel art textures. Fez-like look.

## Locked decisions
- Godot 4.5, GL Compatibility renderer (runs on web and mobile).
- Touch first. Mouse emulates touch on desktop.
- Hybrid rotation: box follows the finger, snaps to 90 degree faces on release (commits past 30 degrees).
- Orthographic camera. 16 texels per world unit everywhere. 2 game pixels per texel. Integer scaling only, game view fills the screen (see _fit_screen).
- Lighting is unshaded with 4 quantized steps (shaders/pixel_surface.gdshader).
- Nested boxes: zoom the camera into a 0.4 scale child box, then swap it in at full scale.

## Workflow
- Art: tools/make_textures.py generates assets/. Keep the palette and texel density.
- Verify every change: `godot --path . -- --autotest` (under xvfb when headless) plays level 1 and saves screenshots to user://shots. Update the autotest when puzzles change.
- After changes, rebuild the browser build: `godot --headless --path . --export-release "Web" web/index.html`. web/ is what gets hosted.

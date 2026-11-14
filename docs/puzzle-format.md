# Room file format (data/rooms/*.json)

Every room is one JSON file. scripts/data_room.gd reads it. No room has its own code.
Units: world units, 16 texels each. Walls are 15 wide (x from -7.5 to 7.5) and 22 tall (y from 0).
Wall keys: n, e, s, w. Textures are file names in assets/rooms/ (or assets/) without .png.

Rooms are listed in data/rooms/index.json (room number to file). Items live in data/items.json (name, examine text); icons are assets/rooms/item_<id>.png.

## The room is a box
Every room has four walls and can have a floor and a ceiling. Drag sideways to turn between walls; drag down to look up at the ceiling, up to look down at the floor.
Wall keys: n, e, s, w, plus d (floor) and u (ceiling). Floor and ceiling are 15 x 15: x across, y from the edge nearest the wall you face (0) to the far edge (15).
Furniture can have hinged faces ("hinges", same as boxes), so a wall panel can swing open like a lid.

## Top level
| Key | What it is |
| --- | --- |
| title | Shown in the top bar. |
| intro | Optional line shown when the room loads. |
| walls | Texture prefix: "r1_wall_" uses r1_wall_n, r1_wall_e, ... |
| floor, ceiling | Optional textures (240 x 240). Without them the room has no floor or ceiling view. |
| on_enter | Run when the room is built: journal entries, and "set" (only if the flag isn't set yet, for starting values). |
| objects | Everything in the room (below). |
| puzzles | Built-in puzzle kinds (below). |
| bindings | How each visual follows the state (below). |
| interactions | What happens when you tap something, or use an item on it. |
| steps | The main path, in order: hints and the bargain's solution. |
| walkthrough | The taps the autotest plays to solve the room. |

## Objects
- furniture: `{"type":"furniture","wall":"n","id":"desk","pos":[x, y_base],"size":[w,h,d],"faces":{"front":tex,"top":tex,"default":tex},"zoom":{},"parts":[...]}`
  zoom (optional): k (2 to 4 pixel zoom), dx/dy (aim offset), w/h (area to fit). Tapping furniture zooms in.
- sprite: `{"type":"sprite","wall":"n","id":"lamp","center":[x,y],"size":[w,h],"tex":"lamp","depth":1.6}`
  Options: tappable (default true), additive (glows), lens (only visible through the Lens).
- box (a hero box you can lift): `{"type":"box","name":"walnut","wall":"n","pos":[x,y],"depth":1.6,"scale":0.5,"view":"front","size":6,"faces":{...},"liner":tex,"liner_skip":["top"],"hinges":[["top","top"]],"blocker":"walnut","parts":[...],"children":[...],"inner_sprites":[...]}`
  children: smaller boxes inside it (give them `"blocker":"dive:<stage box name>"` to dive into them).
  inner_sprites: flat things inside a box: `{"id","tex","size","pos":[x,y,z],"rot":[x,y,z],"face":"top"}` (face: which side you look through to see it).
- stage_box: the full-size twin you reach by diving: `{"type":"stage_box","name":"walnut_inner","view":"top",...}`.
- parts (on any furniture or box face): `{"face":"front","uv":[x,y],"size":[w,h],"tex":"drawer","id":"drawer","depth":0.03}`
  Options: tappable, lens. Higher depth sits in front.

## Puzzle kinds
- cycler: a part that steps through states each tap. `{"kind":"cycler","part":"clock_hand","flag":"clock_hour","count":12,"start":7,"rotate":-30}` or `"textures":[...]`. Options: lock (condition that freezes it), locked_say, sfx, spin (false = just swap pictures), on: `{"3":[actions]}` runs when it reaches that state.
- combo: several flags matching a code. `{"kind":"combo","flags":["dial0","dial1","dial2"],"code":[1,3,2],"lock":"panel_open","commit":"catch","fail":[actions],"do":[actions]}`
  With "commit" (use it for every real puzzle), the code is only tried when the player taps that part, and a wrong try gives no hint which part is wrong. Without it, the combo opens the moment it matches, which lets players turn things until something clicks.
- sequence: parts pulled in an order; a wrong pull resets. With "silent": true, nothing resets or clicks until the whole sequence is in (use it whenever there are decoys, so it can't be solved one step at a time). `{"kind":"sequence","flag":"books","parts":{"book_green":"g",...},"order":"gbr","tex":{...},"fail":[actions],"do":[actions]}`
- radial: concentric rings on one touch area; the ring is chosen by distance from the centre. `{"kind":"radial","part":"rings","rings":[["ring_core",0.7],["ring_mid",1.32],["ring_outer",2.05]],"rotate":-90}`
- pickup: take an item. `{"kind":"pickup","part":"clock_key","item":"brass_key","flag":"brass_taken","show_if":"clock_open","then":[actions]}`
- dark: a wall too dark to use until a flag. `{"kind":"dark","wall":"e","until":"lamp_lit","say":"Too dark..."}`
- sliding parts: a cycler with "offsets" moves its part instead of turning it. `{"kind":"cycler","part":"barT","flag":"barT","count":3,"spin":false,"offsets":[[-0.5,0],[0,0],[0.5,0]],"lock":["any","!barM=0"]}`. Interlocks are just lock conditions on other bars.
- beam: light crossing a grid of cells on one face. Mirrors are cyclers with 4 textures (/ - \ |).
  `{"kind":"beam","id":"lamp_beam","box":"carriage","face":"top","cols":6,"rows":6,"cell":0.75,"source":[0,3,"e"],"when":"lamp_lit","mirrors":[["mir1","mir1",2,3,0]],"fixed":[[4,1,0,"lens"]],"blocks":[[3,3]],"targets":[{"cell":[4,0],"flag":"beam_sea","do":[actions]}]}`
  Rows count from the top. mirrors: [part, flag, col, row, start]. fixed: [col, row, state] plus "lens" for a mirror that only exists through the Lens. A target's "do" runs once, the first time the beam reaches it. "box" can also be a furniture id.
- roll: a pearl in a tilt maze. Tapping a button part rolls it until a wall cell or the edge stops it.
  `{"kind":"roll","box":"chest","face":"front","cols":6,"rows":4,"cell":0.5,"center":[-0.875,0.125],"token":"pearl","flag":"pearl","start":[0,0],"walls":[[1,0]],"goal":[5,2],"done":"pearl_home","buttons":{"tilt_n":"n","tilt_s":"s","tilt_e":"e","tilt_w":"w"},"do":[actions]}`

- lights: a toggle grid. Pressing a cell flips it and its four neighbours. `{"kind":"lights","flag":"pins","cols":3,"rows":3,"parts":["pin0",...],"on":"pin_up","off":"pin_down","start":"000000000","goal":"001101001","done":"pins_done","lock":...,"do":[actions]}`
- Several combos can share one "commit" part (an index lever that opens different drawers): the first whose code matches runs; if none, the first one's "fail" runs.

## Room state that changes behind your back
Every turn to another wall adds 1 to the "turns" flag (reset when a room loads). Use it in conditions with a modulo: `"turns%5=4"`. Rooms refresh after each turn, so anything bound to turns moves while its wall is out of view.
Binding values can show a flag: `{"texture":"tally_{turns:30}"}` uses tally_ plus the turns count, capped at 30.

## Items you work in the tray (data/items.json)
`"wire": ["Name", "Examine text", {"reshape": {"label": "Bend it", "to": "wire_hook", "say": "..."}}]`: examining it shows a button that turns it into another item ("to" can be a list to pull it apart into several, plus an optional "journal").
`"key_bow": [..., {"combine": {"key_blade": {"makes": "sew_key", "say": "..."}}}]`: select one, then touch the other in the tray.

## Conditions
"flag", "!flag", "item:x", "lens", "flag=3", or a list (all must hold). A list starting with "any" holds if any of the rest holds: `["any","tide=0","tide=1"]`.

## Bindings
`{"target":"drawer","when":"drawer_open","then":{"texture":"drawer_open","tappable":false},"else":{"texture":"drawer"},"anim":0.6,"delay":0.4}`
Targets: a part or sprite id, "box:<name>" (the box's own touch area), "hinge:<box>.<face>", "wall:<key>".
Properties: texture, visible, tappable, offset [dx,dy], hinge (degrees), gone (hides a Lens-only part for good).
Changes animate when the state changes during play; on load everything snaps.

## Actions
set (+ value), unset, give, take, sfx, say (+ secs), journal [key, title, text], fragment, shake, wait, refresh, face (turn the box in your hands), complete_room [next room, card title, card text].
Text can use {fragments} and {bargains_line}.

## Interactions
`{"on":"tap","id":"door","when":"!door_open","do":[actions]}` and `{"on":"use","item":"door_key","id":"door","do":[actions]}`.
Use "ids": [...] instead of "id" to match several things with one entry.
The first match wins. "handled": false lets furniture still zoom after the actions. Lifting a box asks for tap "lift:<name>" first, so a room can refuse it.

## Steps
`{"id":"drawer","done":"drawer_open","hints":["nudge","what to do"],"solve":[actions],"said":"what the Whisper did"}`
Steps are the main path in order. Optional puzzles stay out of steps.

## Walkthrough
["tap", id], ["use", item, id], ["tapat", id, [x,y]], ["repeat", n, action], ["back"], ["face", f], ["lens", true],
["swipe", dx], ["swipev", dy], ["tapv", id] (tap from the current view, no turning), ["hint"], ["examine", item], ["reshape", item], ["combine", a, b], ["journal"], ["wait", s], ["shot", name], ["expect", flag].
The autotest can start at any room: `-- --autotest --start=5`.

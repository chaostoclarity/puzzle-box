from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
C = 0.75
def cuv(c, r, n=5, cell=C): return [(c - (n - 1) / 2) * cell, ((n - 1) / 2 - r) * cell]
MAZE_WALLS = [[1, 0], [1, 2], [2, 0], [3, 2], [3, 3], [4, 1]]
WATER_IDS = ["water_%s_%d" % (k, l) for k in "nesw" for l in (0, 1)] + ["water_floor"]

objs = []
for k in "nesw":
    objs += [sprite(k, "water_%s_0" % k, [0, 4.5], [15, 9], "water_9", depth=3.6),
             sprite(k, "water_%s_1" % k, [0, 2.5], [15, 5], "water_5", depth=3.6),
             sprite(k, "water_%s_2" % k, [0, 0.75], [15, 1.5], "water_1", depth=3.6, tappable=False)]
objs += [
 sprite("d", "carving", [0, 9], [8, 3], "carving", depth=0.03),
 sprite("d", "water_floor", [0, 7.5], [15, 15], "water_floor", depth=0.2),
 sprite("u", "skylight", [0, 7.5], [4, 4], "skylight"),
 {"type": "box", "name": "chest", "wall": "n", "pos": [-3, 1], "depth": 1.0, "scale": 0.5, "view": "front", "size": [8, 4, 4],
  "faces": {"front": "chest_front", "back": "chest_back", "left": "chest_side", "right": "chest_side", "top": "chest_top", "bottom": "chest_top"},
  "liner": "chest_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "chest",
  "parts": [part("front", [-0.875 - 1.25, 0.125 + 0.75], [0.5, 0.5], "pearl", "pearl", depth=0.04, tappable=False),
            part("front", [-0.875, 1.6], [0.75, 0.75], "tilt_n", "tilt_n"),
            part("front", [-0.875, -1.6], [0.75, 0.75], "tilt_s", "tilt_s"),
            part("front", [-3.0, 0.125], [0.75, 0.75], "tilt_w", "tilt_w"),
            part("front", [1.25, 0.125], [0.75, 0.75], "tilt_e", "tilt_e"),
            part("front", [2.59, 0.03], [1, 1.25], "keyhole", "keyhole", depth=0.03),
            part("front", [2.59, 0.03], [1, 1.25], "keyhole_cover", "keyhole_cover", depth=0.045)],
  "inner_sprites": [{"id": "fbottom", "tex": "fbottom", "size": [5, 3], "pos": [0, -0.2, 0], "rot": [-90, 0, 0], "face": "top"},
                    {"id": "keyhole2", "tex": "keyhole2", "size": [0.75, 1], "pos": [2.0, -0.15, 0.4], "rot": [-90, 0, 0], "face": "top"}],
  "children": [{"name": "binnacle_mini", "faces": {"front": "binn_front", "back": "binn_back", "left": "binn_left", "right": "binn_right",
                "top": "binn_top", "bottom": "binn_bottom"}, "liner": "binn_liner", "hinges": [["top", "top"]],
                "blocker": "dive:binnacle", "scale": 0.25, "pos": [0, -1.2, 0]}]},
 {"type": "stage_box", "name": "binnacle", "view": "top",
  "faces": {"front": "binn_front", "back": "binn_back", "left": "binn_left", "right": "binn_right", "top": "binn_top", "bottom": "binn_bottom"},
  "liner": "binn_liner", "hinges": [["top", "top"]], "blocker": "binnacle",
  "parts": [part("top", cuv(0, 4), [C, C], "lsocket", "lsocket"),
            part("top", cuv(2, 4), [C, C], "mirror_1", "bm1"),
            part("top", cuv(2, 1), [C, C], "mirror_3", "bm2"),
            part("top", cuv(4, 1), [C, C], "ghost_mirror", "ghost", depth=0.035, tappable=False, lens=True),
            part("top", cuv(4, 0), [C, C], "fisheye", "fisheye", tappable=False)],
  "inner_sprites": [{"id": "seal2_part", "tex": "item_seal_stone2", "size": [1.5, 1.5], "pos": [0, -1.5, 0], "rot": [-90, 0, 0], "face": "top"}]},
 sprite("n", "port_n", [3.5, 13], [3, 3], "porthole"),
 {"type": "furniture", "wall": "e", "id": "ctable", "pos": [-2, 0], "size": [7, 9.5, 2.5],
  "faces": {"front": "ctable_front", "top": "wood_top_112x40", "default": "wood_side_40x152"}, "zoom": {"k": 2, "dy": 3, "w": 7.5, "h": 8}},
 sprite("e", "clog", [-3.5, 10.25], [2.5, 1.5], "clog", depth=1.3),
 sprite("e", "chart", [-2, 15], [5, 4], "chart"),
 sprite("e", "port_e", [4.5, 13], [3, 3], "porthole"),
 sprite("e", "captain", [4.5, 18], [3, 4], "portrait_captain"),
 {"type": "furniture", "wall": "s", "id": "pump", "pos": [3.5, 0], "size": [2, 11, 1.5],
  "faces": {"front": "pump_front", "default": "iron_side_24x176"}, "zoom": False,
  "parts": [part("front", [0, 4.2], [1, 1], "pump_socket", "pump_socket", depth=0.04)]},
 sprite("s", "gauge", [0.5, 5.5], [1.5, 10], "gauge", depth=0.04),
 sprite("s", "cdoor", [-4.5, 5], [4, 10], "cdoor"),
 sprite("w", "seacock", [3.5, 6.5], [2, 2], "seacock_rust", depth=0.2),
 sprite("w", "shelf", [-3, 10.5], [5, 1], "shelf", depth=0.3),
 sprite("w", "chest_key_part", [-3, 11.375], [1.5, 0.75], "small_chest_key", depth=0.35),
]

log_j = journal("penhallow_log", "Captain's log", "The log of the Constance, Josiah Penhallow master. Water-stained, the last pages in pencil:\n\n\"Struck the reef following Pike's light, which turned on us. Hull holed. She floods at the flood and drains at the ebb, and the pump and the sea-cock between them will hold her at any mark you please.\"\n\n\"Left the chest key on the high shelf, where only the flood can carry a man.\"\n\n\"The chest won't show its lock till the pearl is home.\"\n\n\"NEVER drain her past the third mark.\"\n\n\"The binnacle's light will not reach the fish's eye. Brass cannot make that turn. The glass can.\"")
abyss_j = journal("abyss", "Past the third mark", "I pumped past the third mark. The water did not drop. It left. It went out through the portholes and the sea went with it, and through the glass I could see the reef standing up out of dry mud for miles, and on the mud, something lying with one eye open, the size of a church.\n\nIt was the thing the beam found. It came closer while I wasn't looking.")
seal_j = journal("seal2", "The second seal", "A second stone, cold and wet, inside the binnacle where the compass should be. The moment I lifted it the sea remembered the wreck and came back for it.\n\nSeven remain. Wren stopped at three. I am beginning to understand why, and I am beginning not to care.")
card = ["SEAL II OF IX BROKEN", "You come up through the skylight into black water and swim for the light. When you look back, the wreck is gone, and so is the reef.\n\nYou carry the stone home to Wren's cabinet."]

tide = lambda v: "tide=%d" % v
pump = [
 taps(["pump", "pump_socket"], [say("A bilge pump with no handle. There's a square socket where it should go.")], when="!pump_fitted"),
 taps(["pump", "pump_socket"], [{"set": "tide", "value": 1}, {"sfx": "water"}, say("You work the crank. The water drops to the second mark.")], when=tide(0)),
 taps(["pump", "pump_socket"], [{"set": "tide", "value": 2}, {"set": "drained"}, {"sfx": "water"}, say("The water drops to the third mark. The chest on the north wall is clear.")], when=tide(1)),
 taps(["pump", "pump_socket"], [{"set": "tide", "value": 3}, {"sfx": "water"}, {"wait": 0.6}, {"sfx": "horn"}, {"shake": True}, abyss_j,
              say("Past the third mark the water doesn't drop. It leaves. Through the portholes, the sea is gone.", 6)], when=tide(2)),
 taps(["pump", "pump_socket"], [say("Nothing left to pump. Nothing left anywhere.")], when=tide(3)),
]
seacock = [
 tap("seacock", [say("The sea-cock. Rusted solid.")], when="!cock_free"),
 tap("seacock", [{"set": "tide", "value": 2}, {"sfx": "water"}, say("The sea comes back in through the cock, to the third mark.")], when=tide(3)),
 tap("seacock", [{"set": "tide", "value": 1}, {"sfx": "water"}, say("Water rushes in, up to the second mark.")], when=tide(2)),
 tap("seacock", [{"set": "tide", "value": 0}, {"sfx": "water"}, say("The sea pours in to the first mark. You float, chest-deep.")], when=tide(1)),
 tap("seacock", [say("Open as far as it goes.")], when=tide(0)),
]

interactions = [
 taps(WATER_IDS, [say("Under the water. Cold enough to stop your heart.")]),
 tap("clog", [{"sfx": "paper"}, log_j, say("The captain's log. It's in your journal.")]),
 tap("chart", [say("A chart of Kingsport. A pencil line runs from the light to the reef.")]),
 tap("captain", [say("Captain Penhallow. The paint has run where the sea got at it.")]),
 tap("cdoor", [say("The cabin door. Jammed by the tilt of the hull.")]),
 tap("gauge", [say("A tide gauge painted on the bulkhead. Marks 1, 2 and 3. The 3 is in red.")]),
 tap("port_n", [say("Green water and drifting sand.")], when="!tide=3"),
 tap("port_e", [say("Green water and drifting sand.")], when="!tide=3"),
 taps(["port_n", "port_e"], [say("Dry mud to the horizon. The eye is closer.")]),
 uses("crank", ["pump", "pump_socket"], [{"take": "crank"}, {"set": "pump_fitted"}, {"sfx": "thunk"}, say("The lighthouse crank fits the pump's socket exactly.")]),
] + pump + seacock + [
 use("oil_can", "seacock", [{"take": "oil_can"}, {"set": "cock_free"}, {"sfx": "creak"}, say("You empty the oil can over the wheel. It groans, and gives.")]),
 tap("chest_key_part", [{"give": "chest_key"}, {"set": "key_taken"}, {"sfx": "pickup"}, say("Floating at the high-water mark, you reach the shelf. A key shaped like a crab.")],
     when=[tide(0), "!key_taken"]),
 tap("chest_key_part", [say("Out of reach. If the water were higher you could float up to it.")], when="!key_taken"),
 tap("lift:chest", [{"shake": True}, say("It's under the water, and bolted down besides.")], when=["any", tide(0), tide(1)]),
 tap("keyhole_cover", [say("A brass cover over the keyhole. Something behind the maze holds it.")]),
 use("chest_key", "keyhole_cover", [say("The keyhole is covered.")]),
 use("chest_key", "keyhole", [{"set": "chest_open"}, {"sfx": "unlock"}, {"wait": 0.4}, {"sfx": "creak"}, {"face": "top"},
      say("The lid comes up. Inside, a false bottom with words carved into it.")], when="!chest_open"),
 tap("fbottom", [say("Carved in the boards: NEVER DRAIN HER PAST THE THIRD MARK.")], when="!tide=3"),
 tap("fbottom", [say("A second keyhole has opened in the boards. It wasn't there before.")]),
 use("chest_key", "keyhole2", [{"take": "chest_key"}, {"set": "fb_open"}, {"sfx": "unlock"}, {"sfx": "slide"}, {"face": "top"},
      say("The key turns. The false bottom lifts away. Beneath it, a ship's binnacle.")]),
 use("chest_key", "fbottom", [say("No keyhole. Not yet.")]),
 use("lantern", "lsocket", [{"take": "lantern"}, {"set": "binnacle_lit"}, {"sfx": "flame"}, say("The lantern fits the binnacle's socket. Its light runs out across the brass.")]),
 tap("lsocket", [say("An empty lamp socket.")], when="!binnacle_lit"),
 tap("fisheye", [say("A brass fish. Its eye is glass.")]),
 tap("carving", [journal("carving", "Carved in the deck", "Cut deep into the deck where the water used to be: THE GLASS TURNS WHAT BRASS CANNOT."), say("Words cut into the deck. They're in your journal.")], when=tide(3)),
 tap("skylight", [{"set": "escaped"}, {"sfx": "water"}, {"complete_room": [102] + card}], when=["seal2_taken", tide(0)]),
 tap("skylight", [say("The skylight, far overhead. Too high to reach unless the water carried you.")]),
]

puzzles = [
 {"kind": "roll", "id": "maze", "box": "chest", "face": "front", "cols": 6, "rows": 4, "cell": 0.5, "center": [-0.875, 0.125],
  "token": "pearl", "flag": "pearl", "start": [0, 0], "walls": MAZE_WALLS, "goal": [5, 2], "done": "pearl_home", "lock": "pearl_home",
  "locked_say": "The pearl is home.", "buttons": {"tilt_n": "n", "tilt_s": "s", "tilt_e": "e", "tilt_w": "w"},
  "do": [{"wait": 0.2}, {"sfx": "thunk"}, {"wait": 0.3}, {"sfx": "slide"}, say("The pearl drops into a channel. The brass cover jumps off the keyhole.")]},
 {"kind": "cycler", "part": "bm1", "flag": "bm1", "count": 4, "start": 1, "spin": False, "sfx": "click",
  "textures": ["mirror_0", "mirror_1", "mirror_2", "mirror_3"], "lock": "fish_lit"},
 {"kind": "cycler", "part": "bm2", "flag": "bm2", "count": 4, "start": 3, "spin": False, "sfx": "click",
  "textures": ["mirror_0", "mirror_1", "mirror_2", "mirror_3"], "lock": "fish_lit"},
 {"kind": "beam", "id": "binn_beam", "box": "binnacle", "face": "top", "cols": 5, "rows": 5, "cell": C,
  "source": [0, 4, "e"], "when": "binnacle_lit", "mirrors": [["bm1", "bm1", 2, 4, 1], ["bm2", "bm2", 2, 1, 3]],
  "fixed": [[4, 1, 0, "lens"]],
  "targets": [{"cell": [4, 0], "flag": "fish_lit", "do": [{"sfx": "hum"}, {"wait": 0.8}, {"sfx": "unlock"}, {"set": "binnacle_open"},
     say("The beam bends where no mirror is and strikes the fish's eye. The binnacle opens.", 5)]}]},
 {"kind": "pickup", "part": "seal2_part", "item": "seal_stone2", "flag": "seal2_taken", "show_if": "binnacle_open", "sfx": "reveal",
  "then": [seal_j, {"wait": 0.8}, {"set": "tide", "value": 0}, {"sfx": "water"}, {"sfx": "horn"},
           say("The hull groans. The sea comes back all at once. Swim up!", 5)]},
]

bindings = []
for k in "nesw":
    bindings += [vis("water_%s_0" % k, tide(0)), vis("water_%s_1" % k, tide(1)),
                 bind("water_%s_2" % k, tide(2), {"visible": True}, {"visible": False})]
bindings += [
 bind("water_floor", ["any", tide(0), tide(1), tide(2)], {"visible": True}, {"visible": False}),
 bind("water_floor", ["any", tide(0), tide(1)], {"tappable": True}, {"tappable": False}),
 tex("port_n", tide(3), "porthole_abyss", "porthole"), tex("port_e", tide(3), "porthole_abyss", "porthole"),
 tex("pump_socket", "pump_fitted", "pump_socket_crank", "pump_socket"),
 tex("seacock", "cock_free", "seacock", "seacock_rust"),
 vis("chest_key_part", "!key_taken"),
 vis("keyhole_cover", "!pearl_home"),
 bind("hinge:chest.top", "chest_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("box:chest", "chest_open", {"tappable": False}, {"tappable": True}),
 vis("fbottom", "!fb_open"),
 vis("keyhole2", [tide(3), "!fb_open"]),
 tex("lsocket", "binnacle_lit", "lsocket_lit", "lsocket"),
 tex("fisheye", "fish_lit", "fisheye_lit", "fisheye"),
 bind("hinge:binnacle.top", "binnacle_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("hinge:binnacle_mini.top", "binnacle_open", {"hinge": 110}, {"hinge": 0}),
 bind("box:binnacle", "binnacle_open", {"tappable": False}, {"tappable": True}),
 tex("skylight", "seal2_taken", "skylight_open", "skylight"),
]

steps = [
 step("pump", "pump_fitted", ["The bilge pump on the south wall is missing its handle. You carried one down from the light.", "Fit the lamp crank into the pump's square socket."],
      [{"take": "crank"}, {"set": "pump_fitted"}], "The crank is in the pump."),
 step("cock", "cock_free", ["The sea-cock on the west wall is rusted shut.", "Use the oil can on the sea-cock."], [{"take": "oil_can"}, {"set": "cock_free"}], "The sea-cock turns freely."),
 step("flood", ["any", "key_taken", tide(0)], ["The shelf on the west wall is out of reach. Water lifts whatever floats, you included.", "Open the sea-cock until the water reaches the first mark."],
      [{"set": "tide", "value": 0}], "The sea pours in."),
 step("key", "key_taken", ["Something glints on the high shelf.", "At high water, take the key from the shelf on the west wall."], [{"give": "chest_key"}, {"set": "key_taken"}], "The crab key is yours."),
 step("drain", ["any", "drained", "chest_open"], ["The chest on the north wall is under the water.", "Work the pump until the water is down to the third mark."],
      [{"set": "tide", "value": 2}, {"set": "drained"}], "The water drains to the third mark."),
 step("maze", "pearl_home", ["The chest's keyhole is covered. The pearl maze beside it is the latch.",
      "Lift the chest. Each arrow tilts it and the pearl rolls until it hits something. Roll it into the hole on the right of the maze."],
      [{"set": "pearl", "value": "5,2"}, {"set": "pearl_home"}], "The pearl rolls home."),
 step("chest", "chest_open", ["The keyhole is clear now.", "Use the crab key on the chest's keyhole."], [{"set": "chest_open"}], "The chest lid lifts."),
 step("abyss", ["any", tide(3), "fb_open"], ["The false bottom warns you about the third mark. Warnings are also instructions.", "Pump past the third mark."],
      [{"set": "tide", "value": 3}, abyss_j], "The sea goes away."),
 step("bottom", "fb_open", ["Something has changed in the chest's false bottom.", "Use the crab key on the new keyhole in the chest's false bottom."],
      [{"take": "chest_key"}, {"set": "fb_open"}], "The false bottom lifts."),
 step("lantern", "binnacle_lit", ["The binnacle has an empty lamp socket. You carried a light down from the tower.", "Dive into the binnacle and put the storm lantern in its socket."],
      [{"take": "lantern"}, {"set": "binnacle_lit"}], "The binnacle is lit."),
 step("beam", "fish_lit", ["The beam has to reach the brass fish's eye, and no mirror can turn it there. The captain's log and the carving both say the glass can.",
      "Turn both mirrors to lean like /, then look through the Lens. A mirror appears that brass can't make."],
      [{"set": "bm1", "value": 0}, {"set": "bm2", "value": 0}, {"set": "fish_lit"}, {"set": "binnacle_open"}], "The light bends. The binnacle opens."),
 step("seal", "seal2_taken", ["Something waits inside the binnacle.", "Take the stone from inside the binnacle."],
      [{"give": "seal_stone2"}, {"set": "seal2_taken"}, seal_j, {"set": "tide", "value": 0}], "The second seal is yours, and the sea is coming."),
 step("escape", "escaped", ["The sea is back, all the way up. Look up.", "Swipe down to look up, and swim out through the skylight."],
      [{"set": "escaped"}, {"complete_room": [102] + card}], "Up you go."),
]

walk = [["shot", "start"], ["tap", "clog"], ["tapat", "pump", [0, 4.5]], ["use", "crank", "pump_socket"], ["tap", "seacock"], ["use", "oil_can", "seacock"],
 ["tap", "chest_key_part"], ["tap", "seacock"], ["shot", "high_tide"], ["tap", "chest_key_part"], ["expect", "key_taken"],
 ["repeat", 2, ["tapat", "pump", [0, 4.5]]], ["shot", "low_tide"], ["expect", "drained"],
 ["tap", "chest"], ["shot", "chest"],
 ["tap", "tilt_s"], ["tap", "tilt_e"], ["tap", "tilt_n"], ["tap", "tilt_e"], ["tap", "tilt_n"], ["tap", "tilt_e"], ["tap", "tilt_s"], ["tap", "tilt_w"], ["tap", "tilt_n"], ["tap", "tilt_e"],
 ["wait", 1.0], ["expect", "pearl_home"], ["shot", "pearl_home"],
 ["use", "chest_key", "keyhole"], ["wait", 1.0], ["shot", "chest_open"], ["tap", "fbottom"],
 ["tapat", "pump", [0, 4.5]], ["wait", 1.0], ["shot", "abyss"], ["tap", "port_n"], ["tap", "carving"], ["shot", "floor_dry"],
 ["use", "chest_key", "keyhole2"], ["wait", 0.5], ["shot", "binnacle_found"], ["tap", "dive:binnacle"],
 ["use", "lantern", "lsocket"], ["shot", "binnacle_lit"],
 ["repeat", 3, ["tap", "bm1"]], ["tap", "bm2"], ["shot", "no_lens"], ["lens", True], ["wait", 2.0], ["shot", "lens_beam"], ["expect", "fish_lit"], ["lens", False],
 ["tap", "seal2_part"], ["wait", 1.0], ["shot", "flooded"], ["tap", "skylight"], ["wait", 2.0]]

room = {"title": "The Constance", "walls": "r4_wall_", "floor": "r4_floor", "ceiling": "r4_ceiling",
        "on_enter": [{"set": "tide", "value": 1},
          journal("wreck", "The wreck", "The captain's cabin of the Constance, lying on her side on the reef. Sea water to my waist, and the tide still coming and going through the holes in her. Pike's beam found her. I think she has been here longer than Pike has.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room4_wreck.json", room)
print("room4 ok")

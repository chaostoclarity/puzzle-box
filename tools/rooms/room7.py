from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
C = 0.75
def cuv(c, r): return [(c - 2) * C, 1.25 + (1 - r) * C]
TILES = [("m1", 1, 1, 1), ("m2", 1, 0, 3), ("m3", 3, 0, 0), ("m4", 3, 1, 1), ("m5", 1, 2, 0), ("m6", 3, 2, 2)]
CROPORDER = ["crop_3", "crop_0", "crop_5", "crop_2", "crop_4", "crop_1"]   # wheat peas bean squash apple corn
NOTES = journal("nahum", "Nahum Gardner's notes", "Pencil on a feed-store calendar page, the writing going grey like everything else:\n\n\"Whatever I cut grows back by the time I've done eight things. The flower on the table goes the same way. I watch it to know how long I have.\"\n\n\"Abby locked the safe three ways: the grey on the top latch, the root in the tin, and the seed jars in her planting order. All three at once or none.\"\n\n\"Her beans give one pod in three breaths. Pick it green and it's the key to her bread tin. Leave it longer and the grey takes it.\"\n\n\"The almanac's gone grey too. Only the colour can read it now.\"")
ALMANAC = journal("almanac", "The almanac", "Through the Lens the greyed-out almanac reads: MARCH PEAS. APRIL WHEAT. MAY CORN. JUNE SQUASH.")

objs = [
 {"type": "furniture", "wall": "n", "id": "piesafe", "pos": [-1, 0], "size": [6, 10, 2.5], "hinges": [["front", "left"]],
  "faces": {"front": "piesafe_front", "top": "grey_top_96x40", "default": "grey_side_40x160"}, "zoom": {"k": 2},
  "parts": [part("front", [0, 4.0], [1, 0.75], "latch_shut", "latch_top"),
            part("front", [0, 4.0], [2, 1.5], "root_knot", "root_top", depth=0.045),
            part("front", cuv(0, 1), [C, C], "root_stub", "root_stub", tappable=False),
            part("front", cuv(2, 1), [C, C], "rivet_block", "rivet_block", tappable=False),
            part("front", cuv(4, 1), [C, C], "mlatch_shut", "latch_mid", tappable=False)] +
           [part("front", cuv(c, r), [C, C], "rtile_%d" % s, m) for m, c, r, s in TILES] +
           [part("front", [-1.5 + 1.5 * i, -2.375], [1, 1], CROPORDER[0], "jar%d" % i) for i in range(3)] +
           [part("front", [2.4, -3.3], [1, 0.5], "jar_latch", "jar_latch", depth=0.04)]},
 sprite("n", "seed_packet", [-2.5, 7], [0.75, 1], "seed_packet", depth=1.0),
 {"type": "box", "name": "breadtin", "wall": "n", "pos": [-0.5, 3.5], "depth": 1.2, "scale": 0.4, "view": "front", "size": [6, 4, 4],
  "faces": {"front": "tin_front2", "back": "btin_back", "left": "btin_side", "right": "btin_side", "top": "btin_top", "bottom": "btin_top"},
  "liner": "btin_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "breadtin",
  "parts": [part("front", [0, -0.1], [1, 1.25], "clear", "pod_lock", depth=0.04)],
  "children": [{"name": "abby_mini", "faces": {"front": "abby_front", "back": "abby_back", "left": "abby_side", "right": "abby_side", "top": "abby_top", "bottom": "abby_bottom"},
                "liner": "abby_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "dive:abby", "scale": 0.3, "pos": [0, -1.0, 0]}]},
 {"type": "stage_box", "name": "abby", "view": "front",
  "faces": {"front": "abby_front", "back": "abby_back", "left": "abby_side", "right": "abby_side", "top": "abby_top", "bottom": "abby_bottom"},
  "liner": "abby_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "abby",
  "parts": [part("bottom", [0, -0.5], [1, 1], "abby_button", "abby_button", depth=0.04)],
  "inner_sprites": [{"id": "handle_part", "tex": "item_handle", "size": [1.5, 1.5], "pos": [-0.8, -1.5, -1.0]},
                    {"id": "bkey_part", "tex": "item_back_key", "size": [1.5, 1.5], "pos": [0.8, -1.5, -1.0]}]},
 {"type": "furniture", "wall": "e", "id": "stove", "pos": [-4, 0], "size": [4, 4, 2], "faces": {"front": "stove_front", "default": "iron_side_32x64"}, "zoom": False},
 sprite("e", "farm_window", [2.5, 11], [4, 4], "farm_window"),
 sprite("e", "pot", [2.5, 7.5], [1.5, 2], "pot_empty", depth=0.5),
 sprite("s", "back_door", [3, 4.5], [4.5, 9], "back_door"),
 sprite("s", "door_roots", [3, 4.5], [5, 6], "door_roots", depth=0.1),
 sprite("s", "almanac", [-3.5, 11], [4, 5], "almanac"),
 sprite("s", "almanac_lens", [-3.5, 11], [4, 5], "almanac_lens", depth=0.05, lens=True),
 {"type": "furniture", "wall": "w", "id": "table", "pos": [0, 0], "size": [7, 3.5, 3], "faces": {"front": "table_front", "top": "grey_top_112x48", "default": "grey_side_48x56"}, "zoom": False},
 sprite("w", "flower", [2, 4.5], [1, 2], "flower_0", depth=1.5),
 sprite("w", "nahum_notes", [-1.5, 4.25], [2, 1.5], "nahum_notes", depth=1.5),
 sprite("u", "shears_part", [2, 9], [2, 1.5], "shears_part"),
 sprite("u", "ceiling_roots", [0, 7.5], [12, 12], "clear", depth=0.01),
 sprite("d", "ash_ring", [0, 7.5], [8, 8], "clear", depth=0.01),
]

puzzles = [
 {"kind": "pickup", "part": "shears_part", "item": "shears", "flag": "shears_taken", "then": [say("You pull Nahum's shears out of the roots in the ceiling.")]},
 {"kind": "pickup", "part": "seed_packet", "item": "seeds", "flag": "seeds_taken", "show_if": "safe_open", "then": [say("A twist of paper: three grey beans. FOR THE TIN.")]},
] + [
 {"kind": "cycler", "part": m, "flag": m, "count": 4, "start": s, "spin": False, "sfx": "click",
  "textures": ["rtile_%d" % k for k in range(4)], "lock": "safe_open"} for m, c, r, s in TILES
] + [
 {"kind": "beam", "id": "root_beam", "box": "piesafe", "face": "front", "cols": 5, "rows": 3, "cell": C, "center": [0, 1.25],
  "source": [0, 1, "e"], "additive": False, "tex_h": "seg_root_h", "tex_v": "seg_root_v", "thick": 4,
  "mirrors": [[m, m, c, r, s] for m, c, r, s in TILES], "blocks": [[2, 1]],
  "targets": [{"cell": [4, 1], "flag": "l2", "do": [{"sfx": "creak"}, say("The root grows through the tin and shoves the middle latch open.")]}]},
] + [
 {"kind": "cycler", "part": "jar%d" % i, "flag": "jar%d" % i, "count": 6, "spin": False, "sfx": "tick", "textures": CROPORDER, "lock": "safe_open"} for i in range(3)
] + [
 {"kind": "combo", "flags": ["jar0", "jar1", "jar2"], "code": [1, 5, 3], "commit": "jar_latch", "lock": ["any", "safe_open", "l3"],
  "locked_say": "The bottom latch is already open.", "fail": [{"sfx": "thunk"}, say("The bottom latch doesn't move.")],
  "do": [{"set": "l3"}, {"sfx": "unlock"}, say("Peas, corn, squash. The bottom latch drops.")]},
 {"kind": "combo", "flags": ["l1", "l2", "l3"], "code": [1, 1, 1], "lock": "safe_open",
  "do": [{"set": "safe_open"}, {"wait": 0.3}, {"sfx": "door"}, say("All three latches at once. The pie safe swings open, and the grey stops.", 5)]},
 {"kind": "rot", "watch": "l1", "after": 8, "until": "safe_open", "decay": [{"unset": "l1"}, {"sfx": "creak"}, say("The grey root has grown back over the top latch.")]},
 {"kind": "rot", "watch": "l2", "after": 8, "until": "safe_open", "decay": [{"unset": "l2"}, {"set": "m4", "value": 1}, {"sfx": "creak"}, say("The root in the tin withers, and a tile twists out of line.")]},
 {"kind": "rot", "watch": "l3", "after": 8, "until": "safe_open", "decay": [{"unset": "l3"}, {"set": "jar1", "value": 0}, {"sfx": "thunk"}, say("A seed jar slips round, and the bottom latch climbs shut.")]},
 {"kind": "rot", "watch": "droot_cut", "after": 4, "until": "left7", "decay": [{"unset": "droot_cut"}, {"sfx": "creak"}, say("The root across the back door has grown back.")]},
 {"kind": "grow", "flag": "bean", "while": "planted", "max": 5},
 {"kind": "pickup", "part": "handle_part", "item": "handle", "flag": "handle_taken", "show_if": "abby_open", "then": [say("An iron crank handle. For the well.")]},
 {"kind": "pickup", "part": "bkey_part", "item": "back_key", "flag": "bkey_taken", "show_if": "abby_open", "then": [say("A grey iron key.")]},
]

bindings = [
 tex("latch_top", "l1", "latch_open", "latch_shut"),
 vis("root_top", "!l1"),
 tex("latch_mid", "l2", "mlatch_open", "mlatch_shut"),
 tex("jar_latch", "l3", "latch_open", "jar_latch"),
 bind("flower", None, {"texture": "flower_{rot_age:8}"}),
 bind("hinge:piesafe.front", "safe_open", {"hinge": 100}, {"hinge": 0}, anim=1.2),
 bind("box:piesafe", "safe_open", {"tappable": False}, {"tappable": True}),
 bind("hinge:breadtin.top", "btin_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("box:breadtin", "btin_open", {"tappable": False}, {"tappable": True}),
 bind("hinge:abby.front", "abby_open", {"hinge": 100}, {"hinge": 0}, anim=0.9),
 bind("hinge:abby_mini.front", "abby_open", {"hinge": 100}, {"hinge": 0}),
 bind("box:abby", "abby_open", {"tappable": False}, {"tappable": True}),
 bind("pot", "planted", {"texture": "pot_{bean:5}"}, {"texture": "pot_empty"}),
 bind("pot", "pod_taken", {"texture": "pot_2"}),
 vis("door_roots", "!droot_cut"),
 tex("back_door", "left7", "back_door_open", "back_door"),
]

interactions = [
 tap("nahum_notes", [{"set": "notes_read"}, {"sfx": "paper"}, NOTES, say("Nahum Gardner's notes. They're in your journal.")]),
 tap("flower", [say("A cut flower in a jar. It wilts as you watch, and recovers when you stop.")]),
 tap("almanac", [{"set": "almanac_read"}, ALMANAC, say("Through the Lens: MARCH PEAS. APRIL WHEAT. MAY CORN. JUNE SQUASH.", 6)], when="lens"),
 tap("almanac", [say("A planting almanac, gone grey. The months are there; the crops have faded out.")]),
 tap("root_top", [say("A grey root, tight round the top latch.")]),
 use("shears", "root_top", [{"set": "l1"}, {"sfx": "slide"}, say("Snip. The top latch springs open. Somewhere a clock starts.")]),
 use("shears", "door_roots", [{"set": "droot_cut"}, {"sfx": "slide"}, say("You cut the root across the door. It's already twitching.")]),
 tap("door_roots", [say("Grey roots across the back door, thick as a wrist.")]),
 tap("back_door", [say("Locked.")], when="!door_unlocked"),
 uses("back_key", ["back_door", "door_roots"], [{"take": "back_key"}, {"set": "door_unlocked"}, {"sfx": "unlock"}, say("The back door unlocks.")]),
 tap("back_door", [{"set": "left7"}, {"take": "seeds"}, {"sfx": "door"},
     {"complete_room": [8, "THE WELL", "The yard behind the farmhouse is grey ash to the fence. In the middle of it, a well house, and from the well a smell like struck matches.\n\nThe chain is down."]}],
     when=["door_unlocked", "droot_cut"]),
 tap("pot", [say("A pot of grey soil on the sill.")], when=["!planted"]),
 use("seeds", "pot", [{"take": "seeds"}, {"set": "planted"}, {"set": "bean", "value": 0}, {"sfx": "slide"}, say("You press a bean into the soil. It stirs at once.")], when="!planted"),
 tap("pot", [{"give": "pod_key"}, {"unset": "planted"}, {"set": "pod_taken"}, {"sfx": "pickup"}, say("One green pod, curved like a key. You pick it.")], when=["planted", "bean=3"]),
 tap("pot", [{"unset": "planted"}, {"set": "bean", "value": 0}, {"give": "seeds"}, {"sfx": "creak"}, say("Too late. The pod has gone grey and crumbles. You still have beans.")], when=["planted", ["any", "bean=4", "bean=5"]]),
 tap("pot", [say("Not ready. Green, and growing as you watch.")], when="planted"),
 tap("pod_lock", [say("A curved keyhole, like a crescent. Or a bean pod.")], when="!btin_open"),
 use("pod_key", "pod_lock", [{"take": "pod_key"}, {"set": "btin_open"}, {"sfx": "unlock"}, {"face": "top"}, say("The pod turns in the lock like a key. In the bread tin: a small velvet box.")]),
 tap("abby_button", [{"set": "abby_open"}, {"sfx": "unlock"}, {"face": "front"}, say("Click. Abby's box opens.")], when="!abby_open"),
 tap("stove", [say("A cold iron stove. The ash inside is the wrong grey.")]),
 tap("farm_window", [say("Grey light, and specks in it of a colour you can't name.")]),
 tap("table", [say("The kitchen table. Nobody has eaten here in a long time.")]),
 tap("ceiling_roots", [say("Roots have come through the ceiling boards, grey and dry.")]),
 tap("ash_ring", [say("A ring of grey ash on the floor, as if something stood here and burned without fire.")]),
]

steps = [
 step("notes", "notes_read", ["Someone left notes on the kitchen table.", "Read Nahum Gardner's notes on the table (west wall)."], [{"set": "notes_read"}, NOTES], "The notes are in your journal."),
 step("shears", "shears_taken", ["Something is caught in the roots overhead.", "Drag down to look up. Take the shears from the ceiling roots."], [{"give": "shears"}, {"set": "shears_taken"}], "The shears are yours."),
 step("almanac", "almanac_read", ["The seed jars want Abby's planting order. The almanac on the south wall has gone grey.", "Read the almanac with the Lens on."], [{"set": "almanac_read"}, ALMANAC], "The almanac reads through the Lens."),
 step("safe", "safe_open", ["All three latches have to be open at once, and each one goes back after eight moves. Watch the flower. Do the slow one first, the quick ones last.",
      "Set the jars to peas, corn, squash first but don't press their latch. Turn the tiles so the root reaches the right-hand latch. Then press the jar latch, then cut the top root with the shears."],
      [{"set": "l1"}, {"set": "l2"}, {"set": "l3"}, {"set": "safe_open"}], "The pie safe opens."),
 step("seeds", "seeds_taken", ["The pie safe held something for the garden.", "Take the seed packet from inside the pie safe."], [{"give": "seeds"}, {"set": "seeds_taken"}], "The seeds are yours."),
 step("pod", ["any", "item:pod_key", "btin_open"], ["Abby's beans give a pod in three breaths. The pot is on the east windowsill.",
      "Plant a bean in the pot, do two other things, then pick the pod when it's green and curved. Too long and it rots."],
      [{"take": "seeds"}, {"give": "pod_key"}, {"set": "pod_taken"}], "A green pod, shaped like a key."),
 step("tin", "btin_open", ["The bread tin in the pie safe has a curved keyhole.", "Lift the bread tin and use the bean pod in its keyhole."], [{"take": "pod_key"}, {"set": "btin_open"}], "The bread tin opens."),
 step("abby", "abby_open", ["Abby's velvet box has no lock on its front. Turn it over.", "Dive into the velvet box, turn it to its bottom and press the button there."], [{"set": "abby_open"}], "Abby's box opens."),
 step("items", ["handle_taken", "bkey_taken"], ["Abby's box held two things.", "Take the crank handle and the key from Abby's box."], [{"give": "handle"}, {"give": "back_key"}, {"set": "handle_taken"}, {"set": "bkey_taken"}], "Handle and key."),
 step("door", "door_unlocked", ["The back door is locked.", "Use the grey key on the back door (south wall)."], [{"take": "back_key"}, {"set": "door_unlocked"}], "The door unlocks."),
 step("leave", "left7", ["The roots across the door grow back in four moves.", "Cut the roots across the back door with the shears, then go straight through the door."],
      [{"set": "left7"}, {"complete_room": [8, "THE WELL", "Out in the grey yard, the well house waits."]}], "Out you go."),
]

walk = [["shot", "start"], ["tap", "nahum_notes"], ["tap", "flower"], ["tap", "shears_part"], ["shot", "ceiling"],
 ["tap", "almanac"], ["lens", True], ["tap", "almanac"], ["shot", "almanac_lens"], ["lens", False],
 ["tap", "piesafe"], ["shot", "safe"],
 ["use", "shears", "root_top"], ["expect", "l1"],
 ["tap", "jar0"], ["repeat", 5, ["tap", "jar1"]], ["repeat", 3, ["tap", "jar2"]],
 ["shot", "rotted"],
 ["tap", "m1"], ["tap", "m1"], ["tap", "m1"], ["tap", "m2"], ["tap", "m3"], ["tap", "m3"], ["tap", "m4"], ["expect", "l2"], ["shot", "root_grown"],
 ["tap", "jar_latch"], ["expect", "l3"], ["use", "shears", "root_top"], ["wait", 1.5], ["expect", "safe_open"], ["shot", "safe_open"],
 ["tap", "seed_packet"], ["use", "seeds", "pot"], ["tap", "pot"], ["tap", "farm_window"], ["tap", "pot"], ["shot", "pod"], ["expect", "pod_taken"],
 ["tap", "breadtin"], ["use", "pod_key", "pod_lock"], ["wait", 1.0], ["tap", "dive:abby"], ["tap", "abby_button"], ["wait", 1.2], ["expect", "abby_open"],
 ["tap", "handle_part"], ["tap", "bkey_part"],
 ["use", "shears", "door_roots"], ["use", "back_key", "back_door"], ["tap", "back_door"], ["expect", "left7"], ["wait", 2.0]]

room = {"title": "The Gardner Kitchen", "walls": "r7_wall_", "floor": "r7_floor", "ceiling": "r7_ceiling",
        "intro": "Everything here grows back.",
        "on_enter": [{"set": "jar0", "value": 0}, {"set": "jar1", "value": 0}, {"set": "jar2", "value": 0},
          journal("kitchen", "The Gardner farm", "The Gardner farm, west of Arkham, where the land went grey after a stone fell in the well. The kitchen is furred with roots. A pie safe stands against the wall, strangled shut. Everything I cut grows back.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room7_kitchen.json", room)
print("room7 ok")

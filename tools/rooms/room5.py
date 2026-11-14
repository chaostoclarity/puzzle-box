from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
GOAL = "001101001"
PIN_UV = [[x, y] for y in (0.9, 0.03, -0.84) for x in (-0.875, 0, 0.875)]
DIARY = journal("ada_diary", "Ada Merrow's diary", "Pages sewn into the mattress ticking, in a small careful hand:\n\n\"Admitted 1911. They say I tried to open something that should stay shut. I say I was nearly through.\"\n\n\"The stool walks when I do not watch it. I have counted. It rests beneath the window on the fourth look, and on every tenth look after that.\"\n\n\"I broke my key in two to keep it from them. One half where the water goes. One half where only the stool can take me.\"\n\n\"My pins are on my handkerchief. The last row they tore away. I put it where they never look.\"")
NOTE = journal("ada_note", "Scratched note", "Scratched into the plaster beside the tally marks: IT WALKS WHEN I DO NOT WATCH. COUNT MY LOOKS. ON THE 4TH IT RESTS BY THE WINDOW.")
STOOL = {"n": ([-6, 1], 0), "w": ([3.5, 1], 1), "e": ([-5, 1], 3), "s": ([0, 1], 4)}

objs = [
 {"type": "furniture", "wall": "n", "id": "cot", "pos": [-2.5, 0], "size": [8, 3, 3],
  "faces": {"front": "cot_front", "top": "cot_top", "default": "iron_side_48x48"}, "zoom": {"k": 2},
  "parts": [part("front", [3, -0.75], [1, 1], "loose_spring", "spring"),
            part("front", [0, 0.9], [7.5, 1], "clear", "mattress", depth=0.02)]},
 sprite("n", "kerchief", [-2.5, 6.5], [3, 3], "kerchief"),
 {"type": "box", "name": "sewbox", "wall": "n", "pos": [4.5, 0.8], "depth": 1.2, "scale": 0.4, "view": "front", "size": [6, 4, 4],
  "faces": {"front": "sew_front", "back": "sew_back", "left": "sew_side", "right": "sew_side", "top": "sew_top", "bottom": "sew_top"},
  "liner": "sew_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "sewbox",
  "parts": [part("front", [0, -0.09], [1, 1.25], "clear", "sew_lock", depth=0.04)] +
           [part("top", PIN_UV[i], [0.75, 0.75], "pin_down", "pin%d" % i) for i in range(9)],
  "children": [{"name": "case_mini", "faces": {"front": "case_front", "back": "case_back", "left": "case_side", "right": "case_side", "top": "case_top", "bottom": "case_top"},
                "liner": "case_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "dive:needlecase", "scale": 0.3, "pos": [0, -1.0, 0]}]},
 {"type": "stage_box", "name": "needlecase", "view": "front",
  "faces": {"front": "case_front", "back": "case_back", "left": "case_side", "right": "case_side", "top": "case_top", "bottom": "case_top"},
  "liner": "case_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "needlecase",
  "parts": [part("front", [0, 0], [1, 1.5], "zig_keyhole", "zig_lock", depth=0.04)],
  "inner_sprites": [{"id": "locket_part", "tex": "item_locket", "size": [1.5, 1.5], "pos": [0, -1.5, -1.0]}]},
 sprite("e", "cell_door", [0, 5.5], [5, 11], "cell_door"),
 sprite("e", "tile_socket", [1.59, 5.375], [1, 1], "tile_socket", depth=0.06),
 sprite("s", "cell_window", [0, 15.5], [4, 4], "cell_window"),
 sprite("s", "sill", [0, 13.25], [4, 0.5], "sill", depth=0.3),
 sprite("s", "tally", [-4.5, 9], [3, 2], "tally_0"),
 sprite("s", "ada_note", [4.5, 9], [2, 3], "ada_note"),
 {"type": "furniture", "wall": "w", "id": "washstand", "pos": [-3, 0], "size": [4, 4, 2],
  "faces": {"front": "washstand_front", "top": "tile_top_64x32", "default": "tile_side_32x64"}, "zoom": False},
 sprite("w", "tin_mirror", [-3, 9], [2, 3], "tin_mirror"),
 sprite("w", "cup_w", [-2, 4.375], [0.75, 0.75], "tin_cup", depth=1.0),
 sprite("n", "cup_n", [-5.5, 3.375], [0.75, 0.75], "tin_cup", depth=2.5),
 sprite("d", "drain", [0, 7.5], [2, 2], "drain"),
 sprite("u", "bulb", [0, 7.5], [2, 2], "bulb_cage"),
 sprite("u", "ceiling_pins", [0, 11], [3, 3], "ceiling_pins", tappable=False, lens=True),
]
for k, (c, _) in STOOL.items():
    objs.append(sprite(k, "stool_" + k, c, [2, 2], "stool", depth=1.0))

puzzles = [
 {"kind": "pickup", "part": "spring", "item": "wire", "flag": "wire_taken", "then": [say("You work a length of spring wire loose from the cot. Hold it in your tray to bend it.", 5)]},
 {"kind": "lights", "flag": "pins", "cols": 3, "rows": 3, "parts": ["pin%d" % i for i in range(9)], "on": "pin_up", "off": "pin_down",
  "start": "000000000", "goal": GOAL, "done": "pins_done", "lock": ["any", "pins_done", "!sew_unlocked"],
  "locked_say": "The pins are locked down. The box's keyhole is on the front.",
  "do": [{"wait": 0.3}, {"sfx": "unlock"}, {"set": "sew_open"}, {"wait": 0.8}, say("The pins match her handkerchief. The lid lifts.")]},
 {"kind": "pickup", "part": "locket_part", "item": "locket", "flag": "locket_taken", "show_if": "case_open",
  "then": [say("A brass locket. It doesn't open like a locket. Hold it in your tray.", 5)]},
]

bindings = [vis("stool_%s" % k, "turns%%5=%d" % r) for k, (_, r) in STOOL.items()]
bindings += [
 bind("tally", None, {"texture": "tally_{turns:30}"}),
 vis("cup_w", "turns%2=0"), vis("cup_n", "turns%2=1"),
 tex("drain", "bow_taken", "drain_empty", "drain"),
 bind("hinge:sewbox.top", "sew_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("box:sewbox", "sew_open", {"tappable": False}, {"tappable": True}),
 bind("hinge:needlecase.front", "case_open", {"hinge": 100}, {"hinge": 0}, anim=0.9),
 bind("hinge:case_mini.front", "case_open", {"hinge": 100}, {"hinge": 0}),
 bind("box:needlecase", "case_open", {"tappable": False}, {"tappable": True}),
 tex("tile_socket", "door_unlocked", "tile_socket_full", "tile_socket"),
 tex("cell_door", "door_unlocked", "cell_door_open", "cell_door"),
]

WIRES = ["wire", "wire_hook", "wire_zigzag"]
interactions = [
 tap("mattress", [{"set": "diary_read"}, {"sfx": "paper"}, DIARY, say("Pages sewn into the mattress. Ada Merrow's diary. It's in your journal.", 5)]),
 tap("kerchief", [journal("kerchief", "The handkerchief", "Pinned above the cot: a handkerchief embroidered with a grid of nine squares. Some are crossed through in red. The right-hand column has been torn away."),
                  say("A handkerchief: a grid of nine squares, some crossed. The right column is torn away.")]),
 tap("ada_note", [NOTE, say("Words scratched beside the tally marks. They're in your journal.")]),
 tap("tally", [say("Tally marks scratched into the plaster. There's one more every time you look away.")]),
 taps(["stool_n", "stool_e", "stool_s", "stool_w"], [say("A heavy stool. It won't budge while you watch it.")]),
 tap("sill", [{"give": "key_blade"}, {"set": "blade_taken"}, {"sfx": "pickup"}, say("You climb the stool. On the sill, behind the bars: the toothed half of a small key.")],
     when=["turns%5=4", "!blade_taken"]),
 tap("sill", [say("The sill is too high to reach. If you had something to stand on...")], when="!blade_taken"),
 tap("sill", [say("An empty sill, and the night outside.")]),
 tap("drain", [say("Something glints on a ring below the grate. Your fingers won't fit through.")], when="!bow_taken"),
 tap("drain", [say("An empty drain.")]),
 use("wire_hook", "drain", [{"give": "key_bow"}, {"set": "bow_taken"}, {"sfx": "pickup"}, say("The hook catches the ring. Up it comes: the round half of a small key.")], when="!bow_taken"),
 uses("wire", ["drain"], [say("The straight wire slides right off. It needs a hook.")]),
 uses("wire_zigzag", ["drain"], [say("It won't catch. It needs a hook.")]),
 tap("bulb", [say("A bare bulb in a wire cage. It hums.")]),
 tap("tin_mirror", [say("A polished tin mirror. Your face in it is a little late.")]),
 tap("washstand", [say("A tiled washstand. The basin is dry.")]),
 taps(["cup_w", "cup_n"], [say("A tin cup. Wasn't it on the other side of the room?")]),
 tap("sew_lock", [say("Locked. A small brass keyhole.")], when="!sew_unlocked"),
 use("sew_key", "sew_lock", [{"take": "sew_key"}, {"set": "sew_unlocked"}, {"sfx": "unlock"}, {"face": "top"},
      say("The lock turns. On top, nine pins in a pincushion are free to move.")]),
 use("wire_zigzag", "zig_lock", [{"set": "case_open"}, {"sfx": "unlock"}, say("The zigzag wire finds every ward. The needle case drops open.")], when="!case_open"),
 uses("wire", ["zig_lock"], [say("Wrong shape. The keyhole is a jagged slot.")]),
 uses("wire_hook", ["zig_lock"], [say("Wrong shape. The keyhole is a jagged slot.")]),
 tap("zig_lock", [say("A keyhole shaped like a jagged slot. No key fits that.")], when="!case_open"),
 tap("cell_door", [say("Locked. In the lock plate, a square socket, like a missing tile.")], when="!door_unlocked"),
 uses("tile", ["tile_socket", "cell_door"], [{"take": "tile"}, {"set": "door_unlocked"}, {"sfx": "unlock"}, {"wait": 0.4}, {"sfx": "door"},
      say("The tile sinks into the lock plate. The eye opens. So does the door.")]),
 tap("tile_socket", [say("A square socket, the size of a tile.")], when="!door_unlocked"),
 tap("cell_door", [{"set": "left5"}, {"take": "wire_zigzag"}, {"take": "wire"}, {"take": "wire_hook"}, {"complete_room": [6, "THE RECORDS ROOM", "The corridor outside Ada's cell is dark and goes the wrong way. At its end, a door marked RECORDS stands open.\n\nThe porter has gone home."]}], when="door_unlocked"),
]

steps = [
 step("diary", "diary_read", ["Ada left more than scratches. Look at her cot.", "Touch the cot's mattress to find Ada's diary sewn into it."], [{"set": "diary_read"}, DIARY], "The diary is in your journal."),
 step("wire", "wire_taken", ["Something on the cot's iron frame is loose.", "Take the loose spring from the front of the cot."], [{"give": "wire"}, {"set": "wire_taken"}], "You have a length of wire."),
 step("hook", ["any", "bow_taken", "item:wire_hook"], ["Something glints under the drain in the floor. Your fingers won't reach it.", "Hold the wire in your tray and bend it into a hook."],
      [{"take": "wire"}, {"take": "wire_zigzag"}, {"give": "wire_hook"}], "The wire is a hook."),
 step("bow", "bow_taken", ["One half of Ada's key is \"where the water goes\".", "Look down. Use the wire hook on the drain."], [{"give": "key_bow"}, {"set": "bow_taken"}], "Half a key."),
 step("blade", "blade_taken", ["The tally counts your looks. The stool only moves when you look away, and it's at the window on the fourth look and every tenth after.",
      "Turn so that you face the window (south wall) on your 4th, 14th or 24th turn since you came in. Then touch the sill."], [{"give": "key_blade"}, {"set": "blade_taken"}], "The other half of the key."),
 step("key", ["any", "item:sew_key", "sew_unlocked"], ["Two halves of one key.", "In your tray, select one half of the key, then touch the other."],
      [{"take": "key_bow"}, {"take": "key_blade"}, {"give": "sew_key"}], "The halves join."),
 step("unlock", "sew_unlocked", ["The sewing box by the cot is locked.", "Lift the sewing box and use Ada's key on its keyhole."], [{"take": "sew_key"}, {"set": "sew_unlocked"}], "The box unlocks."),
 step("pins", "pins_done", ["The nine pins should match Ada's handkerchief, all of it. The torn column is somewhere they never look; it only shows through the Lens.",
      "Pressing a pin flips it and its neighbours. Aim for: top row up only on the right; middle row left and right up; bottom row right up. Press top middle, top right, middle left, middle right, bottom middle, bottom right."],
      [{"set": "pins", "value": GOAL}, {"set": "pins_done"}, {"set": "sew_open"}], "The pins rise. The lid lifts."),
 step("zig", ["any", "case_open", "item:wire_zigzag"], ["The needle case has a jagged keyhole, and Ada drew her key inside the box's lid.", "Hold the wire in your tray and bend it until it's a zigzag."],
      [{"take": "wire"}, {"take": "wire_hook"}, {"give": "wire_zigzag"}], "The wire is a zigzag."),
 step("case", "case_open", ["The needle case in the sewing box is locked.", "Dive into the needle case and use the zigzag wire on its keyhole."], [{"set": "case_open"}], "The case opens."),
 step("locket", "locket_taken", ["Something lies in the needle case.", "Take the locket from the needle case."], [{"give": "locket"}, {"set": "locket_taken"}], "The locket is yours."),
 step("tile", ["any", "item:tile", "door_unlocked"], ["The locket doesn't open like a locket.", "Hold the locket in your tray and pull it apart."],
      [{"take": "locket"}, {"give": "tile"}], "The locket folds into a tile."),
 step("door", "door_unlocked", ["The cell door has a square socket in its lock plate.", "Use the eye tile on the socket in the door."], [{"take": "tile"}, {"set": "door_unlocked"}], "The door opens."),
 step("leave", "left5", ["The door is open.", "Go through the cell door."],
      [{"set": "left5"}, {"complete_room": [6, "THE RECORDS ROOM", "At the end of the corridor, a door marked RECORDS stands open."]}], "Out you go."),
]

walk = [["shot", "start"], ["tap", "mattress"], ["tap", "kerchief"], ["tap", "spring"], ["examine", "wire"], ["reshape", "wire"],
 ["tap", "drain"], ["use", "wire_hook", "drain"], ["expect", "bow_taken"], ["shot", "floor"],
 ["lens", True], ["tap", "bulb"], ["shot", "ceiling_lens"], ["lens", False],
 ["tap", "ada_note"], ["tap", "sill"], ["shot", "south_no_stool"], ["swipe", -120], ["swipe", 120], ["shot", "south_stool"], ["tapv", "sill"], ["expect", "blade_taken"],
 ["combine", "key_bow", "key_blade"],
 ["tap", "sewbox"], ["tap", "pin0"], ["use", "sew_key", "sew_lock"], ["shot", "pins"],
 ["tap", "pin1"], ["tap", "pin2"], ["tap", "pin3"], ["tap", "pin5"], ["tap", "pin7"], ["tap", "pin8"], ["wait", 1.5], ["expect", "sew_open"], ["shot", "sew_open"],
 ["reshape", "wire_hook"], ["tap", "dive:needlecase"], ["tap", "zig_lock"], ["shot", "case"], ["use", "wire_zigzag", "zig_lock"], ["wait", 1.2], ["expect", "case_open"],
 ["tap", "locket_part"], ["examine", "locket"], ["reshape", "locket"], ["examine", "tile"], ["tap", "cell_door"], ["use", "tile", "tile_socket"], ["shot", "door_open"], ["tap", "cell_door"], ["wait", 2.0]]

room = {"title": "Ada Merrow's Cell", "walls": "r5_wall_", "floor": "r5_floor", "ceiling": "r5_ceiling",
        "intro": "Room 9, Arkham Sanitarium. The door locks behind you.",
        "on_enter": [journal("cell", "The cell", "Arkham Sanitarium, room 9, the cell on the admission form. The porter locked the door behind me without being asked. Tally marks on the plaster. A cot. A sewing box made out of cot slats. Someone lived here a long time ago and did not leave.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room5_cell.json", room)
print("room5 ok")

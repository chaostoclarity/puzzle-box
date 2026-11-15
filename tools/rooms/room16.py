from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
FRAG = [{"set": "frag8"}, {"fragment": True}, {"sfx": "reveal"},
        journal("frag8", "Fragment VIII", "Through dream sight, on the cellar brick in Wren's hand: WAKE UP ELIAS IT IS ONLY A LOOP. And under it, smaller: \"It isn't only a loop. It is the eighth seal, and it keeps whoever can't count. Count.\""),
        say("Through dream sight, on the brick: WAKE UP ELIAS IT IS ONLY A LOOP. In Wren's hand.", 5)]
objs = [
 sprite("n", "wine_rack", [0, 4], [6, 7], "wine_rack"),
 sprite("n", "label_1", [1.5, 4.5], [1.25, 0.75], "label_1", depth=0.06),
 sprite("n", "jar_shelf", [-5, 7], [6, 2], "jar_shelf"),
 sprite("n", "candle16", [-5, 8.6], [1, 3], "dcandle_0", depth=0.3),
 sprite("e", "coal_chute", [0, 8], [4, 4], "coal_chute"),
 sprite("e", "label_2", [0, 7], [1.5, 0.75], "label_2", depth=0.06),
 sprite("e", "wren16", [-4.5, 5], [3, 4], "wren_lens3", lens=3),
 sprite("w", "grate", [0, 3], [3, 3], "cellar_grate"),
 sprite("w", "label_3", [0, 3], [2, 0.75], "label_3", depth=0.06),
 sprite("s", "cellar_door", [0, 4.5], [5, 9], "cellar_door"),
] + [sprite("s", "cdl%d" % i, [-1 + i, 5.5], [0.75, 0.75], "ddial_0", depth=0.06) for i in range(3)] + [
 sprite("s", "handle16", [1.8, 4], [1, 1], "cellar_handle", depth=0.06),
 sprite("s", "stone8", [0, 1.2], [1.5, 1.5], "item_seal_stone8", depth=0.08),
]
RESET = ["cdl0", "cdl1", "cdl2", "chute_open", "grate_open"]
puzzles = [
 {"kind": "loop", "every": 12, "flag": "loop", "max": 4, "until": "door_open", "reset": RESET,
  "do": [{"sfx": "wind"}, {"shake": True}, say("The candle gutters. You are standing at the foot of the cellar stairs again, and everything you did is undone. Only the candle remembers: it is a notch shorter.", 5), {"refresh": True}]},
] + [{"kind": "cycler", "part": "cdl%d" % i, "flag": "cdl%d" % i, "count": 10, "spin": False, "sfx": "tick", "textures": ["ddial_%d" % k for k in range(10)], "lock": "door_open"} for i in range(3)] + [
 {"kind": "combo", "flags": ["cdl0", "cdl1", "cdl2"], "code": [3, 1, 2], "commit": "handle16", "lock": "door_open",
  "fail": [{"sfx": "thunk"}, say("The handle won't turn.")],
  "do": [{"set": "door_open"}, {"sfx": "unlock"}, {"sfx": "creak"}, say("The handle turns. The door opens on a stair going up, and on the bottom step, a dark stone with an eye in it. The candle steadies. The loop has let go.", 6)]},
 {"kind": "pickup", "part": "stone8", "item": "seal_stone8", "flag": "stone8_taken", "show_if": "door_open", "then": [say("The eighth seal. Its eye closes as you pick it up.")]},
]
bindings = [
 bind("candle16", None, {"texture": "dcandle_{loop:4}"}),
 vis("label_1", "loop=0"),
 vis("label_2", ["loop=1", "chute_open"]),
 vis("label_3", ["loop=2", "grate_open"]),
 vis("cellar_door", "loop>2"),
 tex("cellar_door", "door_open", "cellar_door_open", "cellar_door"),
 vis("handle16", ["loop>2", "!door_open"]),
] + [vis("cdl%d" % i, ["loop>2", "!door_open"]) for i in range(3)]
interactions = [
 tap("label_1", [{"set": "seen1"}, say("A label on a bottle, in chalk: I 3. The first is three.")]),
 tap("label_2", [{"set": "seen2"}, say("Chalked inside the chute: II 1. The second is one.")]),
 tap("label_3", [{"set": "seen3"}, say("Scratched under the grate: III 2. The third is two.")]),
 tap("wine_rack", [say("A wine rack. Every bottle is the same vintage: a year that hasn't happened.")]),
 tap("jar_shelf", [say("Jars of preserves, all labelled in your handwriting, all empty.")]),
 tap("candle16", [say("Your candle, on the shelf where you didn't put it. Five notches down its side. Every time the cellar starts over, it burns down one.")]),
 tap("coal_chute", [{"set": "chute_open"}, {"sfx": "creak"}, say("You heave the chute's hatch open. Coal dust and cold air.")], when="!chute_open"),
 tap("coal_chute", [say("The coal chute, open. It goes up to a street that isn't there.")]),
 tap("grate", [{"set": "grate_open"}, {"sfx": "creak"}, say("You prise the drain grate up an inch and wedge it.")], when="!grate_open"),
 tap("grate", [say("The drain grate, wedged up. Water moving far below.")]),
 tap("wren16", FRAG, when="!frag8"),
 tap("wren16", [say("WAKE UP ELIAS IT IS ONLY A LOOP.")]),
 tap("cellar_door", [{"set": "left16"}, {"take": "candle"}, {"complete_room": [108, "THE EIGHTH SEAL", "You climb the stair, and climb, and wake at your desk with your cheek on the blotter and a dark stone in your fist. The clock is going forwards again."]}], when="stone8_taken"),
 tap("cellar_door", [say("A door at the foot of the stairs, with three dials and a handle.")]),
]
steps = [
 step("count", ["any", "loop>0", "seen1"], ["The cellar starts over every twelve things you do. Look around before it does.", "Read the chalk on the bottle in the wine rack (north wall)."], [{"set": "seen1"}], "The first is three."),
 step("loop1", ["any", "seen2", "loop>1"], ["Each time round, something different shows. Undo the cellar on purpose: do twelve things.", "On the second time round, open the coal chute (east wall) and read inside it."], [{"set": "seen2"}], "The second is one."),
 step("loop2", ["any", "seen3", "loop>2"], ["The third time round, look low.", "Prise up the drain grate on the west wall and read under it."], [{"set": "seen3"}], "The third is two."),
 step("frag", "frag8", ["Something is written on the cellar wall that only dream sight shows.", "Look at the east wall with the Lens on."], FRAG, "Fragment VIII."),
 step("door", "door_open", ["The fourth time round there's a door. You have twelve moves before it's gone again.", "Set the door's dials to 3, 1, 2 (seven moves with the handle) and turn the handle."],
      [{"set": "loop", "value": 3}, {"set": "door_open"}], "The door opens."),
 step("stone", "stone8_taken", ["The stone is on the bottom step.", "Take the stone."], [{"give": "seal_stone8"}, {"set": "stone8_taken"}], "The eighth seal."),
 step("up", "left16", ["The stair goes up.", "Go through the door."], [{"set": "left16"}, {"complete_room": [108, "THE EIGHTH SEAL", "You wake."]}], "Awake."),
]
walk = [["shot", "start"], ["tap", "label_1"], ["repeat", 11, ["tap", "wine_rack"]], ["expect", "loop=1"], ["shot", "loop1"],
 ["tap", "coal_chute"], ["tap", "label_2"], ["lens", True], ["tap", "wren16"], ["lens", False], ["expect", "frag8"], ["repeat", 9, ["tap", "coal_chute"]], ["expect", "loop=2"],
 ["tap", "grate"], ["tap", "label_3"], ["repeat", 10, ["tap", "grate"]], ["expect", "loop=3"], ["shot", "door"],
 ["repeat", 3, ["tap", "cdl0"]], ["tap", "cdl1"], ["repeat", 2, ["tap", "cdl2"]], ["tap", "handle16"], ["wait", 1.0], ["expect", "door_open"], ["shot", "open"],
 ["tap", "stone8"], ["expect", "stone8_taken"], ["tap", "cellar_door"], ["wait", 2.0]]
room = {"title": "The Cellar", "walls": "r16_wall_", "floor": "r16_floor", "ceiling": "r16_ceiling", "intro": "You have been here before.",
        "on_enter": [{"set": "loop", "value": 0}, journal("cellar", "The cellar", "Under the dream study, a cellar my house does not have. Wine racks, a coal chute, a drain. I have the strangest feeling I have counted these bricks before.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room16_cellar.json", room)
print("room16 ok")

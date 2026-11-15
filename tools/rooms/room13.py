from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
NOTE = journal("violist", "The violist's notebook", "The notebook on the bed, in a cramped French hand, the English underneath in pencil (Wren's):\n\n\"I play it every night so that the window stays shut. D, A, E, G, A. If I stop, it opens.\"\n\n\"The case: tune its wires to the fork, then the fork less two, then the fork and one more.\"\n\n\"I have strung her my own way. The case remembers how.\"")
SX = [-0.75, -0.25, 0.25, 0.75]
objs = [
 sprite("n", "gwin", [0, 11], [5, 6], "gwin_street"),
 {"type": "furniture", "wall": "n", "id": "gdesk", "pos": [0, 0], "size": [6, 4, 2], "faces": {"front": "gdesk_front", "top": "roof_top_96x32", "default": "roof_side_32x64"}, "zoom": False},
 sprite("n", "fork", [2, 5.5], [1, 3], "fork", depth=1.3),
 sprite("n", "fork_lens", [2, 5.5], [1, 3], "fork_lens", depth=1.35, lens=2),
 sprite("e", "viol", [0, 4.5], [4, 9], "viol", depth=0.3),
] + [sprite("e", "vs%d" % k, [SX[k], 6.6], [0.5, 6], "vstring_%d" % k, depth=0.35) for k in range(4)] + [
 sprite("s", "gdoor", [4, 4.5], [4, 9], "gdoor"),
 sprite("s", "hatch", [-3, 5], [3, 3], "dumb_hatch"),
 sprite("w", "gbed", [0, 1.5], [7, 3], "gbed"),
 sprite("w", "notebook", [-2.25, 3.3], [2.5, 1.75], "notebook", depth=0.4),
 {"type": "box", "name": "vcase", "wall": "w", "pos": [2.0, 3.6], "depth": 0.9, "scale": 0.4, "view": "front", "size": [8, 3, 3],
  "faces": {"front": "vcase_front", "back": "vcase_back", "left": "vcase_side", "right": "vcase_side", "top": "vcase_top", "bottom": "vcase_top"},
  "liner": "vcase_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "vcase",
  "parts": [part("front", [-2.5 + i * 1.5, 0], [1, 2], "vpeg_0", "peg%d" % i, depth=0.04) for i in range(3)] + [part("front", [2.75, 0], [1, 1], "vcase_clasp", "vclasp", depth=0.04)],
  "inner_sprites": [{"id": "bow_part", "tex": "bow_inside", "size": [1, 7], "pos": [0, -1.2, 0], "rot": [-90, 90, 0], "face": "top"}]},
 sprite("d", "rosin_floor", [4.5, 11], [1.5, 1], "rosin_floor"),
]
puzzles = [
 {"kind": "cycler", "part": "peg%d" % i, "flag": "peg%d" % i, "count": 7, "start": st, "spin": False, "sfx": "tick",
  "textures": ["vpeg_%d" % k for k in range(7)], "lock": "case_open"} for i, st in enumerate((0, 6, 2))
] + [
 {"kind": "combo", "flags": ["peg0", "peg1", "peg2"], "code": [4, 2, 5], "commit": "vclasp", "lock": "case_open",
  "fail": [{"sfx": "thunk"}, say("The wires buzz against each other. The clasp stays shut.")],
  "do": [{"set": "case_open"}, {"sfx": "unlock"}, {"face": "top"}, say("The three wires ring true together, and the clasp lets go. Inside, on violet velvet: the bow.")]},
 {"kind": "pickup", "part": "bow_part", "item": "bow", "flag": "bow_taken", "show_if": "case_open", "then": [say("The bow. Its hair is dry as straw.")]},
 {"kind": "sequence", "parts": {"vs%d" % k: str(k) for k in range(4)}, "tex": {"vs%d" % k: "vstring_%d" % k for k in range(4)}, "pulled_suffix": "_hum",
  "order": "21031", "flag": "tune", "silent": True, "repeat": True, "lock": ["any", "!viol_ready", "played"],
  "do": [{"set": "played"}, {"sfx": "wind"}, {"set": "win", "value": "void"}, {"look": "n"}, {"shake": True},
         say("The fifth note and the window bursts open on its own. There is no street outside. There is nothing outside, only a dark full of moving lights, and it is listening. Shut it.", 6)],
  "fail": [{"sfx": "creak"}, say("Wrong. The notes go sour, and something outside the window shifts.")]},
]
bindings = [
 bind("gwin", "win=void", {"texture": "gwin_void"}),
 bind("gwin", "win=shut", {"texture": "gwin_shut"}),
 tex("hatch", "hatch_open", "dumb_hatch_open", "dumb_hatch"),
 vis("rosin_floor", "!rosin_taken"),
 bind("box:vcase", "case_open", {"tappable": False}, {"tappable": True}),
 bind("hinge:vcase.top", "case_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
]
interactions = [tap("vs%d" % k, [{"sfx": "tone_%d" % [2, 4, 0, 6][k]}], when="viol_ready", handled=False) for k in range(4)] + [
 tap("vs%d" % k, [{"sfx": "tick"}, say("A dull pluck. It wants a bow.")], when="!viol_ready") for k in range(4)] + [
 uses("rosined_bow", ["viol", "vs0", "vs1", "vs2", "vs3"], [{"take": "rosined_bow"}, {"set": "viol_ready"}, {"sfx": "tone_0"}, say("You set the bow to the strings. The viol speaks, low and too loud for the room.")]),
 uses("bow", ["viol", "vs0", "vs1", "vs2", "vs3"], [{"sfx": "tick"}, say("The bow slides over the strings and makes no sound at all. The hair is too dry.")]),
 tap("viol", [say("A viol on a stand. Four strings. The violist strung it his own way.")]),
 tap("gwin", [say("Rooftops. Somewhere down there is a street you couldn't find on any map, and you are above it.")], when="!win"),
 tap("gwin", [{"set": "win", "value": "shut"}, {"sfx": "thunk"}, {"wait": 0.8}, {"set": "hatch_open"}, {"sfx": "creak"},
              say("You throw the shutters closed against it and hold them. The listening stops. Behind you, the little hatch in the south wall drops open.", 5)], when="win=void"),
 tap("gwin", [say("Shuttered. You are not opening it again.")], when="win=shut"),
 tap("gwin", [say("Rooftops.")]),
 tap("hatch", [say("A dumbwaiter hatch, shut.")], when="!hatch_open"),
 tap("hatch", [{"set": "cock_taken"}, {"give": "vane_cock"}, {"sfx": "pickup"}, say("In the dumbwaiter, wrapped in a page of music: an iron weathercock, wrenched off its spindle.")], when=["hatch_open", "!cock_taken"]),
 tap("hatch", [say("The dumbwaiter is empty.")]),
 tap("rosin_floor", [{"set": "rosin_taken"}, {"give": "rosin"}, {"sfx": "pickup"}, say("A cake of rosin, dropped between the boards.")]),
 tap("notebook", [NOTE, {"set": "nb_read"}, say("The violist's notebook. It's in your journal.")]),
 tap("fork", [{"sfx": "tone_4"}, say("A tuning fork. It rings one clean note that goes on longer than it should.")]),
 tap("fork_lens", [{"sfx": "tone_4"}, say("Through the Lens, the fork's note hangs in the air as a wave: five humps.")]),
 tap("gbed", [say("A narrow bed. The violist didn't sleep in it much.")]),
 tap("gdesk", [say("A desk covered in candle wax and rosin dust.")]),
 tap("gdoor", [say("The door down to the street. Locked, and the key is nowhere.")], when="!win=shut"),
 tap("gdoor", [{"set": "left13"}, {"complete_room": [14, "THE STREET", "The door opens on its own now. You go down a stair that is longer than the house, and out onto a street that turns the wrong number of times."]}], when="win=shut"),
]
steps = [
 step("nb", "nb_read", ["The violist left notes.", "Read the notebook on the bed (west wall)."], [NOTE, {"set": "nb_read"}], "The notebook is in your journal."),
 step("case", "case_open", ["The notebook says how to tune the case's wires. Something on the desk gives the note.",
      "Look at the tuning fork with the Lens: five humps. The case's pegs show humps too. Set them to 5, 3 and 6 humps and press the clasp."], [{"set": "case_open"}], "The case opens."),
 step("bow", "bow_taken", ["The case held a bow.", "Take the bow from the open case."], [{"give": "bow"}, {"set": "bow_taken"}], "The bow."),
 step("rosin", ["any", "item:rosined_bow", "viol_ready"], ["The bow is too dry to sound. Something on the floor helps.",
      "Pick up the rosin from the floor, then rub the bow on it in your tray."], [{"take": "bow"}, {"give": "rosined_bow"}, {"set": "rosin_taken"}], "The bow is rosined."),
 step("ready", "viol_ready", ["The viol needs a bow.", "Use the rosined bow on the viol."], [{"take": "rosined_bow"}, {"set": "viol_ready"}], "The viol is ready."),
 step("play", "played", ["The notebook gives the tune in letters. The case's lid says how the strings are laid out.",
      "The strings, left to right, are E A D G. Play D, A, E, G, A: third, second, first, fourth, second."], [{"set": "played"}, {"set": "win", "value": "void"}], "The window opens."),
 step("shut", "win=shut", ["Something is listening at the window.", "Touch the window to shut it."], [{"set": "win", "value": "shut"}, {"set": "hatch_open"}], "Shut."),
 step("cock", "cock_taken", ["A hatch opened in the south wall.", "Take what's in the dumbwaiter."], [{"set": "cock_taken"}, {"give": "vane_cock"}], "A weathercock."),
 step("go", "left13", ["The door will open now.", "Go out of the door in the south wall."], [{"set": "left13"}, {"complete_room": [14, "THE STREET", "You go down."]}], "Down to the street."),
]
walk = [["shot", "start"], ["tap", "notebook"], ["tap", "gwin"], ["lens", True], ["tap", "fork_lens"], ["lens", False], ["tap", "vcase"], ["shot", "case"],
 ["repeat", 4, ["tap", "peg0"]], ["repeat", 3, ["tap", "peg1"]], ["repeat", 3, ["tap", "peg2"]], ["tap", "vclasp"], ["wait", 1.5], ["expect", "case_open"], ["tap", "bow_part"], ["back"],
 ["tap", "rosin_floor"], ["combine", "bow", "rosin"], ["use", "rosined_bow", "viol"], ["expect", "viol_ready"]] + [["tap", "vs%s" % c] for c in "21031"] + [
 ["wait", 1.5], ["expect", "played"], ["shot", "void"], ["tap", "gwin"], ["wait", 1.5], ["tap", "hatch"], ["expect", "cock_taken"], ["tap", "gdoor"], ["wait", 2.0]]
room = {"title": "The Garret", "walls": "r13_wall_", "floor": "r13_floor", "ceiling": "r13_ceiling", "intro": "Someone has just stopped playing.",
        "on_enter": [journal("garret", "The garret", "At the top of a street I could not find until I stopped looking for it: a garret under the roof, a viol on its stand, a bed, a window with no curtain. The violist is gone. His bow is not on the stand.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room13_garret.json", room)
print("room13 ok")

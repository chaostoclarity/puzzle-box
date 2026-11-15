from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
ORDER = "52714"
FX = [-1.25, -0.8125, -0.375, 0, 0.375, 0.8125, 1.25]
FRAG = [{"set": "frag6"}, {"fragment": True}, {"sfx": "reveal"},
        journal("frag6", "Fragment VI", "Through the Lens, on the keeper's wrappings, written over and over in my own hand: E.T. HERE. And under it, Wren's: \"I saw this too, in my dream of the hall, and the initials were mine. They write whoever comes. I think they are telling us where we will be kept.\""),
        say("Through the Lens, on the wrappings, in your own handwriting: E.T. HERE.", 5)]
objs = [
 sprite("n", "mural_frame", [0, 11.5], [14.5, 5], "mural_frame"),
] + [sprite("n", "m%d" % i, [(i - 2) * 2.85, 11.5], [2.75, 4], "mural_0", depth=0.06) for i in range(5)] + [
 sprite("n", "mural_stone", [6, 8], [1.25, 1.25], "mural_stone", depth=0.06),
 sprite("n", "mural_hand", [0, 6], [2.75, 4], "mural_hand", depth=0.06),
 {"type": "furniture", "wall": "e", "id": "coffin", "pos": [0, 0], "size": [4, 8, 2], "faces": {"front": "coffin_front", "top": "crypt_top_64x32", "default": "crypt_side_32x128"},
  "zoom": {"k": 3}, "parts": [part("front", [FX[i], 0.75], [0.6, 0.6], "finger", "f%d" % (i + 1), depth=0.04) for i in range(7)] +
                         [part("front", [0, -2.75], [2, 0.75], "clear", "plate", depth=0.04)]},
 sprite("e", "coffin_dark", [0, 4], [4, 8], "coffin_inside", depth=2.05),
 sprite("e", "mummy", [0, 4.5], [3, 7], "mummy", depth=2.1),
 sprite("e", "mummy_lens", [0, 4.5], [3, 7], "mummy_lens", depth=2.15, lens=2),
 {"type": "box", "name": "reli", "wall": "e", "pos": [0, 3.2], "depth": 2.6, "scale": 0.35, "view": "front", "size": 6,
  "faces": {"front": "reli_front", "back": "reli_back", "left": "reli_side", "right": "reli_side", "top": "reli_top", "bottom": "reli_top"},
  "liner": "reli_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "reli",
  "parts": [part("front", [0, 0.2], [4.5, 4.5], "rring_o", "rring_o", tappable=False), part("front", [0, 0.2], [3, 3], "rring_i", "rring_i", depth=0.04, tappable=False),
            part("front", [0, 0.2], [4.5, 4.5], "clear", "rrings", depth=0.065), part("front", [0, 2.6], [1, 0.5], "reli_mark", "reli_mark", depth=0.05),
            part("front", [2.3, -2.3], [0.75, 0.75], "reli_pin", "reli_pin", depth=0.04)],
  "inner_sprites": [{"id": "stone_part", "tex": "item_seal_stone6", "size": [1.5, 1.5], "pos": [0, -2.2, 0], "rot": [-90, 0, 0], "face": "top"}]},
 sprite("s", "stair", [0, 5], [5, 10], "stair"),
 sprite("s", "stair_gate", [0, 5], [5, 10], "stair_gate", depth=0.08),
 sprite("w", "idol_w", [-4, 3], [3, 4], "idol"),
 sprite("w", "drift_w", [0, 1], [15, 2], "sand_drift"),
]
puzzles = [
 {"kind": "swap", "parts": ["m%d" % i for i in range(5)], "flag": "mural", "start": "31402", "tex": "mural_%s", "lock": "mural_done"},
 {"kind": "sequence", "parts": {"f%d" % (i + 1): str(i + 1) for i in range(7)}, "tex": {"f%d" % (i + 1): "finger" for i in range(7)}, "order": ORDER, "flag": "gesture", "silent": True, "lock": "coffin_open",
  "do": [{"set": "coffin_open"}, {"sfx": "creak"}, {"wait": 0.6}, {"sfx": "reveal"}, say("The palm takes the gesture. The lid of the coffin swings away on a keeper, standing, wrapped, holding a bronze box against its chest.", 5)],
  "fail": [{"sfx": "thunk"}, say("The fingers spring back up. That wasn't the gesture.")]},
 {"kind": "radial", "part": "rrings", "rotate": -45, "count": 8, "lock": "reli_open", "rings": [["rring_i", 1.5], ["rring_o", 2.25]]},
 {"kind": "combo", "flags": ["rring_i", "rring_o"], "code": [2, 6], "commit": "reli_pin", "lock": "reli_open",
  "fail": [{"sfx": "thunk"}, say("The red pin won't go in.")],
  "do": [{"set": "reli_open"}, {"sfx": "unlock"}, {"face": "top"}, say("The pin slides home and the lid lifts. Inside: a green-black stone, warm as skin.")]},
 {"kind": "pickup", "part": "stone_part", "item": "seal_stone6", "flag": "stone6_taken", "show_if": "reli_open", "then": [say("The sixth seal. It is warm. It should not be warm.")]},
]
bindings = [
 vis("mural_hand", "mural_done"),
 vis("coffin_dark", "coffin_open"),
 vis("mummy", "coffin_open"), vis("mummy_lens", "coffin_open"),
 bind("box:reli", "coffin_open", {"visible": True}, {"visible": False}),
 bind("box:reli", "reli_open", {"tappable": False}),
 bind("hinge:reli.top", "reli_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 vis("stair_gate", "!stone6_taken"),
] + [vis("f%d" % (i + 1), "!coffin_open") for i in range(7)] + [vis("plate", "!coffin_open")]
interactions = [
 tap("mural_stone", [{"set": "mural_done"}, {"sfx": "slide"}, {"wait": 0.5}, {"sfx": "reveal"}, say("The story runs true now: the city, and the sand coming, and the city gone. A slab under the strip slides down on another picture: a seven-fingered hand.", 5)], when=["mural=01234", "!mural_done"]),
 tap("mural_stone", [{"sfx": "thunk"}, say("The stone doesn't move. The story is told out of order.")], when="!mural_done"),
 tap("mural_stone", [say("Pressed in.")]),
 tap("mural_hand", [say("A seven-fingered hand. Five fingers have marks over them in the keepers' dots and bars.")]),
 tap("mural_frame", [say("A painted strip of five panels. They lift out of their frame and change places if you touch two in turn.")]),
 tap("plate", [say("A bronze plate in dots and bars: two numbers. Under the first, a small circle; under the second, a large one. The keeper's birth flood and its sealing flood.", 6)]),
 tap("mummy", FRAG, when=["lens", "!frag6"]),
 tap("mummy_lens", FRAG, when="!frag6"),
 tap("mummy", [say("A keeper, wrapped, standing. Its face is a long, flat thing. Seven fingers on each hand, folded round the box.")]),
 tap("mummy_lens", [say("E.T. HERE.")]),
 tap("coffin_dark", [say("The open coffin. It smells of cinnamon and something under the cinnamon.")]),
 tap("reli_mark", [say("A mark at the top of the rings: whatever stands here is the setting.")]),
 tap("stair_gate", [say("A bronze gate across a stair going up. It is locked by nothing you can see.")]),
 tap("stair", [{"set": "left12"}, {"take": "weight1"}, {"take": "weight3"}, {"take": "weight9"}, {"complete_room": [106, "THE SIXTH SEAL", "The gate opens as you come near it. The stair goes up a long way, through sand, into a night with the wrong stars."]}], when="stone6_taken"),
 tap("idol_w", [say("Another keeper idol, its face worn away by a thousand years of kissing.")]),
 tap("drift_w", [say("Sand, heaped against the wall as if blown by a wind from inside.")]),
]
steps = [
 step("mural", "mural_done", ["The mural tells a story, but its panels are out of order.", "Order the panels by the sand: no sand on the left, buried on the right. Then press the round stone."],
      [{"set": "mural", "value": "01234"}, {"set": "mural_done"}], "The mural opens."),
 step("gesture", "coffin_open", ["The hand in the mural marks five fingers in the keepers' numbers. The coffin has a hand lock with seven fingers.",
      "Press the coffin's fingers in the order the mural numbers them: fifth, second, seventh, first, fourth (counting from the left)."], [{"set": "coffin_open"}], "The coffin opens."),
 step("frag", "frag6", ["The keeper's wrappings have writing you can't see.", "Look at the keeper with the Lens on."], FRAG, "Fragment VI."),
 step("reli", "reli_open", ["The coffin plate gives two numbers in dots and bars. Remember the weights: a dot is one, a bar is three.",
      "Turn the inner ring to 3 (one bar) and the outer to 7 (two bars and a dot) under the mark, then push the red pin."], [{"set": "rring_i", "value": 2}, {"set": "rring_o", "value": 6}, {"set": "reli_open"}], "The box opens."),
 step("stone", "stone6_taken", ["The bronze box held the seal.", "Take the stone."], [{"give": "seal_stone6"}, {"set": "stone6_taken"}], "The sixth seal."),
 step("up", "left12", ["The gate on the stair is open.", "Climb the stair in the south wall."], [{"set": "left12"}, {"complete_room": [106, "THE SIXTH SEAL", "You climb."]}], "Up."),
]
# swaps from 31402 to 01234: (m0,m3) -> 01432? compute in python below
def swaps(start, goal="01234"):
    s = list(start); out = []
    for i in range(5):
        if s[i] != goal[i]:
            j = s.index(goal[i]); out += [["tap", "m%d" % i], ["tap", "m%d" % j]]; s[i], s[j] = s[j], s[i]
    return out
walk = [["shot", "start"], ["tap", "mural_stone"]] + swaps("31402") + [["shot", "mural"], ["tap", "mural_stone"], ["expect", "mural_done"],
 ["tap", "coffin"], ["tap", "plate"]] + [["tap", "f%s" % c] for c in ORDER] + [["wait", 1.5], ["expect", "coffin_open"], ["back"],
 ["lens", True], ["tap", "mummy_lens"], ["expect", "frag6"], ["lens", False], ["tap", "reli"], ["shot", "reli"],
 ["repeat", 2, ["tapat", "rrings", [0, 0.6]]], ["repeat", 6, ["tapat", "rrings", [0, 1.9]]], ["shot", "reli_set"], ["tap", "reli_pin"], ["wait", 1.5], ["expect", "reli_open"],
 ["tap", "stone_part"], ["expect", "stone6_taken"], ["back"], ["tap", "stair"], ["wait", 2.0]]
room = {"title": "The Hall of Keepers", "walls": "r12_wall_", "floor": "r12_floor", "ceiling": "r12_ceiling", "intro": "Coffins, standing, all the way up.",
        "on_enter": [journal("hall", "The hall of keepers", "A hall of coffins standing on end, cut for bodies longer and lower than a man's. A painted strip above the north wall tells a story, out of order. One coffin on the east wall has a hand set into its lid, with seven fingers.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room12_coffins.json", room)
print("room12 ok")

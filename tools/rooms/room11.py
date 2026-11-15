from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
TILE_START = [1, 3, 2, 1]
TC = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
objs = [
 sprite("n", "low_door", [0, 2], [5, 4], "low_door"),
 sprite("n", "lintel", [0, 6], [6, 3], "lintel"),
 sprite("n", "lintel_lens", [0, 6], [6, 3], "lintel_lens", depth=0.06, lens=2),
 sprite("n", "gpanel", [5, 4.5], [5, 5], "gpanel"),
] + [sprite("n", "gtile_%d" % q, [5 + TC[q][0], 4.5 + TC[q][1]], [2, 2], "gtile_%d_%d" % (q, TILE_START[q]), depth=0.06) for q in range(4)] + [
 sprite("n", "gpanel_key", [5, 1.2], [1, 1], "gpanel_key", depth=0.06),
 sprite("e", "plinth", [0, 1.5], [3, 3], "plinth"),
 sprite("e", "hglass", [0, 6], [3, 6], "hglass_0_0", depth=0.3),
 sprite("s", "niche", [0, 5], [4, 4], "niche"),
 sprite("w", "altar", [0, 1.5], [7, 3], "altar_front"),
 sprite("w", "altar_glyph", [0, 1.6], [1, 1], "altar_glyph", depth=0.06),
 sprite("w", "beam", [0, 6], [8, 4], "beam_l"),
 sprite("w", "pan_l", [-3.5, 4.5], [3, 1.5], "pan", depth=0.06),
 sprite("w", "pan_r", [3.5, 4.5], [3, 1.5], "pan", depth=0.06),
 sprite("w", "idol", [-4.25, 5.6], [1.5, 2], "idol", depth=0.08),
]
for w, (lx, rx) in ((1, (-3.0, 2.6)), (3, (-2.4, 3.5)), (9, (-3.6, 4.4))):
    objs.append(sprite("w", "wl_%d" % w, [lx, 5.4], [1.5, 1.5], "wsprite_%d" % w, depth=0.09))
    objs.append(sprite("w", "wr_%d" % w, [rx, 5.4], [1.5, 1.5], "wsprite_%d" % w, depth=0.09))
objs += [sprite("d", "drift", [0, 1.5], [15, 2], "sand_drift")]
puzzles = [
 {"kind": "tick", "flag": "sand", "every": 1, "step": -1, "min": 0, "while": "!facing=e"},
] + [{"kind": "cycler", "part": "gtile_%d" % q, "flag": "gt%d" % q, "count": 4, "start": TILE_START[q], "spin": False, "sfx": "stone",
      "textures": ["gtile_%d_%d" % (q, r) for r in range(4)], "lock": "tiles_done"} for q in range(4)] + [
 {"kind": "combo", "flags": ["gt0", "gt1", "gt2", "gt3"], "code": [0, 0, 0, 0], "commit": "gpanel_key", "lock": "tiles_done",
  "fail": [{"sfx": "thunk"}, say("The bronze stud won't press in.")],
  "do": [{"set": "tiles_done"}, {"sfx": "unlock"}, {"give": "weight1"}, say("The stud sinks. A drawer no wider than a finger slides out of the panel: a small bronze weight with one dot on it.", 5)]},
]
bindings = [
 bind("hglass", "hg_taken", {"texture": "hglass_taken"}, {"texture": "hglass_{gu:1}_{sand:5}"}),
 tex("niche", "niche_open", "niche_open", "niche"),
 tex("low_door", "door_open", "low_door_open", "low_door"),
 bind("beam", "wl>wr", {"texture": "beam_l"}),
 bind("beam", "wl<wr", {"texture": "beam_r"}),
 bind("beam", "wl==wr", {"texture": "beam_level"}),
]
for w in (1, 3, 9):
    bindings.append(vis("wl_%d" % w, "w%d_at=l" % w)); bindings.append(vis("wr_%d" % w, "w%d_at=r" % w))
put = []
for w in (1, 3, 9):
    put += [uses("weight%d" % w, ["pan_l", "idol", "wl_1", "wl_3", "wl_9"], [{"take": "weight%d" % w}, {"set": "w%d_at" % w, "value": "l"}, {"add": "wl", "value": w}, {"sfx": "thunk"}]),
            uses("weight%d" % w, ["pan_r", "wr_1", "wr_3", "wr_9"], [{"take": "weight%d" % w}, {"set": "w%d_at" % w, "value": "r"}, {"add": "wr", "value": w}, {"sfx": "thunk"}])]
back = []
for w in (1, 3, 9):
    for side in "lr":
        back.append(taps(["w%s_%d" % (side, w)], [{"give": "weight%d" % w}, {"set": "w%d_at" % w, "value": ""}, {"add": "w" + side, "value": -w}, {"sfx": "click"}], when=["w%d_at=%s" % (w, side), "!door_open"]))
flips = []
for u in (0, 1):
    for s_ in range(6):
        flips.append(tap("hglass", [{"set": "gu", "value": 1 - u}, {"set": "sand", "value": 5 - s_}, {"set": "sand#", "value": 0}, {"sfx": "slide"},
                                    say("You turn the glass over. The sand hangs in the neck and does not fall. Not while you watch it.")], when=["gu=%d" % u, "sand=%d" % s_]))
interactions = put + back + [
 tap("hglass", [say("The glass is empty now. Only sand.")], when="hg_taken"),
 tap("hglass", [{"set": "hg_taken"}, {"give": "weight3"}, {"sfx": "unlock"}, say("The top bulb is empty but for the weight that couldn't pass the neck. You unscrew the cap and take it: one bar.")], when=["gu=1", "sand=0", "!hg_taken"]),
] + flips + [
 tap("niche", [{"ask": ["The keepers", "A voice that is not a voice, from the mouth in the wall: the keepers will hold something for you, if you give them a place to keep it.\n\nGive up one slot of your tray? It will not come back.", ["Give a slot", "Not yet"]]},
               {"add": "slots_given"}, {"set": "niche_open"}, {"sfx": "creak"}, say("Something cold settles in your tray where a slot was. The stone teeth draw back.")], when="!niche_open"),
 tap("niche", [{"set": "w9_taken"}, {"give": "weight9"}, {"sfx": "pickup"}, say("In the mouth: a heavy bronze weight with three bars on it.")], when=["niche_open", "!w9_taken"]),
 tap("niche", [say("An empty stone mouth.")]),
 tap("altar_glyph", [{"set": "door_open"}, {"sfx": "horn"}, {"wait": 1.0}, {"sfx": "creak"}, {"shake": True}, say("You press the red stone. The scale locks level, and behind you the low door rolls aside.", 5)], when=["wl==wr", "!door_open"]),
 tap("altar_glyph", [{"sfx": "thunk"}, say("The red stone won't press while the scale hangs crooked.")], when="!door_open"),
 tap("altar_glyph", [say("Pressed in for good.")]),
 tap("idol", [say("A keeper idol, fixed to the left pan. You can't lift it. It is heavier than it looks, and it looks heavy.")]),
 tap("pan_l", [say("The left pan, with the idol fixed to it. Put weights on either pan.")]),
 tap("pan_r", [say("The right pan. Put weights on either pan.")]),
 tap("beam", [say("A bronze balance. The pointer shows which pan is heavier.")]),
 tap("altar", [say("An altar under the scale, cut low, for things that walked on all fours.")]),
 tap("plinth", [say("A plinth with a carving of an eye, closed.")]),
 tap("lintel", [say("A carved glyph over the door, worn almost away by sand.")]),
 tap("lintel_lens", [say("Through the Lens, the glyph as it was cut, whole.")]),
 tap("gpanel", [say("A panel of four turning tiles, each with a piece of a glyph, and a bronze stud.")]),
 tap("drift", [say("Sand that came in through no door you can see.")]),
 tap("low_door", [say("A stone door cut for a crawling thing, rolled shut.")], when="!door_open"),
 tap("low_door", [{"set": "left11"}, {"complete_room": [12, "THE HALL OF KEEPERS", "You crawl through. The ceiling goes up, and up, and the walls are lined with the coffins of things that were never men."]}], when="door_open"),
]
steps = [
 step("glyph", "tiles_done", ["The glyph above the door is the picture the four tiles make.", "Look at the glyph above the door with the Lens (Through), then turn each tile to match it and press the bronze stud."],
      [{"set": "tiles_done"}, {"give": "weight1"}], "A small weight drops out."),
 step("offer", "niche_open", ["The mouth in the south wall wants something.", "Touch the stone mouth and give the keepers a tray slot."], [{"add": "slots_given"}, {"set": "niche_open"}], "The mouth opens."),
 step("w9", "w9_taken", ["The mouth held something.", "Take the heavy weight from the stone mouth."], [{"set": "w9_taken"}, {"give": "weight9"}], "Three bars."),
 step("flip", "gu=1", ["Something is buried in the bottom of the hourglass.", "Turn the hourglass over."], [{"set": "gu", "value": 1}, {"set": "sand", "value": 5}], "The glass turns."),
 step("sand", ["any", "hg_taken", "sand=0"], ["The sand won't fall while you watch it.", "Turn away from the hourglass and do five other things (touch anything), then come back."], [{"set": "sand", "value": 0}], "The sand has run."),
 step("w3", "hg_taken", ["The weight is in the empty top bulb.", "Touch the hourglass to take the weight."], [{"set": "hg_taken"}, {"give": "weight3"}], "One bar."),
 step("balance", "door_open", ["Weights can go on either pan. The idol is heavy: more than six of the small ones, less than nine.", "Put the 3 on the idol's pan, the 9 and the 1 on the other pan, then press the red stone on the altar."],
      [{"set": "door_open"}], "The door rolls aside."),
 step("go", "left11", ["The low door is open.", "Crawl through the low door in the north wall."], [{"set": "left11"}, {"complete_room": [12, "THE HALL OF KEEPERS", "You crawl through."]}], "Through."),
]
walk = [["shot", "start"], ["lens", True], ["tap", "lintel_lens"], ["lens", False], ["shot", "panel"],
 ["repeat", 3, ["tap", "gtile_0"]], ["tap", "gtile_1"], ["repeat", 2, ["tap", "gtile_2"]], ["repeat", 3, ["tap", "gtile_3"]], ["tap", "gpanel_key"], ["expect", "tiles_done"],
 ["tap", "hglass"], ["shot", "flipped"], ["tap", "niche"], ["tap", "niche"], ["expect", "w9_taken"], ["tap", "altar"], ["tap", "idol"], ["tap", "beam"], ["tap", "drift"],
 ["tap", "hglass"], ["shot", "glass_empty"], ["expect", "hg_taken"],
 ["use", "weight9", "pan_r"], ["shot", "tilt_r"], ["use", "weight1", "pan_r"], ["use", "weight3", "pan_l"], ["shot", "level"], ["tap", "altar_glyph"], ["wait", 1.5], ["expect", "door_open"], ["tap", "low_door"], ["wait", 2.0]]
room = {"title": "The Antechamber", "walls": "r11_wall_", "floor": "r11_floor", "ceiling": "r11_ceiling", "intro": "You have to stoop. They walked lower than men.",
        "on_enter": [{"set": "gu", "value": 0}, {"set": "sand", "value": 0}, {"set": "wl", "value": 7}, {"set": "wr", "value": 0},
                     journal("ante", "The city under the sand", "The map was right. Under the dunes, a city of low doors and long halls, cut for things that crawled. The antechamber's door rolled shut behind me. On the west wall a bronze scale, and an idol on one pan that no one has ever lifted.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room11_ante.json", room)
print("room11 ok")

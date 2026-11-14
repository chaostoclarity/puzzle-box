from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
LOG = journal("survey_log", "The survey log", "The log of Hut 4, Kingsport Antarctic Survey, 1926. The last entries:\n\n\"Specimen case locked by Halvorsen to the three survey stakes, as seen from the window: red, then blue, then green. If you can't see them, warm the hut.\"\n\n\"Coal finished. Burned the charts. Burned the novels. Burned the log of the first winter.\"\n\n\"Halvorsen went down the hatch with the specimen tin and came back up without it, and then went down again for good. The hatch froze over after him.\"\n\n\"The stove only wants paper now. It asks for it.\"")
HEAT_WORDS = {0: "Bitter cold.", 1: "The frost on the window is melting.", 2: "The hut is almost warm. Something on the bench creaks as it thaws.", 3: "Hot enough to melt the ice in the floor."}
def stove_burn(h):
    return tap("stove", [{"ask": ["The stove", "The cold will kill you before morning, and the only paper in the hut is your journal.\n\nFeed the stove the newest page?", ["Burn a page", "Not yet"]]},
                         {"burn": True}, {"set": "heat", "value": h + 1}, {"sfx": "flame"}, {"set": "heat#", "value": 0}, say(HEAT_WORDS[h + 1], 4)], when=["blank_burned", "heat=%d" % h])
objs = [
 sprite("n", "stove", [-3, 3], [4, 6], "hstove_0", depth=1.0),
 sprite("n", "therm", [1.5, 8], [0.75, 3], "htherm_0"),
 {"type": "furniture", "wall": "e", "id": "hdesk", "pos": [-2.5, 0], "size": [7, 4, 2.5], "faces": {"front": "hdesk_front", "top": "hut_top_112x40", "default": "hut_side_40x64"}, "zoom": False},
 sprite("e", "survey_log", [-3.5, 4.75], [2.5, 1.5], "survey_log", depth=1.3),
 sprite("e", "hwin", [3, 10], [4, 4], "hwin_0"),
 sprite("s", "bunk", [-3, 2], [7, 3], "bunk"),
 sprite("s", "hut_door", [3.5, 4.5], [4.5, 9], "hut_door"),
 {"type": "furniture", "wall": "w", "id": "bench", "pos": [0, 0], "size": [6, 2, 2], "faces": {"front": "bench_front", "top": "hut_top_96x32", "default": "hut_side_32x32"}, "zoom": False},
 {"type": "box", "name": "spec", "wall": "w", "pos": [0, 2.9], "depth": 1.0, "scale": 0.45, "view": "front", "size": [6, 4, 4],
  "faces": {"front": "spec_front", "back": "spec_back", "left": "spec_side", "right": "spec_side", "top": "spec_top", "bottom": "spec_top"},
  "liner": "spec_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "spec",
  "parts": [part("front", [-1.5, -0.875], [1, 1], "cdial_r_0", "dial_r"), part("front", [0, -0.875], [1, 1], "cdial_b_0", "dial_b"),
            part("front", [1.5, -0.875], [1, 1], "cdial_g_0", "dial_g"), part("front", [2.4, 0.4], [1, 0.5], "spec_latch", "spec_latch", depth=0.04)],
  "inner_sprites": [{"id": "tin_part", "tex": "item_frozen_tin", "size": [1.5, 1.5], "pos": [0, -0.8, 0], "rot": [-90, 0, 0], "face": "top"}]},
 sprite("u", "hut_lamp", [0, 7.5], [2, 3], "hut_lamp"),
 sprite("d", "ice_hatch", [0, 4], [5, 5], "ice_hatch"),
]
puzzles = [
 {"kind": "tick", "flag": "heat", "every": 6, "step": -1, "min": 0, "say": "The stove dies down. The cold comes back in."},
] + [
 {"kind": "cycler", "part": "dial_" + c, "flag": "dial_" + c, "count": 10, "spin": False, "sfx": "tick", "textures": ["cdial_%s_%d" % (c, k) for k in range(10)], "lock": "case_open"} for c in "rbg"
] + [
 {"kind": "combo", "flags": ["dial_r", "dial_b", "dial_g"], "code": [3, 8, 1], "commit": "spec_latch", "lock": "case_open",
  "fail": [{"sfx": "thunk"}, say("The latch won't lift.")], "do": [{"set": "case_open"}, {"sfx": "unlock"}, {"face": "top"}, say("The latch lifts. Inside the case, packed in frost: a specimen tin, frozen solid.")]},
 {"kind": "pickup", "part": "tin_part", "item": "frozen_tin", "flag": "tin_taken", "show_if": "case_open", "then": [say("A specimen tin frozen into a block of ice.")]},
]
bindings = [
 bind("stove", None, {"texture": "hstove_{heat:3}"}),
 bind("therm", None, {"texture": "htherm_{heat:3}"}),
 bind("hwin", None, {"texture": "hwin_{heat:3}"}),
 bind("ice_hatch", "hatch_open", {"texture": "ice_hatch_open"}, {"texture": "ice_hatch"}),
 bind("ice_hatch", ["heat=3", "!hatch_open"], {"texture": "ice_hatch_thawed"}),
 bind("hinge:spec.top", "case_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("box:spec", "case_open", {"tappable": False}, {"tappable": True}),
]
interactions = [
 tap("stove", [{"ask": ["The stove", "The stove is cold. There is no coal, no wood, no paper in the hut but your journal. It wants a page; it seems to want a particular one, the blank one.", ["Burn the blank page", "Not yet"]]},
               {"burn": "blank"}, {"set": "blank_burned"}, {"set": "heat", "value": 1}, {"set": "heat#", "value": 0}, {"sfx": "flame"}, say("The blank page catches. For a little while, the hut is less cold.", 5)], when="!blank_burned"),
 stove_burn(0), stove_burn(1), stove_burn(2),
 tap("stove", [say("As hot as it gets. It will want more soon.")], when="heat=3"),
 uses("frozen_tin", ["stove"], [{"take": "frozen_tin"}, {"give": "thawed_tin"}, {"sfx": "water"}, say("You hold the tin to the stove until the ice runs off it. Hold it in your tray to open it.", 5)], when=["any", "heat=1", "heat=2", "heat=3"]),
 uses("frozen_tin", ["stove"], [say("The stove is cold. It won't thaw anything.")]),
 tap("survey_log", [{"set": "log_read"}, {"sfx": "paper"}, LOG, say("The survey log. It's in your journal. Read it now; the stove will ask for pages.", 5)]),
 tap("hwin", [say("Frost, thick as a blanket. You can't see out.")], when="heat=0"),
 tap("hwin", [say("Through the melting frost: three survey stakes in the snow, flagged red, blue and green. Too far to read.")], when="heat=1"),
 tap("hwin", [say("The glass is clear. Numbers are painted on the stakes: red 3, blue 8, green 1.", 5)]),
 tap("therm", [say("A thermometer. It reads the stove, not the weather.")]),
 tap("bunk", [say("A bunk with a frozen blanket. Someone slept here in their coat.")]),
 tap("hut_door", [say("Snowed shut from outside. Wind howls through the gaps.")]),
 tap("hut_lamp", [say("A lamp with no oil in it.")]),
 tap("bench", [say("A workbench, scored with knife marks.")]),
 tap("lift:spec", [{"shake": True}, say("Frozen to the bench. The hut needs to be warmer.")], when=["!case_free", ["any", "heat=0", "heat=1"]]),
 tap("lift:spec", [{"set": "case_free"}, say("The ice lets go of the bench.")], when="!case_free", handled=False),
 tap("ice_hatch", [say("A hatch in the floor, frozen solid under a foot of ice.")], when=["!hatch_open", "!heat=3"]),
 tap("ice_hatch", [{"set": "hatch_open"}, {"sfx": "crack"}, say("The ice over the hatch breaks up. You heave it open. A ladder goes down into blue light.")], when=["!hatch_open", "heat=3"]),
 tap("ice_hatch", [{"set": "left9"}, {"take": "frozen_tin"}, {"take": "thawed_tin"}, {"complete_room": [10, "THE SHAFT", "The ladder goes down a long way through blue ice. At the bottom, the cold has a sound to it, like a held note."]}], when="hatch_open"),
]
steps = [
 step("log", "log_read", ["The hut kept a log.", "Read the survey log on the desk (east wall)."], [{"set": "log_read"}, LOG], "The log is in your journal."),
 step("blank", "blank_burned", ["You'll freeze. The stove wants something.", "Touch the stove and feed it the blank page."], [{"burn": "blank"}, {"set": "blank_burned"}, {"set": "heat", "value": 1}], "The blank page burns."),
 step("warm", ["any", "case_free", "case_open"], ["The specimen case is frozen to the bench, and the window is frosted. Warm the hut.",
      "Burn another page so the hut warms to the second mark, then lift the specimen case from the bench before it cools."], [{"set": "heat", "value": 2}, {"set": "case_free"}], "The hut warms."),
 step("case", "case_open", ["The log says how the case is locked. The window shows the stakes when the hut is warm.",
      "The stakes read red 3, blue 8, green 1. Set the three dials on the specimen case and lift the latch."], [{"set": "dial_r", "value": 3}, {"set": "dial_b", "value": 8}, {"set": "dial_g", "value": 1}, {"set": "case_open"}], "The case opens."),
 step("tin", "tin_taken", ["The case held a frozen tin.", "Take the frozen tin from the specimen case."], [{"give": "frozen_tin"}, {"set": "tin_taken"}], "The tin is yours."),
 step("thaw", ["any", "item:thawed_tin", "item:bone_flute"], ["The tin is frozen solid.", "With the stove lit, use the frozen tin on the stove."], [{"take": "frozen_tin"}, {"give": "thawed_tin"}], "The tin thaws."),
 step("pry", "item:bone_flute", ["The thawed tin's lid is rusted down.", "Hold the thawed tin in your tray and pry it open."], [{"take": "thawed_tin"}, {"give": "bone_flute"}], "A bone flute."),
 step("hatch", "hatch_open", ["The hatch in the floor is frozen under a foot of ice.", "Burn pages until the stove is at its hottest, then touch the hatch in the floor."], [{"set": "heat", "value": 3}, {"set": "hatch_open"}], "The hatch opens."),
 step("down", "left9", ["The way down is open.", "Climb down through the hatch in the floor."], [{"set": "left9"}, {"complete_room": [10, "THE SHAFT", "You climb down into the ice."]}], "Down you go."),
]
walk = [["shot", "start"], ["tap", "survey_log"], ["tap", "hwin"], ["tap", "stove"], ["shot", "heat1"], ["tap", "stove"], ["expect", "case_free"] if False else ["wait", 0.1],
 ["tap", "spec"], ["shot", "case"], ["expect", "case_free"],
 ["tap", "hwin"], ["shot", "window"], ["tap", "spec_latch"],
 ["repeat", 3, ["tap", "dial_r"]], ["repeat", 8, ["tap", "dial_b"]], ["tap", "dial_g"], ["tap", "spec_latch"], ["wait", 1.0], ["expect", "case_open"],
 ["tap", "tin_part"], ["use", "frozen_tin", "stove"], ["tap", "stove"], ["use", "frozen_tin", "stove"], ["examine", "thawed_tin"], ["reshape", "thawed_tin"], ["journal"],
 ["tap", "ice_hatch"], ["tap", "stove"], ["tap", "stove"], ["tap", "stove"], ["shot", "hot"], ["tap", "ice_hatch"], ["shot", "hatch"], ["tap", "ice_hatch"], ["wait", 2.0]]
room = {"title": "Hut 4", "walls": "r9_wall_", "floor": "r9_floor", "ceiling": "r9_ceiling", "intro": "It is cold enough to kill you.",
        "on_enter": [{"set": "heat", "value": 0},
          journal("hut", "Hut 4", "Hut 4 of the Kingsport Antarctic Survey, on the plateau, abandoned in 1926. The ship left me at the edge of the ice and did not wait. I am no longer writing this for anyone. I am writing it for the cabinet."),
          journal("blank", "A blank page", "(Blank. You don't remember leaving a page blank.)")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room9_hut.json", room)
print("room9 ok")

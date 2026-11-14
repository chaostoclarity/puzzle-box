from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
ORDER = "2041635"   # chimes 3 1 5 2 from the score, then 7 4 6 from the ice
HALV = journal("halvorsen", "Halvorsen's note", "Through the ice, the note in Halvorsen's coat pocket: \"The stone in the plug turns one point for every page the hut's fire has eaten. I fed it four and turned it four. Then I blew. Then I understood, and stayed.\"")
CH = [sprite("n", "chime_%d" % k, [-4.5 + k * 1.5, 13.5], [1, 7], "chime_%d" % k, depth=0.1) for k in range(7)]
objs = CH + [
 sprite("e", "frozen_man", [-3, 3], [3, 6], "frozen_man"),
 sprite("e", "frozen_note", [-3, 3], [3, 6], "frozen_note", depth=0.12, lens=2),
 {"type": "box", "name": "cham", "wall": "e", "pos": [3.5, 4.0], "depth": 1.0, "scale": 0.45, "view": "front", "size": 6,
  "faces": {"front": "cham_front", "back": "cham_back", "left": "cham_side", "right": "cham_side", "top": "cham_top", "bottom": "cham_top"},
  "liner": "cham_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "cham",
  "parts": [part("front", [-1.5, 0], [1, 1], "tone_hole", "hole_a", depth=0.04), part("front", [0, 0], [1, 1], "tone_hole", "hole_b", depth=0.04),
            part("front", [1.5, 0], [1, 1], "tone_hole", "hole_c", depth=0.04)],
  "inner_sprites": [{"id": "frag_part", "tex": "score", "size": [2, 1.5], "pos": [0, -2.2, 0], "rot": [-90, 0, 0], "face": "top"}]},
 sprite("s", "rope_ladder", [0, 5], [3, 10], "rope_ladder"),
 {"type": "box", "name": "plug", "wall": "w", "pos": [0, 4.0], "depth": 1.0, "scale": 0.45, "view": "front", "size": 6,
  "faces": {"front": "plug_front", "back": "plug_back", "left": "plug_side", "right": "plug_side", "top": "plug_top", "bottom": "plug_top"},
  "liner": "plug_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "plug",
  "parts": [part("front", [0, 0.5], [4, 4], "star5_0", "star", depth=0.04), part("front", [0, -2.6], [0.75, 0.75], "flute_hole", "flute_hole", depth=0.04)],
  "inner_sprites": [{"id": "stone_part", "tex": "item_seal_stone5", "size": [1.5, 1.5], "pos": [0, -2.2, 0], "rot": [-90, 0, 0], "face": "top"}]},
]
puzzles = [
 {"kind": "melody", "parts": {"chime_%d" % k: str(k) for k in range(7)}, "order": ORDER, "flag": "played", "echo_from": 4, "lock": "chimes_done",
  "wrong": [{"sfx": "crack"}, say("The chimes jangle out of tune. The ice goes quiet again.")],
  "do": [{"set": "chimes_done"}, {"sfx": "crack"}, {"shake": True}, say("The last note hangs in the air, and the ice on the east wall splits open around a chamber of blue glass.", 5)]},
 {"kind": "sequence", "parts": {"hole_a": "a", "hole_b": "b", "hole_c": "c"}, "tex": {"hole_a": "tone_hole", "hole_b": "tone_hole", "hole_c": "tone_hole"}, "pulled_suffix": "_lit", "order": "cab", "flag": "holes", "silent": True, "lock": "cham_open",
  "do": [{"set": "cham_open"}, {"sfx": "unlock"}, {"face": "top"}, say("The chamber hums the three notes back and its lid lifts. Inside: the torn end of the score.")],
  "fail": [{"sfx": "thunk"}, say("The chamber gives back a sour note.")]},
 {"kind": "cycler", "part": "star", "flag": "star", "count": 5, "sfx": "stone", "textures": ["star5_%d" % k for k in range(5)], "lock": "plug_open"},
 {"kind": "none"},
]
FRAG = [{"set": "frag5"}, {"fragment": True}, {"sfx": "reveal"}, journal("frag5", "Fragment V", "Wren's fifth fragment, written on the back of the torn score: \"Every seal asks for something. The first ones asked for my time. This one asked for my words, and I gave them, page by page, to keep warm. By the seventh they will ask for things I do not know I have.\""), say("The torn end of the score. On its back, in Wren's hand: a fragment.")]
puzzles = puzzles[:-1] + [
 {"kind": "pickup", "part": "stone_part", "item": "seal_stone5", "flag": "stone5_taken", "show_if": "plug_open", "then": [say("The fifth seal. Cold to the core.")]},
]
bindings = [
 vis("frag_part", ["cham_open", "!frag5"]),
 bind("box:cham", "chimes_done", {"visible": True}, {"visible": False}),
 bind("hinge:cham.top", "cham_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("box:cham", "cham_open", {"tappable": False}, {"tappable": True}),
 bind("box:plug", "plug_open", {"tappable": False}, {"tappable": True}),
 bind("hinge:plug.top", "plug_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
]
open_plug = [{"set": "plug_open"}, {"sfx": "horn"}, {"wait": 1.0}, {"sfx": "unlock"}, {"face": "top"}, say("You blow. The star-stone takes the note and holds it, and the plug's lid rises on a pale stone.", 5)]
interactions = [
 uses("bone_flute", ["flute_hole", "plug", "star"], open_plug, when=["!plug_open", "burned%%5=%d" % k, "star=%d" % k]) for k in range(5)
] + [
 uses("bone_flute", ["flute_hole", "plug", "star"], [{"sfx": "horn"}, {"shake": True}, say("The flute shrieks in the hole. The star doesn't take the note.")], when="!plug_open"),
 tap("flute_hole", [say("A hole in the plug, sized for a mouthpiece.")]),
] + [tap("hole_" + h, [{"sfx": "tone_" + n}], when="!cham_open", handled=False) for h, n in (("a", "3"), ("b", "5"), ("c", "6"))] + [
 tap("frag_part", FRAG, when=["cham_open", "!frag5"]),
 tap("frozen_man", [say("A man frozen into the wall, standing. Survey coat. His eyes are open. There is paper in his pocket, too deep in the ice to see.")]),
 tap("frozen_note", [HALV, {"set": "note_read"}]),
 tap("rope_ladder", [say("The ladder back up to the hut. Not without the seal.")], when="!stone5_taken"),
 tap("rope_ladder", [{"set": "left10"}, {"take": "bone_flute"}, {"complete_room": [105, "THE FIFTH SEAL", "You climb out of the ice with the stone against your chest. Behind you, the chimes ring once on their own."]}], when="stone5_taken"),
]
steps = [
 step("score", "chimes_done", ["The torn score in your journal is for these chimes.", "Play chimes 3, 1, 5, 2 (counting from the left). Then listen: the ice hums the rest; play what it hums."],
      [{"set": "chimes_done"}], "The ice splits open."),
 step("holes", "cham_open", ["Each hole in the glass chamber hums one note. You have heard these notes before.", "Touch the holes in the order the ice hummed its notes: right, left, middle."],
      [{"set": "cham_open"}], "The chamber opens."),
 step("note", "note_read", ["The frozen man has something in his pocket.", "Look at the frozen man with the Lens turned on."], [HALV, {"set": "note_read"}], "His note is in your journal."),
 step("plug", "plug_open", ["Halvorsen's note says how far to turn the star in the plug.", "Turn the star one point for every page you burned in the hut, then blow the bone flute into the hole."],
      [{"set": "plug_open"}], "The plug opens."),
 step("stone", "stone5_taken", ["The plug held the seal.", "Take the stone from the plug."], [{"give": "seal_stone5"}, {"set": "stone5_taken"}], "The fifth seal is yours."),
 step("up", "left10", ["The ladder goes back up.", "Climb the rope ladder."], [{"set": "left10"}, {"complete_room": [105, "THE FIFTH SEAL", "You climb out of the ice."]}], "Up you go."),
]
walk = [["shot", "start"]] + [["tap", "chime_%d" % int(c)] for c in ORDER[:4]] + [["wait", 1.0], ["shot", "echo"]] + [["tap", "chime_%d" % int(c)] for c in ORDER[4:]] + [["wait", 2.0], ["expect", "chimes_done"],
 ["tap", "cham"], ["shot", "chamber"], ["tap", "hole_c"], ["tap", "hole_a"], ["tap", "hole_b"], ["wait", 1.5], ["expect", "cham_open"], ["tap", "frag_part"], ["expect", "frag5"], ["back"],
 ["lens", True], ["tap", "frozen_note"], ["expect", "note_read"], ["lens", False], ["tap", "plug"], ["shot", "plug"], ["repeat", 6, ["use", "bone_flute", "flute_hole"], ["tap", "star"]], ["wait", 2.0], ["expect", "plug_open"], ["shot", "plug_open"], ["tap", "stone_part"], ["shot", "after_stone"], ["expect", "stone5_taken"], ["back"], ["tap", "rope_ladder"], ["wait", 2.0]]
room = {"title": "The Shaft", "walls": "r10_wall_", "floor": "r10_floor", "ceiling": "r10_ceiling", "intro": "The ice hums.",
        "on_enter": [journal("shaft", "The shaft", "Under the hut, a shaft cut into blue ice, and at the bottom a chamber where seven ice chimes hang from the ceiling. The cold here has a sound to it.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room10_shaft.json", room)
print("room10 ok")

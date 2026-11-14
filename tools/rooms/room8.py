from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
FRAG = journal("fragment4", "Wren's fragment, IV", "Inside the well-house post, visible only through both lenses, a folded paper pushed into a hole and plugged with wax:\n\n\"I never went down the well. I sent the lens element down on the chain and looked through it from above, and I saw what the Gardners saw. That is the fourth seal: you do not have to go to the thing. You only have to look. Elias, you will look. I know you.\"")
WELL_J = journal("well", "The well house", "A plank shed over the Gardner well. The windlass is overhead, the chain runs down into the dark, and the drum has no handle. Somewhere down there, Nahum wrote, the stone that fell from the sky is still glowing.")

objs = [
 sprite("u", "drum", [0, 7.5], [10, 3], "drum_5"),
 sprite("u", "handle_on", [5.4, 7.5], [1.5, 1.5], "handle_fitted", depth=0.05, tappable=False),
 sprite("d", "shaft", [0, 7.5], [7, 7], "shaft_5", depth=0.02),
 sprite("d", "carving", [0, 7.5], [7, 7], "carv_5", depth=0.04, tappable=False, lens=2),
 {"type": "box", "name": "bucket", "wall": "d", "pos": [0, 7.5], "depth": 1.2, "scale": 0.4, "view": "front", "size": 6,
  "faces": {"front": "bucket_front", "back": "bucket_back", "left": "bucket_side", "right": "bucket_side", "top": "bucket_top", "bottom": "bucket_top"},
  "liner": "bucket_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "bucket",
  "parts": [part("front", [-1.75, 0.5], [1, 1], "wdial_0", "dialA"),
            part("front", [0, 0.5], [1, 1], "pdial_0", "dialB", depth=0.045, lens=2),
            part("front", [1.75, 0.5], [1, 1], "wdial_0", "dialC"),
            part("front", [0, -1.5], [0.75, 0.75], "bucket_pin", "bucket_pin", depth=0.04)],
  "children": [{"name": "jar_mini", "faces": {"front": "jar_front", "back": "jar_back", "left": "jar_side", "right": "jar_side", "top": "jar_top", "bottom": "jar_top"},
                "liner": "jar_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "dive:jar", "scale": 0.3, "pos": [0, -1.2, 0]}]},
 {"type": "stage_box", "name": "jar", "view": "front",
  "faces": {"front": "jar_front", "back": "jar_back", "left": "jar_side", "right": "jar_side", "top": "jar_top", "bottom": "jar_top"},
  "liner": "jar_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "jar",
  "parts": [part("front", [0, 0], [4, 4], "jar_roots", "jar_roots", depth=0.04)],
  "inner_sprites": [{"id": "seal4_part", "tex": "item_seal_stone4", "size": [1.5, 1.5], "pos": [0, -1.5, -1.0]}]},
 sprite("n", "tool_rack", [-3, 9], [4, 3], "tool_rack"),
 sprite("n", "post", [4, 8], [1.5, 12], "clear", depth=0.02),
 sprite("n", "post_note", [4, 9], [3, 4], "post_note", depth=0.05, lens=2),
 sprite("e", "shed_door", [0, 4.5], [4.5, 9], "shed_door"),
 sprite("s", "knothole", [-2, 6], [1, 1], "knothole"),
 sprite("w", "scorch", [0, 8], [6, 6], "clear", depth=0.02),
]
CYC = lambda part_, tex_, lens=False: {"kind": "cycler", "part": part_, "flag": part_, "count": 10, "spin": False, "sfx": "tick",
                                       "textures": ["%s_%d" % (tex_, k) for k in range(10)], "lock": "bucket_open"}
puzzles = [
 {"kind": "cycler", "part": "drum", "flag": "depth", "count": 6, "start": 5, "spin": False, "sfx": "creak", "textures": ["drum_%d" % k for k in range(6)],
  "lock": "!handle_fitted", "locked_say": "The drum has no handle. There's a square socket at its end.",
  "on": {"0": [{"set": "raised"}, say("You crank the chain all the way up. The bucket swings out of the dark onto the well's lip.", 5)],
         "1": [say("You let the chain down a turn.")], "2": [say("Another turn down.")], "3": [say("Further down.")], "4": [say("Deeper.")], "5": [say("The chain hits bottom.")]}},
 {"kind": "pickup", "part": "knothole", "item": "lens_element", "flag": "element_taken", "then": [say("Wedged in a knothole: a disc of ground green glass with Wren's mark on the rim. Put it with the Lens in your tray.", 6)]},
 CYC("dialA", "wdial"), CYC("dialB", "pdial"), CYC("dialC", "wdial"),
 {"kind": "combo", "flags": ["dialA", "dialB", "dialC"], "code": [7, 2, 4], "commit": "bucket_pin", "lock": "bucket_open",
  "fail": [{"sfx": "thunk"}, say("You press the pin. The bucket's lid stays down.")],
  "do": [{"set": "bucket_open"}, {"sfx": "unlock"}, {"face": "top"}, say("The lid of the bucket lifts. Inside, a stone jar choked with grey roots.")]},
 {"kind": "pickup", "part": "seal4_part", "item": "seal_stone4", "flag": "seal4_taken", "show_if": "jar_open", "sfx": "reveal",
  "then": [{"take": "shears"}, {"take": "handle"}, journal("seal4", "The fourth seal", "The fourth stone was in the jar the Gardners lowered down their own well. It has a speck of colour at its heart that has no name. I looked at it too long. When I looked away, the shed was a different grey."),
           {"wait": 1.2}, {"complete_room": [104, "SEAL IV OF IX BROKEN", "You walk back to Arkham along the road, and for a mile behind you the verges go grey.\n\nYou carry the stone home."]}]},
]
bindings = [
 bind("shaft", None, {"texture": "shaft_{depth}"}),
 bind("carving", None, {"texture": "carv_{depth}"}),
 bind("handle_on", "handle_fitted", {"visible": True}, {"visible": False}),
 bind("box:bucket", "depth=0", {"visible": True}, {"visible": False}),
 bind("box:bucket", ["depth=0", "!bucket_open"], {"tappable": True}, {"tappable": False}),
 bind("hinge:bucket.top", "bucket_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("hinge:jar.front", "jar_open", {"hinge": 100}, {"hinge": 0}, anim=0.9),
 bind("hinge:jar_mini.front", "jar_open", {"hinge": 100}, {"hinge": 0}),
 bind("box:jar", "jar_open", {"tappable": False}, {"tappable": True}),
 vis("jar_roots", "!jar_open"),
]
interactions = [
 use("handle", "drum", [{"take": "handle"}, {"set": "handle_fitted"}, {"sfx": "thunk"}, say("The handle from Abby's box fits the drum.")]),
 tap("shaft", [say("The well. The chain goes down into a dark that smells of struck matches.")], when="!lens"),
 tap("shaft", [say("Through both lenses the well's stones go thin as paper. Something is carved behind them, at the depth the chain reaches.")]),
 tap("dialB", [], when="lens"),
 tap("tool_rack", [say("Nahum's tools, furred grey.")]),
 tap("post", [say("A heavy post holding up the roof. There's a plug of wax in a hole near the top.")], when="!lens"),
 tap("post", [say("Through the Lens the post is hollow, and something is folded inside.")]),
 tap("post_note", [{"set": "fragment4"}, {"fragment": True}, {"sfx": "reveal"}, FRAG, say("A note from Wren inside the post. It's in your journal.", 5)], when="!fragment4"),
 tap("shed_door", [say("The yard. Nothing out there but grey ash to the fence.")]),
 tap("scorch", [say("Scorched boards, in the shape of a man reaching for the well.")]),
 tap("jar_roots", [say("Grey roots knotted over the jar's mouth.")]),
 use("shears", "jar_roots", [{"set": "jar_open"}, {"sfx": "slide"}, say("You cut the roots away. They don't grow back. Whatever fed them is inside the jar.")]),
 tap("lift:bucket", [say("The bucket is down the well.")], when="!depth=0"),
]
steps = [
 step("element", "element_taken", ["The shed's walls aren't all solid. Something catches the light in the south wall.", "Take what's wedged in the knothole in the south wall."], [{"give": "lens_element"}, {"set": "element_taken"}], "A disc of ground glass."),
 step("lens2", "item:lens2", ["The glass disc belongs with something you carry.", "In your tray, select the glass disc, then touch Wren's Lens."], [{"take": "lens_element"}, {"take": "lens"}, {"give": "lens2"}], "The Lens is doubled."),
 step("handle", "handle_fitted", ["The windlass drum overhead has no handle.", "Look up and use the crank handle on the drum."], [{"take": "handle"}, {"set": "handle_fitted"}], "The handle is fitted."),
 step("raise", "raised", ["The bucket is at the bottom of the well.", "Turn the drum until the chain comes all the way up."], [{"set": "depth", "value": 0}, {"set": "raised"}], "The bucket comes up."),
 step("dials", "bucket_open", ["The bucket has two dials and the shadow of a third. Through both lenses the well's stones show carvings, one at each of three depths.",
      "Let the chain down one turn at a time and look into the well through the Lens: I 7, II 2, III 4. Raise the bucket, set the dials (the middle one only through the Lens) and press the pin."],
      [{"set": "dialA", "value": 7}, {"set": "dialB", "value": 2}, {"set": "dialC", "value": 4}, {"set": "bucket_open"}], "The bucket opens."),
 step("jar", "jar_open", ["The jar in the bucket is choked with roots.", "Dive into the jar and cut the roots with Nahum's shears."], [{"set": "jar_open"}], "The jar opens."),
 step("seal", "seal4_taken", ["The jar holds the fourth seal.", "Take the stone from the jar."], [{"give": "seal_stone4"}, {"set": "seal4_taken"}, {"complete_room": [104, "SEAL IV OF IX BROKEN", "You carry the stone home."]}], "The fourth seal is yours."),
]
walk = [["shot", "start"], ["tap", "knothole"], ["combine", "lens_element", "lens"], ["expect", "element_taken"],
 ["tap", "drum"], ["use", "handle", "drum"], ["tap", "drum"], ["expect", "raised"], ["shot", "raised"], ["tap", "shaft"],
 ["tap", "drum"], ["lens", True], ["tap", "shaft"], ["shot", "carving1"],
 ["tap", "drum"], ["tap", "drum"], ["tap", "shaft"], ["shot", "carving3"], ["tap", "drum"], ["tap", "drum"], ["tap", "shaft"], ["shot", "carving5"],
 ["tap", "post_note"], ["expect", "fragment4"], ["tap", "drum"], ["lens", False],
 ["tap", "bucket"], ["shot", "bucket"], ["repeat", 7, ["tap", "dialA"]], ["repeat", 4, ["tap", "dialC"]], ["lens", True], ["shot", "bucket_lens"], ["repeat", 2, ["tap", "dialB"]], ["lens", False],
 ["tap", "bucket_pin"], ["wait", 1.0], ["expect", "bucket_open"], ["shot", "bucket_open"],
 ["tap", "dive:jar"], ["use", "shears", "jar_roots"], ["wait", 1.0], ["tap", "seal4_part"], ["wait", 3.0]]
room = {"title": "The Well House", "walls": "r8_wall_", "floor": "r8_floor", "ceiling": "r8_ceiling",
        "on_enter": [{"set": "depth", "value": 5}, WELL_J], "objects": objs, "puzzles": puzzles, "bindings": bindings,
        "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room8_well.json", room)
print("room8 ok")

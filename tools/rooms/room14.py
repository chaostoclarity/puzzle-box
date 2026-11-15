from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
FACADES = ["home", "r1", "r2", "r3", "r4", "l1", "l2"]
W = "nesw"
objs = []
for f in FACADES:
    for w in W:
        objs.append(sprite(w, "fac_%s_%s" % (f, w), [0, 11], [15, 22], "fac_" + f, depth=0.02))
for w in W:
    objs.append(sprite(w, "vane_%s" % w, [0, 14.5], [4, 4], "vane_bare", depth=0.05))
    objs.append(sprite(w, "rope_%s" % w, [1.9, 9.5], [1, 6], "bell_rope", depth=0.05))
objs.append({"type": "box", "name": "mbox", "wall": "d", "pos": [0, 7.5], "depth": 1.0, "scale": 0.4, "view": "front", "size": [6, 4, 4],
  "faces": {"front": "mbox_front", "back": "mbox_back", "left": "mbox_side", "right": "mbox_side", "top": "mbox_top", "bottom": "mbox_top"},
  "liner": "mbox_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "mbox",
  "parts": [part("front", [-2 + i, 0.4], [0.875, 1.75], "mkey_d", "slot%d" % i, depth=0.04) for i in range(5)] + [part("front", [0, -1.4], [1, 1], "vcase_clasp", "crank", depth=0.04)],
  "inner_sprites": [{"id": "stone_part", "tex": "item_seal_stone7", "size": [1.5, 1.5], "pos": [0, -1.4, 0], "rot": [-90, 0, 0], "face": "top"}]})
puzzles = [
 {"kind": "swap", "parts": ["slot%d" % i for i in range(5)], "flag": "mb", "start": "deaga", "tex": "mkey_%s", "lock": "mbox_open"},
 {"kind": "pickup", "part": "stone_part", "item": "seal_stone7", "flag": "stone7_taken", "show_if": "mbox_open", "then": [say("The seventh seal. Hold it to your ear: the street.")]},
]
bindings = []
for f in FACADES:
    for w in W:
        bindings.append(vis("fac_%s_%s" % (f, w), "facade=" + f))
for w in W:
    bindings.append(vis("fac_r3_" + w, "facade=r3"))
    bindings.append(bind("fac_r3_" + w, "bdoor_open", {"texture": "fac_r3_open"}, {"texture": "fac_r3"}))
    bindings.append(vis("vane_" + w, "facade=l2"))
    bindings.append(bind("vane_" + w, "cock_on", {"texture": "vane_{vane:7}"}, {"texture": "vane_bare"}))
    bindings.append(vis("rope_" + w, "facade=l2"))
bindings += [bind("box:mbox", "bdoor_open", {"visible": True}, {"visible": False}),
             bind("box:mbox", "mbox_open", {"tappable": False}),
             bind("hinge:mbox.top", "mbox_open", {"hinge": 110}, {"hinge": 0}, anim=1.0)]
def ids(f): return ["fac_%s_%s" % (f, w) for w in W]
interactions = [
 uses("vane_cock", ["vane_" + w for w in W] + ids("l2"), [{"take": "vane_cock"}, {"set": "cock_on"}, {"set": "vane", "value": 3}, {"sfx": "thunk"},
      say("You fit the weathercock back on its spindle. It swings and settles, though there is no wind. When you turn your head, it turns too.", 5)], when="facade=l2"),
 taps(["vane_" + w for w in W], [say("A bare iron spindle on the spire, with N, E, S and O cut round it. The cock is gone.")], when="!cock_on"),
 taps(["vane_" + w for w in W], [say("The weathercock. It turns whenever the street does: one way when you go left, the other when you go right.")]),
 taps(["rope_" + w for w in W], [{"set": "bell_rung"}, {"sfx": "horn"}, {"wait": 1.0}, {"set": "bdoor_open"}, {"sfx": "creak"},
      say("The bell. As it rings, somewhere off to your right a door unlatches.", 5)], when=["cock_on", "vane=2", "!bell_rung"]),
 taps(["rope_" + w for w in W], [{"sfx": "horn"}, say("The bell rings. Nothing answers. The cock is not facing the wind.")], when=["cock_on", "!bell_rung"]),
 taps(["rope_" + w for w in W], [say("The bell rope. The poster said something about the cock and the wind.")], when="!cock_on"),
 taps(["rope_" + w for w in W], [say("The bell has rung.")]),
 taps(ids("home"), [say("Number 7. The violist's house. The door you came out of is a blank wall now.")]),
 taps(ids("r1"), [say("A patisserie, shuttered. There is bread in the window that has been there a hundred years.")]),
 taps(ids("r2"), [{"set": "poster_read"}, journal("poster", "The poster", "A recital bill pasted on a wall: THE MUTE VIOLIST PLAYS IT BACKWARD, WHEN THE COCK FACES THE WIND."), say("A recital poster. It's in your journal.")]),
 taps(ids("r3"), [say("A house with a blue door. Locked.")], when="!bdoor_open"),
 taps(ids("r3"), [say("The blue door stands open on nothing. Something has rolled out of it onto the cobbles at your feet.")]),
 taps(ids("r4"), [say("A chimney with smoke blowing off it, and a compass cut into the wall below: N, E, S, O. The smoke drifts toward the O.")]),
 taps(ids("l1"), [say("Steps down to the river, gated. The river is making the wrong sound.")]),
 taps(ids("l2"), [say("A church, very narrow. A weathervane on the spire and a bell rope hanging by the door.")]),
 tap("crank", [{"set": "mbox_open"}, {"sfx": "unlock"}, {"face": "top"}, say("You turn the crank. The tune comes out backwards, and it is the right way round. The lid lifts on a violet stone.", 5)], when=["mb=agead", "!mbox_open"]),
 tap("crank", [{"sfx": "creak"}, say("The crank turns and the box plays something wrong. The lid stays down.")], when="!mbox_open"),
 tap("crank", [say("The box has played.")]),
 taps(ids("home"), [{"set": "left14"}, {"complete_room": [107, "THE SEVENTH SEAL", "You turn left, and left, and left, and the street lets you go. You are standing in Garrison Street with snow on your coat and the tune in your mouth."]}], when="stone7_taken"),
]
interactions.insert(0, interactions.pop())   # leaving takes priority over the home facade's text
steps = [
 step("poster", "poster_read", ["The street turns more times one way than the other. Walk it.", "Turn right twice to find a poster on a wall, and read it."], [{"set": "poster_read"}], "The poster is in your journal."),
 step("mount", "cock_on", ["The church has a weathervane with no cock. You have one.", "Turn left twice to the church and use the weathercock on the spindle at the top of the spire."], [{"take": "vane_cock"}, {"set": "cock_on"}, {"set": "vane", "value": 3}], "The cock is on."),
 step("wind", "bell_rung", ["The cock should face the wind. Smoke shows where the wind goes; the cock points to where it comes from. The cock turns with the street.",
      "The smoke drifts to O (west), so the wind comes from E. Each left turn moves the cock one point clockwise, each right turn one point back. Get it to E while at the church, then pull the bell rope."],
      [{"set": "vane", "value": 2}, {"set": "bell_rung"}, {"set": "bdoor_open"}], "The bell rings."),
 step("box", "mbox_open", ["A music box rolled out of the blue door. The violist's tune goes in it, the way the poster says.",
      "Arrange the keys A G E A D (the notebook's D A E G A, backwards), then turn the crank."], [{"set": "mb", "value": "agead"}, {"set": "mbox_open"}], "The box opens."),
 step("stone", "stone7_taken", ["The music box held the seal.", "Take the stone."], [{"give": "seal_stone7"}, {"set": "stone7_taken"}], "The seventh seal."),
 step("home", "left14", ["Go back to the violist's house.", "Walk the street until you see number 7 again, and touch it."], [{"set": "left14"}, {"complete_room": [107, "THE SEVENTH SEAL", "You go home."]}], "Home."),
]
R, L = -200, 200   # swipe right / left
def swaps(start, goal):
    s = list(start); out = []
    for i in range(5):
        if s[i] != goal[i]:
            j = next(k for k in range(i + 1, 5) if s[k] == goal[i]); out += [["tap", "slot%d" % i], ["tap", "slot%d" % j]]; s[i], s[j] = s[j], s[i]
    return out
walk = [["shot", "start"], ["expect", "!facade=r1"], ["swipe", R], ["expect", "facade=r1"], ["swipe", R], ["expect", "facade=r2"], ["tapv", "fac_r2_s"], ["shot", "poster"],
 ["swipe", R], ["swipe", R], ["expect", "facade=r4"], ["tapv", "fac_r4_n"], ["shot", "smoke"], ["swipe", R], ["expect", "facade=home"],
 ["swipe", L], ["swipe", L], ["expect", "facade=l2"], ["shot", "church"], ["usev", "vane_cock", "vane_w"], ["expect", "cock_on"],
 ["swipe", R], ["swipe", R], ["swipe", R], ["swipe", L], ["swipe", L], ["expect", "facade=l2"], ["expect", "vane=2"], ["shot", "vane"], ["tapv", "rope_n"], ["wait", 1.5], ["expect", "bdoor_open"],
 ["tap", "mbox"], ["shot", "mbox"]] + swaps("deaga", "agead") + [["tap", "crank"], ["wait", 1.5], ["expect", "mbox_open"], ["tap", "stone_part"], ["expect", "stone7_taken"], ["back"], ["expect", "facade=l2"], ["swipev", 200], ["shot", "after_box"],
 ["swipe", L], ["shot", "going_home"], ["expect", "facade=home"], ["tapv", "fac_home_w"], ["wait", 2.0]]
room = {"title": "The Street", "walls": "r14_wall_", "floor": "r14_floor", "ceiling": "r14_ceiling", "intro": "Five turns one way. Three the other.",
        "street": {"right": 5, "left": 3, "vane": "vane", "vane_while": "cock_on"},
        "on_enter": [{"set": "facade", "value": "home"}, {"set": "last_view", "value": 0},
                     journal("street", "The street", "The violist's street. Turn right and it takes five turns to bring me back to his door. Turn left and it takes three. I counted twice. I counted my fingers too, after.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room14_street.json", room)
print("room14 ok")

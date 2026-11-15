from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
WALLS = [[0, 2], [0, 3], [0, 5], [1, 0], [1, 4], [2, 5], [3, 0], [3, 3], [4, 0], [5, 3]]
FRAG = [{"set": "frag9"}, {"fragment": True}, {"sfx": "reveal"},
        journal("frag9", "Fragment IX", "In the hollow the dream hid, scratched by Wren with a nail: \"I got this far in my sleep, every night for a year. The last seal is not a place. It is the cabinet, and the cabinet is a mind, and it wants what you use to see and what you use to ask. Give it those and keep the rest. Elias, keep the rest.\""),
        say("Scratched in the hollow, in Wren's hand: the last fragment.", 4)]
objs = [
 {"type": "box", "name": "slab", "wall": "d", "pos": [0, 7.5], "depth": 0.6, "scale": 0.5, "view": "top", "size": [6, 2, 6],
  "faces": {"front": "slab_front", "back": "slab_front", "left": "slab_side", "right": "slab_side", "top": "slab_top", "bottom": "slab_bottom"},
  "blocker": "slab", "parts": [part("top", [-2.5, 2.5], [0.75, 0.75], "marble", "marble", depth=0.05, tappable=False)]},
] + [sprite("d", "dust_%s" % k, [0, 12.5], [6, 2], "dust_" + k, depth=0.02, tappable=False) for k in "nesw"] + [
 sprite("n", "n_dust", [0, 1.5], [6, 2], "dust_s", tappable=True),
 sprite("u", "ceil_door", [0, 7.5], [5, 5], "ceil_door"),
 sprite("w", "niche_dream", [0, 6], [4, 6], "niche_dream", depth=0.02),
 dict(sprite("w", "wall_slab", [0, 6], [4, 6], "wall_slab", depth=0.04), lens_hide=3),
 sprite("s", "wrong_stair", [0, 5], [6, 10], "wrong_stair"),
]
puzzles = [
 {"kind": "roll", "id": "maze", "box": "slab", "face": "top", "cols": 6, "rows": 6, "cell": 1.0, "center": [0, 0], "token": "marble", "flag": "marble",
  "start": [0, 0], "walls": WALLS, "goal": [5, 5], "done": "marble_home", "lock": "marble_home", "buttons": {},
  "do": [{"sfx": "thunk"}, {"wait": 0.4}, {"sfx": "crack"}, {"shake": True}, say("Somewhere you can't see, the marble drops into the hole. Above you, in the ceiling, a bar scrapes back.", 5)]},
]
bindings = [vis("dust_%s" % k, "gravity=" + k) for k in "nesw"] + [
 tex("ceil_door", "ceil_open", "ceil_door_open", "ceil_door"),
]
interactions = [
 uses("elder_sign", ["ceil_door"], [{"take": "elder_sign"}, {"set": "ceil_open"}, {"sfx": "horn"}, {"shake": True}, say("You press the sign to the stone. The door in the ceiling swings down, which is up, and green water stands in it without falling.", 5)], when="marble_home"),
 uses("elder_sign", ["ceil_door"], [{"shake": True}, say("The sign holds the door, but the door is still barred from the other side.")]),
 tap("ceil_door", [{"set": "left17"}, {"complete_room": [18, "INSIDE THE CABINET", "You climb up into the water and fall down out of it, into a small wooden room lined with sockets. You know this wood. You are inside Wren's cabinet."]}], when="ceil_open"),
 tap("ceil_door", [say("A door in the ceiling, barred, with a five-armed sign worn into it.")], when="!marble_home"),
 tap("ceil_door", [say("The bar is gone. The door wants the sign it was carved with.")]),
 tap("niche_dream", FRAG + [{"set": "sign_taken"}, {"give": "elder_sign"}, say("In the hollow behind the dream: the Elder Sign, and Wren's last fragment.", 5)], when="!sign_taken"),
 tap("niche_dream", [say("An empty hollow.")]),
 tap("n_dust", [say("Dust slides down the wall and across the floor toward you, following your eyes. Look down: there's a slab in the floor with a marble in it.", 5)]),
 tap("wall_slab", [say("A slab of green stone, fitted too well. It looks like it was dreamed there.")]),
 tap("wrong_stair", [{"set": "marble", "value": "0,0"}, {"sfx": "slide"}, {"refresh": True}, say("You go down the stair and arrive back at its top, in this room, as if you never left. Behind you, the marble rattles back to its corner of the slab.", 5)], when="!marble_home"),
 tap("wrong_stair", [say("A stair. It goes down. When you look along it, it goes up. Whichever way you look is down.")]),
 tap("slab", [say("A slab with a maze cut in its face and a pale marble in it. It rolls toward whichever way you look.")], handled=False),
]
steps = [
 step("dust", ["any", "gravity=e", "gravity=s", "gravity=w", "gravity=n"], ["Things here fall toward whichever wall you look at. Watch the dust on the floor.", "Turn to another wall, then look down at the dust and the marble. If the marble gets stuck, walk the wrong stair on the south wall to start it over."], [{"set": "gravity", "value": "e"}], "The dust moves."),
 step("maze", "marble_home", ["Roll the marble into the hole by turning to face walls.", "From facing north: east, south, east, south, west, south, east, south, east, south. You can only turn a quarter at a time, and every quarter turn rolls it."], [{"set": "marble", "value": "5,5"}, {"set": "marble_home"}], "The marble drops."),
 step("sign", "sign_taken", ["The west wall is not all there. Something is dreamed over it.", "Look at the west wall with dream sight (Lens on) and touch the hollow."], FRAG + [{"set": "sign_taken"}, {"give": "elder_sign"}], "The Elder Sign."),
 step("door", "ceil_open", ["The ceiling door is carved with the same sign.", "Look up and use the Elder Sign on the ceiling door."], [{"take": "elder_sign"}, {"set": "ceil_open"}], "The door opens."),
 step("up", "left17", ["The door is open.", "Touch the open door in the ceiling."], [{"set": "left17"}, {"complete_room": [18, "INSIDE THE CABINET", "You go through."]}], "Through."),
]
R, L = -200, 200
walk = [["shot", "start"]] + [["swipe", x] for x in (R, R, L, R, R, L, L, R, L, R)] + [["expect", "marble_home"], ["tapv", "slab"], ["shot", "slab"], ["back"],
 ["lens", True], ["tap", "niche_dream"], ["lens", False], ["expect", "sign_taken"], ["use", "elder_sign", "ceil_door"], ["expect", "ceil_open"], ["tap", "ceil_door"], ["wait", 2.0]]
room = {"title": "The Last Stair", "walls": "r17_wall_", "floor": "r17_floor", "ceiling": "r17_ceiling", "intro": "Down is wherever you look.", "gravity": "maze",
        "on_enter": [journal("stair", "The last stair", "The drawer's stair came out in a chamber of green stone where no angle is right. When I turn my head, the dust on the floor slides after my eyes. Down is wherever I look.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room17_stair.json", room)
print("room17 ok")

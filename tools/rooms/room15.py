from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
DREAMJ = journal("dream15", "The dream", "I am in my study and it is tidy. The papers are squared, the ink is capped, the salt is gone from the door. The clock on the wall is running backwards. There is a note on the desk in my own hand that I did not write. I don't trust any of it.")
objs = [
 {"type": "furniture", "wall": "n", "id": "cabinet", "pos": [0, 0], "size": [3.5, 6, 2], "faces": {"front": "cabinet_front", "top": "dark_top_56x32", "default": "dark_side_32x96"}, "zoom": False},
] + [sprite("n", "dd%d" % i, [-1 + i, 3.2], [0.75, 0.75], "ddial_0", depth=2.06) for i in range(3)] + [
 sprite("n", "dcab_lock", [0, 2.1], [2, 1], "dcab_lock", depth=2.05),
 sprite("n", "dclock", [-5, 10], [3, 3], "dclock_11"),
 sprite("n", "pendulum", [-5, 7.3], [1, 3], "pendulum"),
 {"type": "furniture", "wall": "e", "id": "tdesk", "pos": [-2, 0], "size": [7, 4, 2.5], "faces": {"front": "tdesk_front", "top": "wood_top_112x40", "default": "wood_side_40x64"}, "zoom": False},
 dict(sprite("e", "dnote", [-3.5, 4.6], [2, 1.5], "dnote", depth=1.3), lens_hide=3),
 sprite("e", "ddrawer", [-2, 2], [2, 1.5], "ddrawer", depth=2.56),
 sprite("e", "pinned", [3, 9], [2, 2], "pinned_lens", lens=3),
 sprite("w", "snow_window", [0, 12], [4, 6], "window_snow"),
 sprite("s", "dmirror", [-3, 10], [3, 5], "dmirror"),
 sprite("s", "hdoor", [3.5, 4], [4.5, 8], "door", depth=0.05),
]
puzzles = [
 {"kind": "tick", "flag": "hour", "every": 1, "step": -1, "wrap": 12, "while": "!clock_stopped"},
] + [{"kind": "cycler", "part": "dd%d" % i, "flag": "dd%d" % i, "count": 10, "spin": False, "sfx": "tick", "textures": ["ddial_%d" % k for k in range(10)], "lock": "cab_open"} for i in range(3)] + [
 {"kind": "combo", "flags": ["dd0", "dd1", "dd2"], "code": [4, 3, 8], "commit": "dcab_lock", "lock": "cab_open",
  "fail": [{"sfx": "thunk"}, say("The lock holds. In the dream, it holds very politely.")],
  "do": [{"set": "cab_open"}, {"sfx": "unlock"}, {"give": "candle"}, say("The cabinet's lock gives. There are no sockets in the dream cabinet: only a stub of candle with notches scratched down its side.", 5)]},
]
bindings = [
 bind("dclock", None, {"texture": "dclock_{hour:11}"}),
 tex("pendulum", "clock_stopped", "pendulum_stopped", "pendulum"),
 tex("ddrawer", "drawer_open", "ddrawer_open", "ddrawer"),
]
interactions = [
 tap("pendulum", [{"set": "clock_stopped"}, {"sfx": "tick"}, {"wait": 0.4}, {"set": "drawer_open"}, {"sfx": "slide"}, say("You catch the pendulum. The hands stop at three, and the desk drawer slides open by itself.", 5)], when=["!clock_stopped", "hour=3"]),
 tap("pendulum", [{"set": "clock_stopped"}, {"sfx": "tick"}, say("You catch the pendulum and the hands stop. Nothing else happens.")], when=["!clock_stopped", "!drawer_open"]),
 tap("pendulum", [{"set": "clock_stopped", "value": False}, {"sfx": "tick"}, say("You let it go. It swings, and the hands start back the wrong way.")], when=["clock_stopped", "!drawer_open"]),
 tap("pendulum", [say("Stopped at three.")]),
 tap("dclock", [say("The clock is running backwards: the hour hand goes back one hour every time you do anything.")]),
 tap("dmirror", [{"set": "mirror_seen"}, say("In the mirror, the study is a mess, cold, and there is a man asleep at the desk: you. The clock in the mirror has stopped. Its hand points to the left, at the numeral you'd read as IX if it weren't backwards.", 6)]),
 tap("dnote", [{"set": "note_read"}, say("A neat note in your own hand: SLEEP WELL. 2 2 2. You don't remember writing it. The dream is very tidy.")]),
 tap("pinned", [say("Through dream sight, a scrap pinned to the real wall: 4, then something torn, then 8. MID IS WOKE: the middle one is the hour you woke.", 6)]),
 tap("ddrawer", [say("A desk drawer, shut. It has no keyhole.")], when="!drawer_open"),
 tap("ddrawer", [{"set": "glass_taken"}, {"give": "dream_glass"}, {"sfx": "pickup"}, say("In the drawer: a disc of violet glass, soft as a bubble. Wren's mark on the rim.")], when=["drawer_open", "!glass_taken"]),
 tap("ddrawer", [say("Empty.")]),
 tap("snow_window", [say("Snow on Garrison Street, falling up.")]),
 tap("hdoor", [say("The door opens on the same study, tidier still. There's no way out of a dream through a door.")]),
 tap("cabinet", [say("Wren's cabinet, but with no sockets. A dial lock where the drawer should be.")], handled=False),
 uses("candle", ["dmirror"], [{"set": "left15"}, {"take": "candle"}, {"give": "candle"}, {"complete_room": [16, "THE CELLAR", "You hold the candle to the mirror and the man asleep in it opens his eyes. You step through. There are stairs, going down, under the house, under the dream."]}]),
 tap("dmirror", [say("The candle is lit. The mirror wants it.")], when="item:candle"),
]
interactions.insert(0, interactions.pop())
steps = [
 step("mirror", "mirror_seen", ["The dream is tidy. The truth is somewhere it can't tidy.", "Look in the mirror on the south wall."], [{"set": "mirror_seen"}], "The mirror shows the waking study."),
 step("clock", "drawer_open", ["The clock runs backwards one hour every time you do something. The mirror shows the hour the real clock stopped.",
      "In the mirror the hand points left, but the mirror is backwards: it's three. Count your moves so the hand reaches III, then catch the pendulum."], [{"set": "hour", "value": 3}, {"set": "clock_stopped"}, {"set": "drawer_open"}], "The drawer opens."),
 step("glass", "glass_taken", ["Something is in the desk drawer.", "Take what's in the desk drawer."], [{"give": "dream_glass"}, {"set": "glass_taken"}], "Dream glass."),
 step("lens3", "item:lens3", ["The glass is the third piece of the Lens.", "Put the dream glass and the Lens together in your tray."], [{"take": "dream_glass"}, {"take": "lens2"}, {"give": "lens3"}], "Dream sight."),
 step("cab", "cab_open", ["The note on the desk is the dream's. Dream sight shows another note.", "With the Lens on, read the scrap on the east wall: 4, the hour you woke (3), 8. Set the cabinet's dials to 4 3 8 and press the lock."],
      [{"set": "cab_open"}, {"give": "candle"}], "A candle."),
 step("down", "left15", ["The mirror is the way deeper.", "Use the candle on the mirror."], [{"set": "left15"}, {"complete_room": [16, "THE CELLAR", "Deeper."]}], "Down."),
]
walk = [["shot", "start"], ["tap", "dnote"], ["tap", "dmirror"], ["tap", "snow_window"], ["tap", "dclock"], ["tap", "ddrawer"], ["tap", "hdoor"], ["tap", "dclock"], ["tap", "dmirror"],
 ["expect", "hour=3"], ["tap", "pendulum"], ["expect", "drawer_open"], ["tap", "ddrawer"], ["combine", "dream_glass", "lens2"], ["expect", "item:lens3"],
 ["lens", True], ["shot", "dream_sight"], ["tap", "pinned"], ["lens", False], ["repeat", 4, ["tap", "dd0"]], ["repeat", 3, ["tap", "dd1"]], ["repeat", 8, ["tap", "dd2"]], ["tap", "dcab_lock"], ["expect", "cab_open"],
 ["use", "candle", "dmirror"], ["wait", 2.0]]
room = {"title": "The Study (dreaming)", "walls": "h2_wall_", "floor": "h2_floor", "ceiling": "h2_ceiling", "intro": "Everything is very tidy.",
        "on_enter": [{"set": "hour", "value": 11}, DREAMJ], "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room15_dream.json", room)
print("room15 ok")

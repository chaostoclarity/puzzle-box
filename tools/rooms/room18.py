from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
TEETH = {"a": ("s", [-4, 3]), "b": ("w", [3, 2]), "c": ("n", [4.5, 2]), "d": ("e", [-5.5, 2]), "e": ("d", [3, 10])}
objs = [
 sprite("n", "lens_socket", [0, 6], [6, 2], "lens_socket"),
 sprite("e", "tumbler_panel", [0, 6], [9, 4], "tumbler_panel"),
] + [sprite("e", "tum%d" % i, [-3.5625 + i, 6.5], [0.75, 2], "tumbler_0", depth=0.06) for i in range(8)] + [
 sprite("e", "tumbler_key", [0, 3.5], [1, 1], "tumbler_key", depth=0.06),
 sprite("w", "whisper_mouth", [0, 6], [4, 3], "whisper_mouth"),
 sprite("s", "ninth_door", [0, 5], [4, 6], "ninth_door"),
 sprite("s", "tooth_bin", [4, 2], [1, 1], "tooth_bin", depth=0.05),
] + [sprite(w, "tooth_" + L, pos, [1.25, 1.25], "tooth_" + L, depth=0.06) for L, (w, pos) in TEETH.items()]
bindings = [
 tex("lens_socket", "socket_full", "lens_socket_full", "lens_socket"),
 vis("tumbler_panel", "socket_full"), vis("tumbler_key", ["socket_full", "!tumblers_done"]),
 vis("whisper_mouth", "tumblers_done"),
 tex("whisper_mouth", "hints_burned", "whisper_fed", "whisper_mouth"),
 tex("ninth_door", "hints_burned", "ninth_door_open", "ninth_door"),
] + [vis("tum%d" % i, "socket_full") for i in range(8)] + [
 bind("tum%d" % i, ["any", "held>%d" % i, "given>%d" % (7 - i)], {"texture": "tumbler_1"}, {"texture": "tumbler_0"}) for i in range(8)
] + [vis("tooth_" + L, "!took_" + L) for L in TEETH]
ENDINGS = [
 (["fragments>7"], "THE NINTH SEAL",
  "The door's eye opens and looks at you, and you look back with Wren's nine fragments in your head like a lamp. The cabinet knows them. It knows him. It lets the ninth seal close instead of break.\n\nYou wake on Garrison Street in the spring. The cabinet is a cabinet. In its drawer, a letter in Wren's hand, dated tomorrow: \"Thank you for keeping the rest.\""),
 (["bargains>2", "mercy==0"], "THE VESSEL",
  "The door's eye opens, and the Whisper is behind it, and it has your pages. All the ones you gave it. It reads them back to you in your own voice until you can't tell which of you is reading.\n\nOn Garrison Street, a professor goes back to his lectures. He is very calm now. The landlady says he hums."),
 ([], "THE KEEPER",
  "The door's eye opens and you step through, and the cabinet closes around you like a hand. There is room in here for one keeper. Wren left it empty for you.\n\nSomewhere, a young man carries a black cabinet up three flights of stairs and tells his landlady it is a wardrobe."),
]
interactions = [
 tap("ninth_door", [{"set": "finished"}, {"sfx": "horn"}, {"complete_room": [99, title, text]}], when=["hints_burned"] + c) for c, title, text in ENDINGS
] + [
 tap("ninth_door", [say("A door with an eye in it. The eye is shut.")]),
 tap("lens_socket", [say("A socket in the wood, shaped exactly like the Lens button you use. Not like the Lens: like the button.")], when="!socket_full"),
 tap("lens_socket", [say("Your Lens is in the wall now. You see a little less. You see enough.")]),
 tap("tumbler_panel", [say("Eight brass tumblers in a row, one for each slot of your tray. Under them, eight dots; four are filled: the first three, and the last.")]),
] + [tap("tum%d" % i, [say("Tumbler %d. It's up when slot %d of your tray is full." % (i + 1, i + 1))]) for i in range(8)] + [
 tap("tumbler_key", [{"set": "tumblers_done"}, {"sfx": "unlock"}, {"wait": 0.5}, {"sfx": "whisper"}, say("The tumblers line up with your tray and the key turns. On the west wall, a mouth opens in the wood.", 5)], when=["held==3", "given==1", "!tumblers_done"]),
 tap("tumbler_key", [{"sfx": "thunk"}, say("The key won't turn. The tumblers aren't right.")], when="!tumblers_done"),
 tap("whisper_mouth", [{"ask": ["The Whisper", "\"You have asked me for help with that little word at the corner of your eye. Give it to me. Never ask again, and I will open the last door.\"", ["Give up hints", "Not yet"]]},
                       {"set": "hints_burned"}, {"sfx": "flame"}, {"wait": 0.5}, {"sfx": "creak"}, say("The Hint button burns away at the edge of your sight. The eye in the south door opens.", 5)], when="!hints_burned"),
 tap("whisper_mouth", [say("The mouth is full and quiet.")]),
] + [tap("tooth_" + L, [{"set": "took_" + L}, {"give": "tooth_" + L}, {"sfx": "pickup"}, say("A brass tooth from the cabinet's insides.")]) for L in TEETH] + [
 uses("tooth_" + L, ["tooth_bin"], [{"take": "tooth_" + L}, {"sfx": "click"}, say("The tooth drops into the box and is gone.")]) for L in TEETH] + [
 tap("tooth_bin", [say("A little box in the wall with a slot. It will take anything brass.")]),
]
steps = [
 step("socket", "socket_full", ["The north wall has a socket shaped like something you use, not something you hold.", "Face the north wall and turn your Lens on."], [{"take": "lens3"}, {"set": "socket_full"}, {"lens_off": True}], "The Lens is taken."),
 step("teeth", ["any", "held>2", "tumblers_done"], ["The tumblers follow your tray. Brass teeth are scattered round the cabinet.", "Pick up the brass teeth: one on every wall and one on the floor."], [{"give": "tooth_a"}, {"give": "tooth_b"}, {"give": "tooth_c"}, {"set": "took_a"}, {"set": "took_b"}, {"set": "took_c"}], "Teeth."),
 step("tumblers", "tumblers_done", ["The engraving wants the first three tumblers up and the last. The last is the slot you gave away.", "Hold exactly three things (drop extra teeth in the little box on the south wall), then turn the key."],
      [{"set": "tumblers_done"}], "The key turns."),
 step("burn", "hints_burned", ["The mouth wants the thing you ask it with.", "Touch the mouth and give up your hints."], [{"set": "hints_burned"}], "Done."),
 step("end", "finished", ["The last door is open.", "Go through the door with the eye."], [{"set": "finished"}], "The end."),
]
walk = [["shot", "start"], ["tap", "lens_socket"], ["lens", True], ["wait", 1.0], ["expect", "socket_full"], ["shot", "socket"],
 ["tap", "tooth_a"], ["tap", "tooth_b"], ["tap", "tooth_c"], ["tap", "tooth_d"], ["tap", "tooth_e"], ["tap", "tumbler_key"], ["shot", "tumblers5"],
 ["use", "tooth_d", "tooth_bin"], ["use", "tooth_e", "tooth_bin"], ["tap", "tumbler_key"], ["wait", 1.0], ["expect", "tumblers_done"], ["shot", "tumblers3"],
 ["tap", "whisper_mouth"], ["wait", 1.0], ["expect", "hints_burned"], ["tap", "ninth_door"], ["wait", 3.0]]
room = {"title": "Inside the Cabinet", "walls": "r18_wall_", "floor": "r18_floor", "ceiling": "r18_ceiling", "intro": "It knows you.",
        "lens_socket": {"when": ["facing=n", "!socket_full"], "do": [{"take": "lens3"}, {"set": "socket_full"}, {"lens_off": True}, {"sfx": "lens"}, {"shake": True},
            say("The moment you raise the Lens, the socket pulls it out of your hand and into the wall. The Lens button goes dark. Brass tumblers rise out of the east wall.", 6)]},
        "on_enter": [journal("cabinet", "Inside the cabinet", "I am inside Wren's cabinet. The walls are the wood I carried up three flights. There are sockets everywhere, and none of them are for stones.")],
        "objects": objs, "puzzles": [], "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room18_cabinet.json", room)
print("room18 ok")

from common import *
OUT = "/home/claude/pb-repo/data/rooms/"
def sockets():
    ps = []
    for i in range(9):
        cx, cy = 12 + (i % 3) * 16, 22 + (i // 3) * 20
        ps.append(part("front", [(cx - 28) / 16, (48 - cy) / 16], [0.75, 0.75], "socket_lit", "socket_%d" % (i + 1), depth=0.04, tappable=False))
    ps.append(part("front", [0, -2.4375], [3, 0.5], "cab_drawer", "cab_drawer", depth=0.035))
    return ps

def hub(n):
    first = n == 1
    stone = {1: "seal_stone", 2: "seal_stone2", 3: "seal_stone3", 4: "seal_stone4", 5: "seal_stone5", 6: "seal_stone6", 7: "seal_stone7"}[n]
    pre = "h1_" if first else "h2_"
    objs = [
        {"type": "furniture", "wall": "n", "id": "cabinet", "pos": [0, 0], "size": [3.5, 6, 2],
         "faces": {"front": "cabinet_front", "top": "dark_top_56x32", "default": "dark_side_32x96"},
         "zoom": {"k": 3}, "parts": sockets()},
        {"type": "furniture", "wall": "e", "id": "tdesk", "pos": [-2, 0], "size": [7, 4, 2.5],
         "faces": {"front": "tdesk_front", "top": "wood_top_112x40", "default": "wood_side_40x64"},
         "zoom": {"dy": 1.0, "w": 7.5, "h": 6}},
        sprite("e", "mail", [-3.5, 4.5] if first else [-3.5, 5.0], [2, 1] if first else [3, 2], "mail" if first else "mail_pile", depth=1.3),
        sprite("w", "snow_window", [0, 12], [4, 6], "window_snow"),
        sprite("s", "mirror", [-3, 10], [3, 5], "mirror" if first else "mirror_covered"),
        sprite("s", "hdoor", [3.5, 4], [4.5, 8], "door", depth=0.05),
    ]
    if not first:
        objs.append(sprite("s", "salt", [3.5, 0.25], [6, 0.5], "salt_line", depth=0.3, tappable=False))
    k = str(n)
    placed = "seal%d_placed" % n
    drawer = "drawer%d_open" % n
    if first:
        enter = journal("home1", "Home", "My rooms on Garrison Street. I carried Wren's cabinet up three flights myself and told the landlady it was a wardrobe. It is not heavy. It only feels heavy.")
        place_j = journal("placed1", "The first socket", "The stone went into the top left socket like a tooth going home. The cabinet was warm afterwards. A drawer I had never seen slid open by itself, the way a man might hold out his hand.")
        card = ("SEAL II: THE LIGHT AT KINGSPORT",
                "The postcard is dated in Wren's hand, the week he vanished. You take the morning train to Kingsport and walk the causeway to the light.\n\nThe keeper has not been seen for a month.")
        read_j = journal("postcard", "Kingsport", "A postcard of the Kingsport light, unsent. On the back, in Wren's hand: \"The second is kept where the light goes out to sea. Pike will not give it to you. Do not ask him. E.T., you should stop here.\"\n\nHe knew I would not.")
        next_room = 3
    elif n == 3:
        enter = journal("home3", "Home, the third time", "I do not remember the walk from the sanitarium. The salt by the door has been swept into a careful line, in a hand I recognise as mine. There is a stain on the ceiling the shape of the reef.")
        place_j = journal("placed3", "The third socket", "Three stones. Wren stopped here. The cabinet was warm all night and in the morning the third socket had grown a little lip of black glass around the stone, like a lid closing over an eye.")
        card = ("SEAL III OF IX BROKEN", "Three seals. Wren's three. From here on, no one has gone further.\n\nThe drawer gives you a deed to a farm west of Arkham. You take the road out at first light.")
        next_room = 7
        read_j = journal("farm", "West of Arkham", "In the drawer, a land deed for a farm west of Arkham, the Gardner place, and a pressed flower that has gone the colour of ash. On the deed, in Wren's hand: \"I did not go. Do not go.\"")
    elif n == 4:
        enter = journal("home4", "Home, the fourth time", "The window boxes on Garrison Street have gone grey. Only mine. The landlady has stopped knocking. The cabinet hums a note I can feel in my teeth.")
        place_j = journal("placed4", "The fourth socket", "Four. Past Wren now. The fourth socket did not wait for me to push the stone in; it pulled.")
        card = ("END OF ACT II: DOUBT", "Four seals broken. Five remain.\n\nAct III: Obsession. The drawer holds a ticket for a steamer south, to the ice.\n\nWren's fragments found: {fragments} of 9.{bargains_line}")
        read_j = journal("ticket", "A ticket south", "In the drawer: a steamer ticket to the Antarctic, first class, in my name, paid for. A note pinned to it in Wren's hand: \"The Kingsport Antarctic Survey left a hut on the plateau. The fifth is in the ice under it. I never bought a ticket. Somebody has bought you one.\"")
        next_room = 9
    elif n == 5:
        enter = journal("home5", "Home, the fifth time", "My hands have not warmed since the ice. I sleep in my coat. The cabinet's hum has a second note in it now, under the first, like someone humming along.")
        place_j = journal("placed5", "The fifth socket", "Five. The cabinet took the stone and the room got colder, not warmer. The ice is in the walls now. I can hear the chimes when I close my eyes.")
        card = ("SEAL V OF IX BROKEN", "Five seals broken. Four remain.\n\nThe drawer gives you a key to a sealed wing of the Miskatonic library: the room where the city maps are kept. Maps of a city no one built.\n\nWren's fragments found: {fragments} of 9.{bargains_line}")
        read_j = journal("maps", "The map room", "In the drawer, a library key on a black ribbon and a map of a city drawn in a hand that is almost mine. The streets are too long. The doors are too low. At the bottom: \"The sixth is kept by those who were here before us. They will want something of yours.\"")
        next_room = 11
    elif n == 6:
        enter = journal("home6", "Home, the sixth time", "There is sand in my shoes that I did not bring home. There is sand in the drawer of the cabinet. My tray has an eye in it now, and it watches the cabinet when I sleep.")
        place_j = journal("placed6", "The sixth socket", "Six. The socket was too low, and the stone slid in sideways, the way the keepers walked. Three left. I have stopped telling the landlady anything.")
        card = ("SEAL VI OF IX BROKEN", "Six seals broken. Three remain.\n\nThe drawer holds a concert bill for a street in Paris that is not on any map, and a violinist's name you somehow already know.\n\nWren's fragments found: {fragments} of 9.{bargains_line}")
        read_j = journal("paris", "A street in Paris", "In the drawer, a concert bill, much folded: a recital by a mute violist in a garret at the top of a street I cannot find on any map of Paris. Under it, in Wren's hand: \"The seventh is played, not found. Do not listen to the end.\"")
        next_room = 13
    elif n == 7:
        enter = journal("home7", "Home, the seventh time", "I hum it. I don't mean to. The landlady stopped me on the stair and asked what the tune was, and then she asked me to stop, and then she ran.")
        place_j = journal("placed7", "The seventh socket", "Seven. The cabinet played the street back to me when the stone went in, every note, backwards and forwards at once. Two left. I can't stop now and I don't want to.")
        card = ("END OF ACT III: OBSESSION", "Seven seals broken. Two remain.\n\nAct IV: Madness. The drawer is empty. Then you look again and the drawer is your study, very small, with a very small man asleep at the desk.\n\nWren's fragments found: {fragments} of 9.{bargains_line}")
        read_j = journal("dream", "The drawer", "Inside the drawer, my study, perfect and tiny, and me in it, asleep at the desk. The eighth is there. I have to go to sleep to get it.")
        next_room = 99
    else:
        enter = journal("home2", "Home again", "I have not opened the post in a week. I covered the mirror; I kept seeing the lamp room in it. The landlady asked about the salt by the door and I told her it was for the ice. There is no ice.")
        place_j = journal("placed2", "The second socket", "Two stones now. The cabinet hums when I am out of the room and stops when I come back, like a conversation that falls silent when you enter.\n\nThe drawer opened again.")
        card = ("END OF ACT I: REASON",
                "Two seals broken. Seven remain.\n\nAct II: Doubt. You take the form to Arkham Sanitarium. The night porter reads your name, goes pale, and lets you in without a word. He puts you in the cell the form names.")
        read_j = journal("admission", "Arkham Sanitarium", "A form from the Arkham Sanitarium. Admission of a patient. The name is filled in, in my own hand, in ink that is still wet:\n\nTHORNE, ELIAS.\n\nI have not written it yet.")
        next_room = 5
    bindings = [bind("socket_%d" % i, "seal%d_placed" % i, {"visible": True}, {"visible": False}) for i in range(1, 10)]
    bindings.append(tex("cab_drawer", drawer, "cab_drawer_open", "cab_drawer"))
    interactions = [
        uses(stone, ["cabinet"] + ["socket_%d" % i for i in range(1, 10)] + ["cab_drawer"], [
            {"take": stone}, {"set": placed}, {"sfx": "reveal"}, {"wait": 1.0}, {"set": drawer}, {"sfx": "slide"}, place_j,
            say("The stone fits its socket. A drawer slides open beneath.")]),
        tap("cab_drawer", [say("A drawer with no handle. It doesn't open from outside.")], when="!" + drawer),
        tap("cab_drawer", [{"sfx": "paper"}, read_j, {"set": "hub%d_done" % n}, {"wait": 1.0},
                           {"complete_room": [next_room, card[0], card[1]]}], when=drawer),
        tap("mail", [journal("mail%d" % n, "The post" if first else "More post",
            "A letter from the Dean about my lectures. A bill. A letter from my sister I will answer later." if first else
            "The Dean again, and then the Dean's secretary. Something about my classes being covered. My sister, twice. I will answer them later.")]),
        tap("snow_window", [say("Snow on Garrison Street. A normal street.")]),
        tap("mirror", [say("Your own face. You look tired.") if first else say("You covered it. You remember why.")]),
        tap("hdoor", [say("Not yet. The cabinet isn't finished with you.")]),
        tap("cabinet", [say("Wren's cabinet. Nine sockets.")], when="!" + placed, handled=False),
    ]
    steps = [
        step("place", placed, ["The stone you carried home belongs somewhere in this room.", "Use the stone on Wren's cabinet."],
             [{"take": stone}, {"set": placed}, {"set": drawer}, place_j], "The stone settles into its socket."),
        step("drawer", "hub%d_done" % n, ["The cabinet has offered you something.", "Open the drawer at the bottom of the cabinet."],
             [{"set": "hub%d_done" % n}, read_j, {"complete_room": [next_room, card[0], card[1]]}], "The drawer gives up its paper."),
    ]
    walk = [["shot", "start"], ["use", stone, "cabinet"], ["wait", 1.5], ["shot", "placed"], ["tap", "mail"], ["tap", "cab_drawer"], ["wait", 2.0]]
    room = {"title": "Thorne's Study", "walls": pre + "wall_", "floor": pre + "floor", "ceiling": pre + "ceiling",
            "on_enter": [enter], "objects": objs, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
    J(OUT + "hub%d_thorne.json" % n, room)
hub(1); hub(2); hub(3); hub(4); hub(5); hub(6); hub(7)
print("hubs ok")

from common import *
import math
OUT = "/home/claude/pb-repo/data/rooms/"
W = "ABCD"
def duv(c, r): return [(4 + c * 30 + 14 - 64) / 16, (84 - (4 + r * 32 + 15)) / 16]
ADA_FILE = journal("ada_file", "File: Merrow, Ada", "MERROW, ADA. No. 0417. Ward B. Admitted 1911.\n\nDelusional. Believes herself a \"seeker\" and the hospital a lock. Builds boxes from her bedding and will not say what goes in them.\n\nDischarged to family, 1912.\n\nEffects: one tabulator card, attached.")
YOUR_FILE = journal("thorne_file", "File: Thorne, Elias", "THORNE, ELIAS. No. 0918. Ward D. Admitted November 1928.\n\nFirst observation: the patient opened drawer D-4 and read this line.\n\nThe patient will not let go of a small bone box. He repeats one number over and over: the year Ada Merrow really died. He says the box opens to it.\n\nI checked the date at the top of the page twice. November 1928. It is November 1927.")
LEDGER = journal("ledger", "Admissions ledger", "The porter's admissions ledger, names and numbers:\n\nAshby, Ruth. No. 0122. 1909\nMerrow, Ada. No. 0417. 1911\nKeane, Silas. No. 0583. 1910\nVoss, Hanna. No. 0806. 1912\n\nThe last line is in fresh ink, in my handwriting:\nThorne, Elias. No. 0918. 1928")
CHART = journal("filing", "Filing rules", "On the west wall: FILING. Ward by patient number: A 1 to 250, B 251 to 500, C 501 to 750, D 751 to 1000. Row by the last digit of the year admitted: 1, 5, 9 row 1. 2, 6, 0 row 2. 3, 7 row 3. 4, 8 row 4.")

holes = []
for k in range(10):
    a = math.radians(70 - k * 32)
    holes.append(part("front", [round(1.0 * math.cos(a), 3), round(0.53 + 1.0 * math.sin(a), 3)], [0.5, 0.5], "dial_%d" % k, "dial_%d" % k, depth=0.04))

objs = [
 {"type": "furniture", "wall": "n", "id": "drawers", "pos": [-2.5, 0], "size": [8, 10.5, 2],
  "faces": {"front": "drawers_front", "top": "oak_top_128x32", "default": "oak_side_32x168"}, "zoom": {"k": 2},
  "parts": [part("front", duv(1, 0), [1.75, 2], "drawer_out", "drawer_b1", depth=0.04, tappable=False),
            part("front", duv(3, 3), [1.75, 2], "drawer_out", "drawer_d4", depth=0.04, tappable=False),
            part("front", duv(1, 0), [2.5, 1.5], "ada_stamp", "ada_stamp", depth=0.05, tappable=False, lens=True),
            part("front", [-2, -4.09], [1, 1], "ward_A", "ward_wheel"),
            part("front", [-0.75, -4.09], [1, 1], "row_1", "row_wheel"),
            part("front", [1.75, -4.09], [1.5, 1], "index_lever", "index_lever"),
            part("front", [0, 0.9], [7.5, 8], "clear", "drawer_fronts", depth=0.02)]},
 sprite("n", "row_chart", [4.5, 9], [3, 2], "row_chart"),
 {"type": "furniture", "wall": "e", "id": "cdesk", "pos": [-2.5, 0], "size": [7, 4, 2.5],
  "faces": {"front": "tdesk_front", "top": "wood_top_112x40", "default": "wood_side_40x64"}, "zoom": False},
 sprite("e", "ledger", [-4.5, 4.75], [2.5, 1.5], "ledger", depth=1.3),
 {"type": "box", "name": "lockbox", "wall": "e", "pos": [-1, 4.8], "depth": 1.25, "scale": 0.4, "view": "front", "size": [6, 4, 4],
  "faces": {"front": "lockbox_front", "back": "lockbox_back", "left": "lockbox_side", "right": "lockbox_side", "top": "lockbox_top", "bottom": "lockbox_top"},
  "liner": "lockbox_liner", "liner_skip": ["top"], "hinges": [["top", "top"]], "blocker": "lockbox",
  "parts": [part("front", [0, 0.03], [1, 1.25], "clear", "lb_lock", depth=0.04)],
  "children": [{"name": "thim_mini", "faces": {"front": "thim_front", "back": "thim_back", "left": "thim_side", "right": "thim_side", "top": "thim_top", "bottom": "thim_top"},
                "liner": "thim_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "dive:thimble", "scale": 0.3, "pos": [0, -1.0, 0]}]},
 {"type": "stage_box", "name": "thimble", "view": "front",
  "faces": {"front": "thim_front", "back": "thim_back", "left": "thim_side", "right": "thim_side", "top": "thim_top", "bottom": "thim_top"},
  "liner": "thim_liner", "liner_skip": ["front"], "hinges": [["front", "bottom"]], "blocker": "thimble",
  "parts": [part("front", [0, 0.4], [4.5, 4.5], "nring_0", "nring_0", tappable=False),
            part("front", [0, 0.4], [3.25, 3.25], "nring_1", "nring_1", depth=0.04, tappable=False),
            part("front", [0, 0.4], [2, 2], "nring_2", "nring_2", depth=0.05, tappable=False),
            part("front", [0, 0.4], [4.5, 4.5], "clear", "nrings", depth=0.065),
            part("front", [2.3, -2.3], [0.75, 0.75], "thim_pin", "thim_pin", depth=0.04)],
  "inner_sprites": [{"id": "seal3_part", "tex": "item_seal_stone3", "size": [1.5, 1.5], "pos": [0, -1.5, -1.0]}]},
 sprite("s", "ward_rules", [-3, 10], [5, 6], "ward_rules"),
 sprite("s", "grille", [-3, 10], [5, 6], "grille_overlay", depth=0.05, tappable=False),
 sprite("s", "rec_door", [3.5, 4.5], [4.5, 9], "rec_door"),
 sprite("w", "filing_chart", [-3.5, 11], [4, 5], "filing_chart"),
 {"type": "furniture", "wall": "w", "id": "phone", "pos": [3, 7], "size": [3, 4, 1],
  "faces": {"front": "phone_front", "default": "wood_side_16x64"}, "zoom": {"k": 4}, "parts": holes},
 sprite("u", "tube", [0, 7.5], [3, 3], "clear", depth=0.02),
 sprite("u", "capsule", [0, 7.5], [1, 1.5], "capsule", depth=0.05),
 sprite("d", "floor_files", [0, 7.5], [6, 6], "clear", depth=0.02),
]

OTHER = [{"sfx": "slide"}, say("The drawer slides out: files on strangers. None of them yours, none of them Ada's. It slides back.")]
puzzles = [
 {"kind": "cycler", "part": "ward_wheel", "flag": "ward", "count": 4, "spin": False, "sfx": "tick", "textures": ["ward_" + c for c in W]},
 {"kind": "cycler", "part": "row_wheel", "flag": "row", "count": 4, "spin": False, "sfx": "tick", "textures": ["row_%d" % i for i in range(1, 5)]},
 {"kind": "combo", "flags": ["ward", "row"], "code": [1, 0], "commit": "index_lever", "fail": OTHER,
  "do": [{"sfx": "slide"}, {"set": "b1_open"}, {"give": "punch_card"}, ADA_FILE, say("Drawer B-1 slides out: Ada Merrow's file, and a punched card. It's in your journal.", 5)]},
 {"kind": "combo", "flags": ["ward", "row"], "code": [3, 3], "commit": "index_lever", "fail": OTHER,
  "do": [{"sfx": "slide"}, {"set": "d4_open"}, {"wait": 0.4}, {"sfx": "whisper", "db": -8}, YOUR_FILE, say("Drawer D-4. A file with your name on it. It's in your journal.", 5)]},
 {"kind": "sequence", "flag": "dialed_digits", "order": "206", "silent": True, "lock": "dialed", "pulled_suffix": "_lit",
  "parts": {"dial_%d" % k: str(k) for k in range(10)}, "tex": {"dial_%d" % k: "dial_%d" % k for k in range(10)},
  "fail": [{"sfx": "click"}, say("The line clicks and goes dead.")],
  "do": [{"set": "dialed"}, {"sfx": "hum"}, {"wait": 1.0}, say("A voice on the line says your name, very slowly. Then a thump overhead: something has dropped into the tube in the ceiling.", 6), {"sfx": "thunk"}, {"set": "capsule_dropped"}]},
 {"kind": "pickup", "part": "capsule", "item": "lockbox_key", "flag": "capsule_taken", "show_if": "capsule_dropped",
  "then": [say("A brass message capsule. Inside: a steel key tagged PATIENT EFFECTS.")]},
 {"kind": "radial", "part": "nrings", "rotate": -36, "count": 10, "lock": "thimble_open",
  "rings": [["nring_2", 1.0], ["nring_1", 1.625], ["nring_0", 2.25]]},
 {"kind": "combo", "flags": ["nring_0", "nring_1", "nring_2"], "code": [9, 1, 3], "commit": "thim_pin", "lock": "thimble_open",
  "fail": [{"sfx": "thunk"}, say("You press the pin. The bone box stays shut.")],
  "do": [{"set": "thimble_open"}, {"sfx": "unlock"}, say("Nineteen thirteen. The pin sinks in, and the bone box opens.")]},
 {"kind": "pickup", "part": "seal3_part", "item": "seal_stone3", "flag": "seal3_taken", "show_if": "thimble_open", "sfx": "reveal",
  "then": [{"take": "punch_card"}, journal("seal3", "The third seal", "The third stone was in Ada's bone box, where her heart should have been kept. Wren's three are done. Everything after this, no one living has seen.\n\nThe file says I will be here next November. I will make sure I am not."),
           {"wait": 1.2}, {"complete_room": [103, "SEAL III OF IX", "You walk out past the porter's empty chair with the stone in your fist. Nobody stops you. Nobody, you realise, ever stopped Ada either.\n\nYou carry the stone home."]}]},
]

bindings = [
 bind("drawer_b1", "b1_open", {"visible": True}, {"visible": False}),
 bind("drawer_d4", "d4_open", {"visible": True}, {"visible": False}),
 bind("ada_stamp", "b1_open", {"gone": False}, {"gone": True}),
 bind("grille", "grille_on", {"visible": True}, {"visible": False}),
 bind("hinge:lockbox.top", "lockbox_open", {"hinge": 110}, {"hinge": 0}, anim=1.0),
 bind("box:lockbox", "lockbox_open", {"tappable": False}, {"tappable": True}),
 bind("hinge:thimble.front", "thimble_open", {"hinge": 100}, {"hinge": 0}, anim=0.9),
 bind("hinge:thim_mini.front", "thimble_open", {"hinge": 100}, {"hinge": 0}),
 bind("box:thimble", "thimble_open", {"tappable": False}, {"tappable": True}),
]

interactions = [
 tap("ledger", [{"set": "ledger_read"}, {"sfx": "paper"}, LEDGER, say("The admissions ledger. The last line is in your handwriting. It's in your journal.", 5)]),
 tap("filing_chart", [{"set": "chart_read"}, CHART, say("Filing rules. They're in your journal.")]),
 tap("row_chart", [CHART, say("Which row a file goes in, by the year. It's in your journal.")]),
 tap("drawer_fronts", [say("Sixteen drawers, A to D across, 1 to 4 down. All locked. The index below picks one.")]),
 tap("ward_rules", [say("RULES OF THE WARD. Nothing in it seems to matter.")], when="!grille_on"),
 tap("ward_rules", [say("Through the card's holes: E, X, T, then 2, 0, 6.")]),
 uses("punch_card", ["ward_rules", "grille"], [{"set": "grille_on"}, {"sfx": "paper"}, journal("grille", "The punched card", "Laid over the Rules of the Ward, the card's six holes pick out six characters: E X T 2 0 6."),
      say("You lay the card over the rules. Six holes, six characters: E X T 2 0 6.", 6)]),
 tap("rec_door", [say("The way back to the cell. It's locked now, from this side.")]),
 tap("tube", [say("A pneumatic tube. Messages used to fall out of it.")], when="!capsule_dropped"),
 tap("tube", [say("The tube's mouth.")]),
 tap("floor_files", [say("Boxes of old files stacked on the floor. Water-stained, illegible.")]),
 tap("lift:lockbox", [], when="!item:lockbox_key", handled=False),
 tap("lb_lock", [say("A steel keyhole. PATIENT EFFECTS.")], when="!lockbox_open"),
 use("lockbox_key", "lb_lock", [{"take": "lockbox_key"}, {"set": "lockbox_open"}, {"sfx": "unlock"}, {"face": "top"},
      say("The lid comes up. Inside, a small box made of bone.")]),
]

steps = [
 step("ledger", "ledger_read", ["Someone keeps a record of who comes in.", "Read the admissions ledger on the desk (east wall)."], [{"set": "ledger_read"}, LEDGER], "The ledger is in your journal."),
 step("chart", "chart_read", ["The files are kept by a system.", "Read the filing rules on the west wall."], [{"set": "chart_read"}, CHART], "The rules are in your journal."),
 step("ada", "b1_open", ["Ada's number and year, put through the filing rules, give a drawer.", "Ada is No. 0417 (ward B), admitted 1911 (row 1). Set the index to B and 1, then pull the lever."],
      [{"set": "ward", "value": 1}, {"set": "row", "value": 0}, {"set": "b1_open"}, {"give": "punch_card"}, ADA_FILE], "Drawer B-1 opens."),
 step("grille", "grille_on", ["Ada's card has six holes. Something in the room has the right shape to read through it.", "Use the punched card on the Rules of the Ward (south wall)."],
      [{"set": "grille_on"}], "The card picks out E X T 2 0 6."),
 step("dial", "dialed", ["EXT 206 is an extension.", "On the telephone (west wall), dial 2, 0, 6."], [{"set": "dialed"}, {"set": "capsule_dropped"}], "Something drops into the ceiling tube."),
 step("capsule", "capsule_taken", ["Something dropped into the pneumatic tube.", "Look up and take the capsule from the tube in the ceiling."], [{"give": "lockbox_key"}, {"set": "capsule_taken"}], "The effects key is yours."),
 step("lockbox", "lockbox_open", ["The EFFECTS box on the desk is locked.", "Lift the box on the desk and use the effects key on it."], [{"take": "lockbox_key"}, {"set": "lockbox_open"}], "The lid comes up."),
 step("yours", "d4_open", ["The ledger's last line is your own name. Your file is in the drawers too.", "You are No. 0918 (ward D), admitted 1928 (row 4). Set D and 4 and pull the lever."],
      [{"set": "ward", "value": 3}, {"set": "row", "value": 3}, {"set": "d4_open"}, YOUR_FILE], "Drawer D-4 opens."),
 step("thimble", "thimble_open", ["Your file says the bone box opens to the year Ada Merrow really died. Her file says one thing. The Lens may say another.",
      "Through the Lens, drawer B-1 is stamped DIED IN CARE 1913. Dive into the bone box, set the rings to 9, 1, 3 from the outside in, and press the pin."],
      [{"set": "nring_0", "value": 9}, {"set": "nring_1", "value": 1}, {"set": "nring_2", "value": 3}, {"set": "thimble_open"}], "The bone box opens."),
 step("seal", "seal3_taken", ["The bone box holds the third seal.", "Take the stone from the bone box."],
      [{"give": "seal_stone3"}, {"set": "seal3_taken"}, {"complete_room": [103, "SEAL III OF IX", "You carry the stone home."]}], "The third seal is yours."),
]

walk = [["shot", "start"], ["tap", "ledger"], ["tap", "filing_chart"], ["tap", "row_chart"],
 ["tap", "index_lever"], ["shot", "drawers"], ["tap", "ward_wheel"], ["tap", "index_lever"], ["expect", "b1_open"],
 ["lens", True], ["shot", "ada_stamp"], ["lens", False],
 ["use", "punch_card", "ward_rules"], ["shot", "grille"], ["expect", "grille_on"],
 ["tap", "dial_2"], ["tap", "dial_1"], ["tap", "dial_9"], ["shot", "phone"], ["tap", "dial_2"], ["tap", "dial_0"], ["tap", "dial_6"], ["wait", 2.0], ["expect", "capsule_dropped"],
 ["tap", "capsule"], ["shot", "ceiling"], ["expect", "capsule_taken"],
 ["tap", "lockbox"], ["use", "lockbox_key", "lb_lock"], ["wait", 1.0], ["shot", "lockbox_open"],
 ["repeat", 2, ["tap", "ward_wheel"]], ["repeat", 3, ["tap", "row_wheel"]], ["tap", "index_lever"], ["expect", "d4_open"], ["shot", "your_file"],
 ["tap", "dive:thimble"], ["shot", "thimble"],
 ["repeat", 5, ["tapat", "nrings", [0, 2.0]]], ["repeat", 4, ["tapat", "nrings", [0, 1.35]]], ["repeat", 3, ["tapat", "nrings", [0, 0.4]]],
 ["shot", "rings_set"], ["tap", "thim_pin"], ["wait", 1.2], ["expect", "thimble_open"], ["tap", "seal3_part"], ["wait", 3.0]]

room = {"title": "Records", "walls": "r6_wall_", "floor": "r6_floor", "ceiling": "r6_ceiling",
        "on_enter": [{"set": "nring_0", "value": 4}, {"set": "nring_1", "value": 7}, {"set": "nring_2", "value": 0},
          journal("records", "Records", "The sanitarium's records room. A wall of locked case-file drawers, a clerk's desk, a telephone, and the smell of wet paper. The porter's chair is still warm.")],
        "objects": objs, "puzzles": puzzles, "bindings": bindings, "interactions": interactions, "steps": steps, "walkthrough": walk}
J(OUT + "room6_records.json", room)
print("room6 ok")

## Seal 1, room 1: Hollis Wren's study, Miskatonic University.
## Act I, Reason: this room is honest. Every clue means what it says.
## Chain: letter (the hour) -> wall clock -> brass key. Walnut box: back plaque -> dials -> iron key.
## Iron key -> desk drawer -> matches + photograph. Matches -> lamp -> east wall lit.
## Photograph (book order) -> bookshelf -> signet ring. Brass key -> walnut box lid -> nested box.
## Ring -> wax seal -> door key -> door.
extends "res://scripts/room.gd"

const SYMS := ["sun", "moon", "star", "eye"]
const CODE := [1, 3, 2]          # moon, eye, star: engraved on the walnut box's back
const BOOK_ORDER := "gbr"        # green, blue, red: inked on the photograph
const BOOKS := {"g": "green", "b": "blue", "r": "red"}

var walnut: PixelBox
var mini: PixelBox
var inner: PixelBox
var lamp: MeshInstance3D
var glow: MeshInstance3D
var panel_y := 0.0


func build() -> void:
	title = "Wren's Study"
	build_walls("r1_wall_")
	_build_north()
	_build_east()
	_build_south()
	_build_west()
	_build_walnut()
	_define_steps()


func _build_north() -> void:
	var desk := add_furniture("n", "desk", Vector2(0, 0), Vector3(7, 3.5, 3),
		{"front": tex("desk_front"), "top": tex("wood_top_112x48"), "default": tex("wood_side_48x56")},
		{"dy": 1.8, "w": 7.6, "h": 7.0})
	desk.add_part("front", Vector2(0, 0.9), Vector2(3, 1), tex("drawer"), "drawer", 0.02)
	desk.add_part("front", Vector2(-0.6, 1.2), Vector2(0.75, 0.5), tex("drawer_matches"), "drawer_matches", 0.03)
	desk.add_part("front", Vector2(0.6, 1.2), Vector2(0.75, 0.5), tex("drawer_photo"), "drawer_photo", 0.03)

	var clock := add_furniture("n", "clock", Vector2(-5.2, 7), Vector3(2, 4, 1),
		{"front": tex("clock_front"), "default": tex("dark_side_32x96")}, {})
	clock.add_part("front", Vector2(0, 0.875), Vector2(1, 1), tex("clock_hand"), "clock_hand", 0.04)
	clock.add_part("front", Vector2(0, -1.375), Vector2(0.75, 0.5), tex("small_brass_key"), "clock_key", 0.025)
	clock.add_part("front", Vector2(0, -1.375), Vector2(1.25, 1), tex("clock_door"), "clock_door", 0.035)

	lamp = add_sprite("n", "lamp", Vector2(2.6, 4.75), Vector2(1.5, 2.5), "lamp", 1.6)
	glow = PixelBox.quad(Vector2(4, 4), tex("glow"))
	var gm := StandardMaterial3D.new()
	gm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	gm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	gm.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	gm.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	gm.albedo_texture = tex("glow")
	glow.material_override = gm
	glow.position = Vector3(2.6, 5.3, -HALF + 1.5)
	groups["n"].add_child(glow)
	add_sprite("n", "letter", Vector2(1.0, 4.0), Vector2(1.25, 1), "letter", 2.3)
	add_sprite("n", "diploma", Vector2(3.6, 10), Vector2(4, 3), "diploma")


func _build_east() -> void:
	var shelf := add_furniture("e", "bookshelf", Vector2(-2, 0), Vector3(8, 13, 1.5),
		{"front": tex("bookshelf"), "top": tex("wood_top_128x24"), "default": tex("wood_side_24x208")},
		{"k": 2, "dx": 0.6, "dy": -0.6, "w": 8, "h": 9})
	var xs := {"b": -0.875, "r": -0.125, "g": 0.625}
	for k in xs:
		shelf.add_part("front", Vector2(xs[k], -0.094), Vector2(0.5, 2), tex("book_" + BOOKS[k]), "book_" + BOOKS[k], 0.03)
	shelf.add_part("front", Vector2(2.5, -0.3), Vector2(0.75, 0.75), tex("small_ring"), "ring_part", 0.025)
	shelf.add_part("front", Vector2(2.5, -0.28), Vector2(1.5, 1.5), tex("compartment"), "compartment", 0.035)
	add_sprite("e", "globe", Vector2(4.8, 1.5), Vector2(2, 3), "globe", 0.8)


func _build_south() -> void:
	add_sprite("s", "door", Vector2(-2.5, 4), Vector2(4.5, 8), "door", 0.05)
	add_sprite("s", "sampler", Vector2(-2.5, 10.5), Vector2(3, 2), "sampler")
	add_sprite("s", "coatrack", Vector2(3.5, 3), Vector2(1.5, 6), "coatrack", 0.5)


func _build_west() -> void:
	add_sprite("w", "window", Vector2(-3.5, 9), Vector2(4, 8), "window")
	add_sprite("w", "portrait", Vector2(3.2, 10.6), Vector2(4, 5), "portrait")
	add_furniture("w", "cabinet", Vector2(3.2, 0), Vector3(3.5, 6, 2),
		{"front": tex("cabinet_front"), "top": tex("dark_top_56x32"), "default": tex("dark_side_32x96")}, {})


func _build_walnut() -> void:
	walnut = PixelBox.new()
	groups["n"].add_child(walnut)
	walnut.build({"front": tex("outer_front"), "back": tex("outer_back"), "left": tex("outer_left"),
		"right": tex("outer_right"), "top": tex("outer_top"), "bottom": tex("outer_bottom")}, 6.0, tex("liner"))
	walnut.hinge_face("top", "top")
	walnut.blocker.set_meta("id", "walnut")
	walnut.add_part("front", Vector2(0, -1.2), Vector2(1.5, 1.5), tex("lock"), "walnut_lock")
	for i in 3:
		walnut.add_part("left", Vector2((i - 1) * 1.6, 0), Vector2(1.25, 1.25), tex("dial_sun"), "dial%d" % i)
	walnut.add_part("right", Vector2(0, -0.5), Vector2(1.5, 1.5), tex("item_iron_key"), "iron_key_part", 0.015)
	var panel := walnut.add_part("right", Vector2(0, -0.5), Vector2(2, 2), tex("panel"), "panel", 0.03)
	panel_y = panel.position.y

	mini = PixelBox.new()
	walnut.add_child(mini)
	mini.build(_inner_faces(), 6.0, tex("liner"))
	mini.hinge_face("top", "top")
	mini.blocker.set_meta("id", "dive:walnut_inner")
	mini.add_part("top", Vector2.ZERO, Vector2(1.5, 1.5), tex("wax_seal"), "mini_wax", 0.03, false)
	mini.scale = Vector3.ONE * 0.4
	mini.position = Vector3(0, -3.0 + 1.2 + 0.06, 0)

	walnut.scale = Vector3.ONE * 0.5
	walnut.position = Vector3(-1.9, 3.5 + 1.5, -HALF + 1.6)
	register_box("walnut", walnut)

	inner = PixelBox.new()
	inner.build(_inner_faces(), 6.0, tex("liner"))
	inner.hinge_face("top", "top")
	inner.blocker.set_meta("id", "walnut_inner")
	inner.add_part("top", Vector2.ZERO, Vector2(1.5, 1.5), tex("wax_seal"), "wax", 0.03)
	var k := PixelBox.quad(Vector2(1.5, 1.5), tex("item_door_key"))
	k.transform = Transform3D(Basis(Vector3.RIGHT, -PI / 2), Vector3(0, -2.85, 0))
	PixelBox.add_body(k, Vector2(1.5, 1.5), "door_key_part")
	inner.add_child(k)
	add_stage_box("walnut_inner", inner, "top")


func _inner_faces() -> Dictionary:
	return {"front": tex("inner_front"), "back": tex("inner_back"), "left": tex("inner_left"),
		"right": tex("inner_right"), "top": tex("inner_top"), "bottom": tex("inner_bottom")}


func _part(id: String) -> MeshInstance3D:
	return ids[id]


# ---------------- steps: hints, bargains, walkthrough ----------------

func _define_steps() -> void:
	steps = [
		{"id": "letter", "done": func(): return State.has("letter_read"),
			"hints": ["Wren left something for you on his desk.", "Read the letter propped by the lamp on the desk (north wall)."],
			"solve": func(): _read_letter(), "said": "The letter unfolds itself on the desk."},
		{"id": "clock", "done": func(): return State.has("clock_open"),
			"hints": ["Wren's letter names an hour.", "Tap the wall clock's hand until it points to three."],
			"solve": func():
				State.set_flag("clock_hour", 3)
				State.set_flag("clock_open"),
			"said": "The clock's hand creeps round to three on its own."},
		{"id": "brass", "done": func(): return State.has("brass_taken"),
			"hints": ["The clock opened a little door.", "Take the brass key from the base of the wall clock."],
			"solve": func(): _take("brass_key", "brass_taken"), "said": "The brass key is in your pocket. You don't remember taking it."},
		{"id": "dials", "done": func(): return State.has("panel_open"),
			"hints": ["The walnut box has a plaque on one face and dials on another.", "Turn the box's dials to moon, eye, star (left to right), as the back plaque shows."],
			"solve": func():
				for i in 3:
					State.set_flag("dial%d" % i, CODE[i])
				State.set_flag("panel_open"),
			"said": "The dials turn themselves. A panel slides open."},
		{"id": "iron", "done": func(): return State.has("iron_taken"),
			"hints": ["A panel on the walnut box slid open.", "Take the iron key from behind the walnut box's sliding panel."],
			"solve": func(): _take("iron_key", "iron_taken"), "said": "The iron key is in your hand."},
		{"id": "drawer", "done": func(): return State.has("drawer_open"),
			"hints": ["Something on the desk is locked.", "Use the iron key on the desk drawer."],
			"solve": func():
				State.remove_item("iron_key")
				State.set_flag("drawer_open"),
			"said": "The desk drawer slides open."},
		{"id": "drawer_items", "done": func(): return State.has("matches_taken") and State.has("photo_taken"),
			"hints": ["The drawer has things in it.", "Take the matches and the photograph from the desk drawer."],
			"solve": func():
				_take("matches", "matches_taken")
				_take("photo", "photo_taken"),
			"said": "Matches and a photograph, in your pocket."},
		{"id": "lamp", "done": func(): return State.has("lamp_lit"),
			"hints": ["One wall of the study is too dark to see.", "Use the matches on the oil lamp on the desk."],
			"solve": func():
				State.remove_item("matches")
				State.set_flag("lamp_lit"),
			"said": "The lamp catches. The east wall comes out of the dark."},
		{"id": "books", "done": func(): return State.has("comp_open"),
			"hints": ["Hold the photograph to examine it. Someone numbered three books.", "In the bookshelf, pull the green book, then the blue, then the red."],
			"solve": func():
				State.set_flag("books", BOOK_ORDER)
				State.set_flag("comp_open"),
			"said": "Three books slide out. A panel in the shelf opens."},
		{"id": "ring", "done": func(): return State.has("ring_taken"),
			"hints": ["A compartment in the bookshelf is open.", "Take the ring from the bookshelf compartment."],
			"solve": func(): _take("ring", "ring_taken"), "said": "Wren's ring is on your finger. It fits too well."},
		{"id": "box_lock", "done": func(): return State.has("box_unlocked"),
			"hints": ["The walnut box has a keyhole on its front.", "Use the small brass key on the walnut box's lock."],
			"solve": func():
				State.remove_item("brass_key")
				State.set_flag("box_unlocked"),
			"said": "The walnut box unlocks and its lid rises."},
		{"id": "wax", "done": func(): return State.has("wax_broken"),
			"hints": ["Inside the walnut box is a smaller box, sealed with a W.", "Look inside the walnut box, touch the small box, and press the signet ring into its wax."],
			"solve": func():
				State.remove_item("ring")
				State.set_flag("wax_broken"),
			"said": "The wax splits. The small box opens."},
		{"id": "door_key", "done": func(): return State.has("door_key_taken"),
			"hints": ["The small box held something.", "Take the key from inside the small box."],
			"solve": func(): _take("door_key", "door_key_taken"), "said": "The door key is cold in your hand."},
		{"id": "door", "done": func(): return State.has("door_open"),
			"hints": ["You have what you need to leave.", "Use the door key on the study door (south wall)."],
			"solve": func(): await _open_door(), "said": "The door opens."},
	]

	walkthrough = [
		["shot", "start"],
		["tap", "letter"], ["shot", "letter"],
		["tap", "clock"], ["shot", "clock_zoom"], ["back"],
	]
	for i in 8:
		walkthrough.append(["tap", "clock_hand"])
	walkthrough += [
		["shot", "clock_open"], ["tap", "clock_key"], ["expect", "brass_taken"],
		["tap", "desk"], ["shot", "desk_zoom"], ["back"],
		["tap", "walnut"], ["shot", "box_front"], ["face", "back"], ["shot", "box_back"],
		["tap", "dial0"], ["tap", "dial1"], ["tap", "dial1"], ["tap", "dial1"], ["tap", "dial2"], ["tap", "dial2"],
		["wait", 1.0], ["shot", "box_panel_open"], ["expect", "panel_open"], ["tap", "iron_key_part"], ["back"],
		["tap", "bookshelf"], ["shot", "east_dark"], ["back"],
		["use", "iron_key", "drawer"], ["tap", "drawer_matches"], ["tap", "drawer_photo"],
		["examine", "photo"],
		["use", "matches", "lamp"], ["shot", "lamp_lit"],
		["tap", "book_green"], ["tap", "book_red"], ["wait", 1.0],
		["tap", "book_green"], ["tap", "book_blue"], ["tap", "book_red"], ["wait", 0.8],
		["shot", "shelf_open"], ["tap", "ring_part"], ["expect", "ring_taken"],
		["tap", "cabinet"], ["shot", "west"], ["back"], ["tap", "portrait"],
		["use", "brass_key", "walnut_lock"], ["wait", 2.5], ["shot", "box_open"],
		["tap", "dive:walnut_inner"], ["shot", "inner_box"],
		["use", "ring", "wax"], ["wait", 1.5], ["shot", "inner_open"],
		["tap", "door_key_part"], ["expect", "door_key_taken"], ["back"], ["back"],
		["journal"],
		["swipe", 80.0], ["swipe", 80.0], ["shot", "south_by_swipe"],
		["hint"], ["shot", "hint1"], ["hint"], ["hint"],
	]


func _take(item: String, flag: String) -> void:
	State.add_item(item)
	State.set_flag(flag)


# ---------------- state -> visuals ----------------

func apply_state() -> void:
	var hour: int = State.flag_value("clock_hour", 7)
	_part("clock_hand").rotation.z = -hour * PI / 6
	PixelBox.set_texture(_part("clock_door"), tex("clock_door_open" if State.has("clock_open") else "clock_door"))
	PixelBox.set_tappable(_part("clock_door"), not State.has("clock_open"))
	_part("clock_key").visible = State.has("clock_open") and not State.has("brass_taken")
	PixelBox.set_tappable(_part("clock_key"), _part("clock_key").visible)

	for i in 3:
		PixelBox.set_texture(_part("dial%d" % i), tex("dial_" + SYMS[int(State.flag_value("dial%d" % i, 0))]))
	_part("panel").position.y = panel_y + (2.0 if State.has("panel_open") else 0.0)
	PixelBox.set_tappable(_part("panel"), not State.has("panel_open"))
	_part("iron_key_part").visible = not State.has("iron_taken")
	PixelBox.set_tappable(_part("iron_key_part"), State.has("panel_open") and not State.has("iron_taken"))

	var dopen := State.has("drawer_open")
	PixelBox.set_texture(_part("drawer"), tex("drawer_open" if dopen else "drawer"))
	PixelBox.set_tappable(_part("drawer"), not dopen)
	for pair in [["drawer_matches", "matches_taken"], ["drawer_photo", "photo_taken"]]:
		var show := dopen and not State.has(pair[1])
		_part(pair[0]).visible = show
		PixelBox.set_tappable(_part(pair[0]), show)

	var lit := State.has("lamp_lit")
	PixelBox.set_texture(lamp, tex("lamp_lit" if lit else "lamp"))
	glow.visible = lit
	set_wall_dim("e", 1.0 if lit else 0.25)

	var pulled: String = State.flag_value("books", "")
	for k in BOOKS:
		PixelBox.set_texture(_part("book_" + BOOKS[k]), tex("book_%s%s" % [BOOKS[k], "_pulled" if k in pulled else ""]))
	PixelBox.set_texture(_part("compartment"), tex("compartment_open" if State.has("comp_open") else "compartment"))
	PixelBox.set_tappable(_part("compartment"), not State.has("comp_open"))
	_part("ring_part").visible = State.has("comp_open") and not State.has("ring_taken")
	PixelBox.set_tappable(_part("ring_part"), _part("ring_part").visible)

	var unlocked := State.has("box_unlocked")
	PixelBox.set_texture(_part("walnut_lock"), tex("lock_open" if unlocked else "lock"))
	walnut.set_hinge("top", 115.0 if unlocked else 0.0)
	PixelBox.set_tappable(walnut.blocker, not unlocked)

	var broken := State.has("wax_broken")
	for w in ["wax", "mini_wax"]:
		PixelBox.set_texture(_part(w) if ids.has(w) else _mini_wax(), tex("wax_broken" if broken else "wax_seal"))
	inner.set_hinge("top", 115.0 if broken else 0.0)
	mini.set_hinge("top", 115.0 if broken else 0.0)
	PixelBox.set_tappable(inner.blocker, not broken)
	var key: Node3D = _part("door_key_part")
	key.visible = not State.has("door_key_taken")
	PixelBox.set_tappable(key, broken and not State.has("door_key_taken"))

	PixelBox.set_texture(_part("door"), tex("door_open" if State.has("door_open") else "door"))


func _mini_wax() -> MeshInstance3D:
	for c in mini.faces["top"].get_children():
		if c.get_meta("id", "") == "mini_wax":
			return c
	return null


# ---------------- taps ----------------

func on_tap(id: String, node: Node) -> bool:
	var dark_east := not State.has("lamp_lit") and wall_of(node) == "e"
	if dark_east:
		game.say("Too dark to make anything out over here.")
		return true
	match id:
		"letter":
			_read_letter()
			return true
		"clock_hand":
			if State.has("clock_open"):
				game.say("The clock has given up its secret.")
				return true
			var h: int = int(State.flag_value("clock_hour", 7)) % 12 + 1
			State.set_flag("clock_hour", h)
			game.play("tick")
			var tw := create_tween()
			tw.tween_property(node, "rotation:z", -h * PI / 6, 0.15)
			if h == 3:
				await tw.finished
				State.set_flag("clock_open")
				game.play("unlock")
				apply_state()
				game.say("Three. A little door in the clock's case clicks open.")
			return true
		"clock_door":
			if not State.has("clock_open"):
				game.shake(node)
				game.say("A small door in the clock case. It won't open.")
			return true
		"clock_key":
			_take("brass_key", "brass_taken")
			game.play("pickup")
			apply_state()
			game.say("A small brass key.")
			return true
		"dial0", "dial1", "dial2":
			await _turn_dial(int(id.substr(4)), node)
			return true
		"panel":
			game.shake(node)
			game.say("A sliding panel. It's locked in place.")
			return true
		"iron_key_part":
			_take("iron_key", "iron_taken")
			game.play("pickup")
			apply_state()
			game.say("An iron key. The bow is stamped with a drawer pull.")
			return true
		"walnut_lock":
			if not State.has("box_unlocked"):
				game.shake(node)
				game.say("A brass keyhole, very small.")
			return true
		"drawer":
			if not State.has("drawer_open"):
				game.shake(node)
				game.say("The desk drawer is locked. Iron, by the look of the keyhole.")
			return true
		"drawer_matches":
			_take("matches", "matches_taken")
			game.play("pickup")
			apply_state()
			game.say("A box of matches.")
			return true
		"drawer_photo":
			_take("photo", "photo_taken")
			game.play("paper")
			apply_state()
			State.add_journal("photo", "A photograph", "Wren at his own bookshelf, younger. Someone has inked numbers over three of the books: 1, 2, 3.")
			game.say("A photograph. Hold it in your tray to look closer.")
			return true
		"lamp":
			game.say("The flame leans toward you." if State.has("lamp_lit") else "An oil lamp, cold. There's still oil in it.")
			return true
		"book_green", "book_blue", "book_red":
			await _pull_book(id.substr(5, 1), node)
			return true
		"compartment":
			if not State.has("comp_open"):
				game.say("A square panel, flush with the shelf. No handle.")
			return true
		"ring_part":
			_take("ring", "ring_taken")
			game.play("pickup")
			apply_state()
			State.add_journal("ring", "Wren's ring", "His signet ring, hidden in his own bookshelf. A W cut into the bezel. It fits my finger exactly.")
			game.say("Wren's signet ring.")
			return true
		"wax":
			if not State.has("wax_broken"):
				game.say("Red wax, stamped with a W.")
			return true
		"door_key_part":
			_take("door_key", "door_key_taken")
			game.play("pickup")
			apply_state()
			game.say("A black iron key. The study door's, surely.")
			return true
		"door":
			if not State.has("door_open"):
				game.shake(node)
				game.say("Locked from the inside. Wren never left this room by the door.")
			return true
		"portrait":
			State.add_journal("portrait", "Wren's portrait", "Hollis Wren, painted the year he took the chair. The painter got the eyes wrong. They look past you, at the cabinet.")
			game.say("Professor Wren. The eyes look past you, toward the cabinet.")
			return true
		"cabinet":
			State.add_journal("cabinet", "The cabinet", "Black lacquer, nine wax seals. Three are cracked through. 'I opened three,' he wrote. The other six are whole, and warm to the touch.")
			game.say("Nine seals. Three are cracked. The rest are warm.")
			return false
		"window":
			game.say("Snow on the quad. Nobody has walked across it in days.")
			return true
		"diploma":
			game.say("Hollis Wren, Doctor of Philology. Yours hangs in a smaller frame.")
			return true
		"sampler":
			game.say("Needlepoint, in a script you almost recognise.")
			return true
		"coatrack":
			game.say("Wren's coat. He went somewhere without it.")
			return true
		"globe":
			game.say("Someone has scratched a mark into the South Pacific.")
			return true
	return false


func on_use(item: String, id: String, node: Node) -> bool:
	match [item, id]:
		["brass_key", "walnut_lock"]:
			State.remove_item("brass_key")
			State.set_flag("box_unlocked")
			game.play("unlock")
			PixelBox.set_texture(_part("walnut_lock"), tex("lock_open"))
			game.say("Click. The lid lifts.")
			game.busy = true
			await get_tree().create_timer(0.4).timeout
			var tw := create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
			tw.tween_method(func(d: float): walnut.set_hinge("top", d), 0.0, 115.0, 0.9)
			await tw.finished
			PixelBox.set_tappable(walnut.blocker, false)
			if game.mode == game.Mode.BOX:
				await game.show_face("top")
			game.busy = false
			game.say("Inside, a smaller box, sealed with wax.")
			return true
		["iron_key", "drawer"]:
			State.remove_item("iron_key")
			State.set_flag("drawer_open")
			game.play("slide")
			apply_state()
			game.say("The drawer slides open.")
			return true
		["matches", "lamp"]:
			State.remove_item("matches")
			State.set_flag("lamp_lit")
			game.play("match")
			PixelBox.set_texture(lamp, tex("lamp_lit"))
			glow.visible = true
			var tw := create_tween()
			tw.tween_method(func(v: float): set_wall_dim("e", v), 0.25, 1.0, 1.2)
			game.say("The wick catches. Light reaches the far wall.")
			return true
		["ring", "wax"]:
			State.remove_item("ring")
			State.set_flag("wax_broken")
			game.play("unlock")
			PixelBox.set_texture(_part("wax"), tex("wax_broken"))
			game.busy = true
			var tw := create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
			tw.tween_method(func(d: float): inner.set_hinge("top", d), 0.0, 115.0, 0.9)
			await tw.finished
			apply_state()
			game.busy = false
			game.say("The ring fits the seal. The wax splits like it was waiting.")
			return true
		["door_key", "door"]:
			await _open_door()
			return true
	return false


func _read_letter() -> void:
	State.set_flag("letter_read")
	game.play("paper")
	State.add_journal("letter", "Wren's letter",
		"\"Elias. Do not open it. I opened three.\n\nIf you must be the fool I was, begin at our hour. Three bells, as always. The box remembers what I forget.\n\nH.W.\"")
	game.say("\"Do not open it. I opened three.\" The letter is in your journal.", 5.0)


func _turn_dial(i: int, node: Node) -> void:
	if State.has("panel_open"):
		return
	game.busy = true
	game.play("click")
	var tw := create_tween()
	tw.tween_property(node, "rotation:z", -PI / 2, 0.1)
	await tw.finished
	node.rotation.z = 0.0
	State.set_flag("dial%d" % i, (int(State.flag_value("dial%d" % i, 0)) + 1) % SYMS.size())
	apply_state()
	game.busy = false
	var ok := true
	for k in 3:
		ok = ok and int(State.flag_value("dial%d" % k, 0)) == CODE[k]
	if ok:
		State.set_flag("panel_open")
		game.play("slide")
		var panel := _part("panel")
		var tw2 := create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw2.tween_property(panel, "position:y", panel_y + 2.0, 0.6)
		await tw2.finished
		apply_state()
		game.say("Something clicks inside the box. A panel slides open.")


func _pull_book(k: String, node: Node) -> void:
	var pulled: String = State.flag_value("books", "")
	if State.has("comp_open") or k in pulled:
		return
	pulled += k
	State.set_flag("books", pulled)
	game.play("slide", -4.0)
	apply_state()
	if not BOOK_ORDER.begins_with(pulled):
		game.busy = true
		await get_tree().create_timer(0.6).timeout
		State.set_flag("books", "")
		game.play("thunk")
		apply_state()
		game.busy = false
		game.say("The books slide back into place on their own.")
	elif pulled == BOOK_ORDER:
		State.set_flag("comp_open")
		await get_tree().create_timer(0.3).timeout
		game.play("unlock")
		apply_state()
		game.say("A panel in the shelf swings open.")


func _open_door() -> void:
	State.remove_item("door_key")
	State.set_flag("door_open")
	game.play("door")
	apply_state()
	game.say("The door opens. It does not open onto the corridor.", 4.0)
	await get_tree().create_timer(1.2).timeout
	game.complete_room.call_deferred(2, "The Restricted Stacks",
		"Beyond Wren's door is not the hallway but the library's locked stacks, two floors below, where you have never been allowed.\n\nThe door closes behind you. There is no handle on this side.")

## Seal 1, room 2: the restricted stacks under Miskatonic's library.
## Introduces the Lens. The curse of this room: the Lens shows one word nobody wrote. Your name.
## Chain: velvet case -> Lens. Lens shows I, II, III on three spines -> pull in order -> niche -> padlock key.
## Key -> chain on the lectern -> lift the book-box. Lens shows where the cover's rings must point
## -> cover opens -> a reliquary inside. Lens shows a button on its blank plate -> the first seal.
extends "res://scripts/room.gd"

const BOOK_ORDER := "sop"   # slate (I), ochre (II), plum (III)
const BOOKS := {"s": "slate", "o": "ochre", "p": "plum"}
const RINGS := {"ring_outer": 1, "ring_mid": 2, "ring_core": 3}   # target quarter-turns

var bookbox: PixelBox
var mini: PixelBox
var reliq: PixelBox


func build() -> void:
	title = "The Restricted Stacks"
	build_walls("r2_wall_")
	_build_north()
	_build_east()
	_build_south()
	_build_west()
	_build_bookbox()
	_build_reliquary()
	_define_steps()
	State.add_journal("stacks", "The stacks",
		"Wren's door let me out two floors below the library, among the restricted shelves. The air smells of old paper and the sea. The door is gone from this side. Only wall.")


func _lens_part(b: PixelBox, face: String, uv: Vector2, dim: Vector2, texname: String, id: String, depth := 0.05, tappable := false) -> MeshInstance3D:
	var p := b.add_part(face, uv, dim, tex(texname), id, depth, tappable)
	p.add_to_group("lens_only")
	return p


func _build_north() -> void:
	add_furniture("n", "lectern", Vector2(0, 0), Vector3(3, 5, 2),
		{"front": tex("lectern_front"), "default": tex("dark_side_32x96")}, {"dy": 1.6, "w": 4, "h": 8})
	add_sprite("n", "chain", Vector2(0, 6.4), Vector2(2, 3), "chain", 1.8)
	add_sprite("n", "arch_window", Vector2(0, 14), Vector2(4, 7), "arch_window")


func _build_east() -> void:
	var a := add_furniture("e", "stack_a", Vector2(-3.6, 0), Vector3(6.5, 16, 1.5),
		{"front": tex("stack_a"), "default": tex("wood_side_24x256")}, {"k": 2, "dy": -1.2, "w": 6.5, "h": 9})
	var xs := {"o": -1.125, "p": -0.375, "s": 0.375}
	var marks := {"o": 2, "p": 3, "s": 1}
	for k in xs:
		a.add_part("front", Vector2(xs[k], -1.0625), Vector2(0.5, 2), tex("book_" + BOOKS[k]), "book_" + BOOKS[k], 0.03)
		_lens_part(a, "front", Vector2(xs[k], -0.7), Vector2(0.75, 1), "lensmark_%d" % marks[k], "mark_" + k, 0.045)
	a.add_part("front", Vector2(1.75, -1.28), Vector2(1.5, 1.5), tex("item_chain_key"), "chain_key_part", 0.025)
	a.add_part("front", Vector2(1.75, -1.28), Vector2(1.5, 1.5), tex("niche"), "niche", 0.035)
	var b := add_furniture("e", "stack_b", Vector2(3.6, 0), Vector3(6.5, 16, 1.5),
		{"front": tex("stack_b"), "default": tex("wood_side_24x256")}, {"k": 2, "dy": 3.0, "w": 6.5, "h": 9})
	b.add_part("front", Vector2(0.5, 3.906), Vector2(0.5, 2), tex("book_wren"), "wren_book", 0.03)
	_lens_part(b, "front", Vector2(0.5, 4.3), Vector2(0.75, 1), "lensmark_w", "mark_w", 0.045)


func _build_south() -> void:
	add_sprite("s", "stacks_door", Vector2(3, 4), Vector2(4.5, 8), "stacks_door", 0.05)
	add_furniture("s", "ldesk", Vector2(-3.5, 0), Vector3(6, 3, 2.5),
		{"front": tex("ldesk_front"), "top": tex("wood_top_96x40"), "default": tex("wood_side_40x48")},
		{"dy": 1.0, "w": 6.5, "h": 5})
	add_sprite("s", "lens_case", Vector2(-3.5, 3.375), Vector2(1.5, 0.75), "lens_case", 1.3)


func _build_west() -> void:
	add_furniture("w", "catalog", Vector2(-3, 0), Vector3(5, 6, 2),
		{"front": tex("catalog_front"), "default": tex("wood_side_32x96")}, {})
	add_sprite("w", "arch2", Vector2(3.5, 10), Vector2(4, 7), "arch_window")


func _build_bookbox() -> void:
	bookbox = PixelBox.new()
	groups["n"].add_child(bookbox)
	bookbox.build({"front": tex("bookbox_front"), "back": tex("bookbox_back"), "left": tex("bookbox_left"),
		"right": tex("bookbox_right"), "top": tex("bookbox_top"), "bottom": tex("bookbox_top")},
		Vector3(6, 7, 3), tex("bookbox_liner"), ["front"])
	bookbox.hinge_face("front", "left")
	bookbox.blocker.set_meta("id", "bookbox")
	# three concentric rings; one touch area decides which ring by distance from the centre
	bookbox.add_part("front", Vector2(0, 0.4), Vector2(4, 4), tex("ring_outer"), "ring_outer", 0.03, false)
	bookbox.add_part("front", Vector2(0, 0.4), Vector2(2.625, 2.625), tex("ring_mid"), "ring_mid", 0.04, false)
	bookbox.add_part("front", Vector2(0, 0.4), Vector2(1.375, 1.375), tex("ring_core"), "ring_core", 0.05, false)
	bookbox.add_part("front", Vector2(0, 0.4), Vector2(4, 4), tex("clear"), "rings", 0.065)
	_lens_part(bookbox, "front", Vector2(0, 0.4), Vector2(4.5, 4.5), "ring_ghost", "ring_ghost", 0.06)
	bookbox.add_part("right", Vector2(0, 0), Vector2(0.625, 1.5), tex("clasp"), "clasp", 0.03)

	mini = PixelBox.new()
	bookbox.add_child(mini)
	mini.build(_reliq_faces(), 6.0, tex("reliq_liner"), ["front"])
	mini.hinge_face("front", "bottom")
	mini.blocker.set_meta("id", "dive:reliquary")
	mini.scale = Vector3.ONE * 0.3
	mini.position = Vector3(0, -0.6, -0.4)

	bookbox.scale = Vector3.ONE * 0.4
	bookbox.position = Vector3(0, 5 + 1.4, -HALF + 1.0)
	register_box("bookbox", bookbox)


func _reliq_faces() -> Dictionary:
	return {"front": tex("reliq_front"), "back": tex("reliq_back"), "left": tex("reliq_left"),
		"right": tex("reliq_right"), "top": tex("reliq_top"), "bottom": tex("reliq_bottom")}


func _build_reliquary() -> void:
	reliq = PixelBox.new()
	reliq.build(_reliq_faces(), 6.0, tex("reliq_liner"), ["front"])
	reliq.hinge_face("front", "bottom")
	reliq.blocker.set_meta("id", "reliquary")
	reliq.add_part("front", Vector2(0, 0.8), Vector2(4, 1.25), tex("reliq_plate"), "plate", 0.03)
	_lens_part(reliq, "front", Vector2(0, 0.8), Vector2(4, 1.25), "reliq_name", "plate_name", 0.045)
	_lens_part(reliq, "front", Vector2(0, -1.2), Vector2(0.75, 0.75), "phantom_button", "phantom", 0.05, true)
	var s := PixelBox.quad(Vector2(1.5, 1.5), tex("item_seal_stone"))
	s.position = Vector3(0, -1.2, -0.8)
	PixelBox.add_body(s, Vector2(1.5, 1.5), "seal_part")
	reliq.add_child(s)
	add_stage_box("reliquary", reliq, "front")


var ring_nodes := {}


func _part(id: String) -> MeshInstance3D:
	if ids.has(id):
		return ids[id]
	if ring_nodes.is_empty():
		for c in bookbox.faces["front"].get_children():
			if c.has_meta("id"):
				ring_nodes[c.get_meta("id")] = c
	return ring_nodes[id]


func _take(item: String, flag: String) -> void:
	State.add_item(item)
	State.set_flag(flag)


# ---------------- steps ----------------

func _define_steps() -> void:
	steps = [
		{"id": "lens", "done": func(): return State.has("lens_taken"),
			"hints": ["Something on the librarian's desk catches the light.", "Open the velvet case on the librarian's desk (south wall) and take what's inside."],
			"solve": func(): _take("lens", "lens_taken"), "said": "Wren's Lens is in your hand."},
		{"id": "books", "done": func(): return State.has("niche_open"),
			"hints": ["The Lens shows what ink cannot. Look at the shelves through it.", "With the Lens on, pull the marked books in the left stack in order: I, then II, then III."],
			"solve": func():
				State.set_flag("books2", BOOK_ORDER)
				State.set_flag("niche_open"),
			"said": "Three books slide out by themselves. A niche opens."},
		{"id": "chain_key", "done": func(): return State.has("chain_key_taken"),
			"hints": ["A niche opened in the left stack.", "Take the little key from the niche in the left stack."],
			"solve": func(): _take("chain_key", "chain_key_taken"), "said": "The padlock key is in your hand."},
		{"id": "chain", "done": func(): return State.has("chain_off"),
			"hints": ["The book on the lectern is chained down.", "Use the padlock key on the chain over the book."],
			"solve": func():
				State.remove_item("chain_key")
				State.set_flag("chain_off"),
			"said": "The chain falls away from the book."},
		{"id": "rings", "done": func(): return State.has("cover_open"),
			"hints": ["The book's cover has three rings that turn.", "Lift the book. With the Lens on, turn each ring until its notch meets a glowing mark."],
			"solve": func():
				for r in RINGS:
					State.set_flag(r, RINGS[r])
				State.set_flag("cover_open"),
			"said": "The rings align. The cover swings open."},
		{"id": "phantom", "done": func(): return State.has("reliq_open"),
			"hints": ["The small box inside the book has a blank plate. Not blank to every eye.", "Look at the small box with the Lens on and press what appears below its plate."],
			"solve": func(): State.set_flag("reliq_open"), "said": "The small box opens."},
		{"id": "seal", "done": func(): return State.has("seal_taken"),
			"hints": ["Something waits inside the small box.", "Take the stone from inside the small box."],
			"solve": func(): await _take_seal(), "said": "The first seal is yours."},
	]
	walkthrough = [
		["shot", "start"],
		["tap", "lens_case"], ["shot", "lens_taken"], ["examine", "lens"],
		["lens", true], ["tap", "stack_a"], ["shot", "stacks_lens"], ["back"],
		["tap", "book_plum"], ["wait", 1.0],
		["tap", "book_slate"], ["tap", "book_ochre"], ["tap", "book_plum"], ["wait", 0.8],
		["shot", "niche_open"], ["tap", "chain_key_part"],
		["tap", "wren_book"], ["lens", false],
		["tap", "bookbox"], ["shot", "chained"],
		["use", "chain_key", "chain"], ["shot", "chain_off"],
		["tap", "bookbox"], ["shot", "book_front"], ["lens", true], ["shot", "book_lens"],
		["tapat", "rings", Vector2(0, 1.65)], ["tapat", "rings", Vector2(1.0, 0)], ["tapat", "rings", Vector2(0, -1.0)],
		["tapat", "rings", Vector2(0.2, 0.2)], ["tapat", "rings", Vector2(-0.2, 0.2)], ["tapat", "rings", Vector2(0, 0)],
		["wait", 1.5], ["shot", "book_open"], ["expect", "cover_open"],
		["tap", "dive:reliquary"], ["shot", "reliquary_lens"],
		["tap", "phantom"], ["wait", 1.5], ["shot", "reliquary_open"], ["expect", "reliq_open"],
		["tap", "seal_part"], ["wait", 3.0], ["expect", "seal_taken"],
	]


# ---------------- state -> visuals ----------------

func apply_state() -> void:
	PixelBox.set_texture(_part("lens_case"), tex("lens_case_open" if State.has("lens_taken") else "lens_case"))
	var pulled: String = State.flag_value("books2", "")
	for k in BOOKS:
		PixelBox.set_texture(_part("book_" + BOOKS[k]), tex("book_%s%s" % [BOOKS[k], "_pulled" if k in pulled else ""]))
	PixelBox.set_texture(_part("niche"), tex("niche_open" if State.has("niche_open") else "niche"))
	PixelBox.set_tappable(_part("niche"), not State.has("niche_open"))
	var ck := _part("chain_key_part")
	ck.visible = State.has("niche_open") and not State.has("chain_key_taken")
	PixelBox.set_tappable(ck, ck.visible)
	PixelBox.set_texture(_part("wren_book"), tex("book_wren_pulled" if State.has("fragment1") else "book_wren"))

	var chain := _part("chain")
	chain.visible = not State.has("chain_off")
	PixelBox.set_tappable(chain, chain.visible)

	for r in RINGS:
		_part(r).rotation.z = -int(State.flag_value(r, 0)) * PI / 2
	var open := State.has("cover_open")
	bookbox.set_hinge("front", 110.0 if open else 0.0)
	PixelBox.set_tappable(bookbox.blocker, not open)
	PixelBox.set_texture(_part("clasp"), tex("clasp_open" if open else "clasp"))

	var ropen := State.has("reliq_open")
	reliq.set_hinge("front", 100.0 if ropen else 0.0)
	mini.set_hinge("front", 100.0 if ropen else 0.0)
	PixelBox.set_tappable(reliq.blocker, not ropen)
	var seal := _part("seal_part")
	seal.visible = not State.has("seal_taken")
	PixelBox.set_tappable(seal, ropen and not State.has("seal_taken"))
	_part("phantom").set_meta("gone", ropen)


# ---------------- taps ----------------

func on_tap(id: String, node: Node) -> bool:
	match id:
		"lens_case":
			if not State.has("lens_taken"):
				_take("lens", "lens_taken")
				game.play("reveal")
				apply_state()
				State.add_journal("lens", "Wren's Lens",
					"A lens of green glass in a velvet case, labelled in Wren's hand: FOR E.T. He knew I would come down here. Through it the stacks look different. Truer, or less true.")
				game.say("Wren's Lens. Touch the Lens button to look through it.", 5.0)
			return true
		"book_slate", "book_ochre", "book_plum":
			await _pull_book(id.substr(5, 1), node)
			return true
		"niche":
			if not State.has("niche_open"):
				game.say("A wooden panel between the books. No handle, no keyhole.")
			return true
		"chain_key_part":
			_take("chain_key", "chain_key_taken")
			game.play("pickup")
			apply_state()
			game.say("A tiny key on a ribbon, stamped with the library's seal.")
			return true
		"wren_book":
			if game.lens_on and not State.has("fragment1"):
				State.set_flag("fragment1")
				State.fragments += 1
				game.play("reveal")
				apply_state()
				State.add_journal("fragment1", "Wren's fragment, I",
					"Tucked in a book with a W only the Lens can see, in Wren's hand:\n\n\"The first seal tests the eye. The second tests the nerve. By the third it is testing something else, and I no longer know what I am being measured for. If you find these, Elias, stop at one.\"")
				game.say("A note from Wren, hidden in the book. It's in your journal.", 5.0)
			else:
				game.say("A thin volume, no title on the spine.")
			return true
		"lift:bookbox":
			if not State.has("chain_off"):
				game.shake(node)
				game.say("The book is chained to the lectern.")
				return true
			return false
		"chain":
			game.say("A chain and a little padlock, holding the book down.")
			return true
		"rings":
			var p: Vector3 = node.global_transform.affine_inverse() * game.last_hit
			var r := Vector2(p.x, p.y).length()
			if r < 2.05:
				var which := "ring_core" if r < 0.7 else "ring_mid" if r < 1.32 else "ring_outer"
				await _turn_ring(which, _part(which))
			return true
		"clasp":
			if not State.has("cover_open"):
				game.say("A brass clasp. The rings must be holding it shut.")
			return true
		"plate":
			game.say("A blank silver plate. Nothing engraved. Nothing your eyes can see.")
			return true
		"phantom":
			await _open_reliquary()
			return true
		"seal_part":
			await _take_seal()
			return true
		"catalog":
			State.add_journal("catalog", "The card catalog",
				"One card is filed out of place: \"Restricted volumes are marked in a light only the trained eye perceives. Fetch them in the order of their numbering.\"")
			game.say("A card filed out of place. It's in your journal.")
			return false
		"stacks_door":
			game.say("Not the door you came in by. It won't move.")
			return true
		"arch_window", "arch2":
			game.say("Painted glass. There is no outside down here.")
			return true
		"lectern":
			return false
	return false


func on_use(item: String, id: String, _node: Node) -> bool:
	match [item, id]:
		["chain_key", "chain"]:
			State.remove_item("chain_key")
			State.set_flag("chain_off")
			game.play("unlock")
			apply_state()
			game.say("The padlock springs. The chain slithers off the book.")
			return true
	return false


func _pull_book(k: String, _node: Node) -> void:
	var pulled: String = State.flag_value("books2", "")
	if State.has("niche_open") or k in pulled:
		return
	pulled += k
	State.set_flag("books2", pulled)
	game.play("slide", -4.0)
	apply_state()
	if not BOOK_ORDER.begins_with(pulled):
		game.busy = true
		await get_tree().create_timer(0.6).timeout
		State.set_flag("books2", "")
		game.play("thunk")
		apply_state()
		game.busy = false
		game.say("The books slide back into place on their own.")
	elif pulled == BOOK_ORDER:
		State.set_flag("niche_open")
		await get_tree().create_timer(0.3).timeout
		game.play("unlock")
		apply_state()
		game.say("A niche opens between the shelves.")


func _turn_ring(id: String, node: Node3D) -> void:
	if State.has("cover_open"):
		return
	game.busy = true
	var n := (int(State.flag_value(id, 0)) + 1) % 4
	State.set_flag(id, n)
	game.play("click")
	var tw := create_tween()
	tw.tween_property(node, "rotation:z", -n * PI / 2 if n != 0 else -2 * PI, 0.18)
	await tw.finished
	node.rotation.z = -n * PI / 2
	game.busy = false
	for r in RINGS:
		if int(State.flag_value(r, 0)) != RINGS[r]:
			return
	State.set_flag("cover_open")
	game.busy = true
	game.play("unlock")
	await get_tree().create_timer(0.3).timeout
	PixelBox.set_texture(_part("clasp"), tex("clasp_open"))
	game.play("slide")
	var tw2 := create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw2.tween_method(func(d: float): bookbox.set_hinge("front", d), 0.0, 110.0, 1.0)
	await tw2.finished
	apply_state()
	game.busy = false
	game.say("The cover swings open. The pages are hollowed out. Something sits inside.")


func _open_reliquary() -> void:
	if State.has("reliq_open"):
		return
	State.set_flag("reliq_open")
	game.busy = true
	game.play("unlock")
	_part("phantom").set_meta("gone", true)
	set_lens(game.lens_on)
	var tw := create_tween().set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	tw.tween_method(func(d: float): reliq.set_hinge("front", d), 0.0, 100.0, 0.9)
	await tw.finished
	apply_state()
	game.busy = false
	State.add_journal("name", "The plate",
		"The plate on the little box is blank. Through the Lens it is not. It is engraved, in a careful hand that is not Wren's and not mine:\n\nELIAS THORNE\n\nIt was made for me before I was born.")
	game.say("Through the Lens the plate reads ELIAS THORNE. The box opens for you.", 6.0)


func _take_seal() -> void:
	if State.has("seal_taken"):
		return
	_take("seal_stone", "seal_taken")
	game.play("reveal")
	apply_state()
	State.add_journal("seal1", "The first seal",
		"A five-sided stone, warm, humming at the edge of hearing. It belongs in Wren's cabinet. I know that the way I know my own name. Eight seals remain. Wren stopped at three. I will not need to stop.")
	await get_tree().create_timer(1.5).timeout
	var bargains := "" if State.bargains == 0 else "\n\nBargains made: %d." % State.bargains
	var frags := "\nWren's fragments found: %d of 9." % State.fragments
	game.complete_room.call_deferred(99, "SEAL I OF IX BROKEN",
		"The stone hums in your hand all the way back to Wren's study, where the cabinet is waiting. One seal fits. Eight remain.\n\nThis is the end of the first seal." + frags + bargains)

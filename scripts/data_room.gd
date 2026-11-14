## A room built entirely from a JSON file in data/rooms/.
## The file describes: the objects (furniture, sprites, hero boxes, nested boxes, parts),
## the puzzle kinds (cyclers, combinations, sequences, radial rings, pickups, dark walls),
## the bindings that tie every visual to the game state, the interactions (tap / use item),
## the steps (hints + bargain solutions) and the walkthrough the autotest plays.
## Format reference: docs/puzzle-format.md
extends "res://scripts/room.gd"

var data: Dictionary
var nodes := {}          ## id -> node (tappable or not)
var box_nodes := {}      ## box name -> PixelBox (hero boxes, nested minis, stage twins)
var base_pos := {}       ## node id -> original position, for offset bindings
var last := {}           ## binding key -> last applied value, so only changes animate
var puzzles: Array = []


func load_file(path: String) -> void:
	var f := FileAccess.open(path, FileAccess.READ)
	var parsed = JSON.parse_string(f.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("Room file %s is not valid JSON" % path)
		return
	data = parsed


# ---------------- building ----------------

func build() -> void:
	title = data.get("title", "")
	build_walls(data["walls"], data.get("floor", ""), data.get("ceiling", ""))
	for o in data.get("objects", []):
		_build_object(o)
	puzzles = data.get("puzzles", [])
	for p in puzzles:
		if p["kind"] == "beam":
			_build_beam(p)
	for s in data.get("steps", []):
		var spec: Dictionary = s
		steps.append({"id": spec["id"], "hints": spec["hints"], "said": spec.get("said", "It is done."),
			"done": func(): return cond(spec["done"]),
			"solve": func(): await run(spec["solve"])})
	walkthrough = _walkthrough(data.get("walkthrough", []))
	for a in data.get("on_enter", []):
		if a.has("set") and not State.flags.has(a["set"]):
			State.flags[a["set"]] = a.get("value", true)
		if a.has("journal"):
			State.add_journal(a["journal"][0], a["journal"][1], a["journal"][2])


func _v2(a) -> Vector2:
	return Vector2(a[0], a[1])


func _v3(a) -> Vector3:
	return Vector3(a[0], a[1], a[2]) if a is Array else Vector3.ONE * float(a)


func _faces(d: Dictionary) -> Dictionary:
	var out := {}
	for k in d:
		out[k] = tex(d[k])
	return out


func _build_object(o: Dictionary) -> void:
	match o["type"]:
		"furniture":
			var z = o.get("zoom", {})
			var b := add_furniture(o["wall"], o["id"], _v2(o["pos"]), _v3(o["size"]), _faces(o["faces"]), z if z is Dictionary else {})
			nodes[o["id"]] = b
			box_nodes[o["id"]] = b
			if o.get("zoom") is bool and not o["zoom"]:
				b.remove_meta("zoom")   ## worked from the room view, never zoomed
			for h in o.get("hinges", []):
				b.hinge_face(h[0], h[1])
			if not o.get("tappable", true):
				PixelBox.set_tappable(b.blocker, false)
			_parts(b, o.get("parts", []))
		"sprite":
			var q := add_sprite(o["wall"], o["id"], _v2(o["center"]), _v2(o["size"]), o["tex"], o.get("depth", 0.03), o.get("tappable", true))
			if o.get("additive", false):
				q.material_override = _additive(tex(o["tex"]))
			if o.get("lens", false):
				q.add_to_group("lens_only")
				q.set_meta("lens_level", int(o["lens"]) if not (o["lens"] is bool) else 1)
				q.set_meta("lens_tappable", o.get("tappable", true))
			nodes[o["id"]] = q
		"box":
			var b := _make_box(o)
			groups[o["wall"]].add_child(b)
			b.scale = Vector3.ONE * float(o.get("scale", 1.0))
			b.position = Vector3(o["pos"][0], o["pos"][1], -HALF + float(o.get("depth", 1.0)))
			register_box(o["name"], b, o.get("view", "front"))
		"stage_box":
			var b := _make_box(o)
			add_stage_box(o["name"], b, o.get("view", "front"))


func _additive(t: Texture2D) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	m.albedo_texture = t
	return m


func _make_box(o: Dictionary) -> PixelBox:
	var b := PixelBox.new()
	b.build(_faces(o["faces"]), _v3(o.get("size", 6)), tex(o["liner"]) if o.has("liner") else null, o.get("liner_skip", ["top"]))
	for h in o.get("hinges", []):
		b.hinge_face(h[0], h[1])
	if o.has("blocker"):
		b.blocker.set_meta("id", o["blocker"])
	box_nodes[o["name"]] = b
	_parts(b, o.get("parts", []))
	for s in o.get("inner_sprites", []):
		var q := PixelBox.quad(_v2(s["size"]), tex(s["tex"]))
		var rot: Array = s.get("rot", [0, 0, 0])
		q.transform = Transform3D(Basis.from_euler(Vector3(rot[0], rot[1], rot[2]) * (PI / 180.0)), _v3(s["pos"]))
		PixelBox.add_body(q, _v2(s["size"]), s["id"])
		if s.has("face"):
			q.set_meta("face", s["face"])   ## which face to turn toward you to see it
		b.add_child(q)
		nodes[s["id"]] = q
	for c in o.get("children", []):
		var m := _make_box(c)
		b.add_child(m)
		m.scale = Vector3.ONE * float(c.get("scale", 1.0))
		m.position = _v3(c.get("pos", [0, 0, 0]))
	return b


func _parts(b: PixelBox, parts: Array) -> void:
	for p in parts:
		var part := b.add_part(p["face"], _v2(p["uv"]), _v2(p["size"]), tex(p["tex"]), p["id"],
			p.get("depth", 0.03), p.get("tappable", true))
		if p.get("lens", false):
			part.add_to_group("lens_only")
			part.set_meta("lens_level", int(p["lens"]) if not (p["lens"] is bool) else 1)
			part.set_meta("lens_tappable", p.get("tappable", true))
		nodes[p["id"]] = part


func _walkthrough(w: Array) -> Array:
	var out: Array = []
	for a in w:
		if a[0] == "repeat":
			for i in int(a[1]):
				out.append_array(_walkthrough(a.slice(2)))
		elif a[0] == "tapat":
			out.append(["tapat", a[1], Vector2(a[2][0], a[2][1])])
		else:
			out.append(a)
	return out


# ---------------- conditions ----------------

## "flag", "!flag", "item:x", "!item:x", "lens", "!lens", "flag=3", or an array of these (all must hold).
## An array that starts with "any" holds if any one of the rest holds.
func cond(c) -> bool:
	if c == null:
		return true
	if c is Array and c.size() > 0 and str(c[0]) == "any":
		for x in c.slice(1):
			if cond(x):
				return true
		return false
	if c is Array:
		for x in c:
			if not cond(x):
				return false
		return true
	var s: String = c
	if s.begins_with("!"):
		return not cond(s.substr(1))
	if s == "lens":
		return game.lens_on
	if s.begins_with("item:"):
		return State.has_item(s.substr(5))
	for op in ["==", "<", ">"]:
		if op in s:
			## "wl==wr", "wl<wr", "sand>2": compare two flags, or a flag with a number
			var lr := s.split(op)
			var x := _num(lr[0])
			var y := _num(lr[1])
			return x == y if op == "==" else (x < y if op == "<" else x > y)
	if "%" in s and "=" in s:
		## "turns%4=2": the flag's value modulo 4 is 2
		var name := s.split("%")[0]
		var rest := s.split("%")[1].split("=")
		return posmod(int(State.flag_value(name, 0)), int(rest[0])) == int(rest[1])
	if "=" in s:
		var kv := s.split("=")
		return str(State.flag_value(kv[0], "")) == kv[1] or (str(kv[1]).is_valid_int() and int(State.flag_value(kv[0], -999)) == int(kv[1]))
	return State.has(s)


## The impossible street ("street": {"right": 5, "left": 3}): turning right walks a circuit of
## right-1 other facades before home; turning left, left-1. Flag "facade": "home", "r2", "l1"...
func _walk_street() -> void:
	var lv := int(State.flag_value("last_view", 0))
	var d := posmod(game.view - lv, 4)
	State.flags["last_view"] = game.view
	var st: Dictionary = data["street"]
	for i in (d if d != 3 else 1):
		if st.has("vane") and cond(st.get("vane_while")):
			## the weathercock turns with the street: one point on for a left turn, one back for a right
			State.flags[st["vane"]] = posmod(int(State.flag_value(st["vane"], 0)) + (1 if d == 3 else -1), 8)
		if d == 3:
			State.flags["sl"] = (int(State.flag_value("sl", 0)) + 1) % int(st["left"])
			State.flags["sr"] = 0
		else:
			State.flags["sr"] = (int(State.flag_value("sr", 0)) + 1) % int(st["right"])
			State.flags["sl"] = 0
	var sr := int(State.flag_value("sr", 0))
	var sl := int(State.flag_value("sl", 0))
	State.flags["facade"] = "r%d" % sr if sr > 0 else ("l%d" % sl if sl > 0 else "home")
	State.save_game()


## Tap one panel, then another: they change places.
func _swap(p: Dictionary, id: String) -> void:
	var sel_key: String = p["flag"] + "_sel"
	var sel: String = str(State.flag_value(sel_key, ""))
	if sel == "" or sel == id:
		State.set_flag(sel_key, "" if sel == id else id)
		game.play("click")
		if sel == "":
			game.flash(_part(id))
		return
	var order: String = str(State.flag_value(p["flag"], p["start"]))
	var a: int = p["parts"].find(sel)
	var b: int = p["parts"].find(id)
	var ca := order[a]
	order[a] = order[b]
	order[b] = ca
	State.set_flag(sel_key, "")
	State.set_flag(p["flag"], order)
	game.play(p.get("sfx", "slide"))
	await refresh(false)


func _num(x: String) -> int:
	return int(x) if x.is_valid_int() else int(State.flag_value(x, 0))


# ---------------- state -> visuals ----------------

func apply_state() -> void:
	await refresh(false)


## Make every visual match the state. With animate, things that changed tween into place.
func refresh(animate := true) -> void:
	var longest := 0.0
	for p in puzzles:
		match p["kind"]:
			"cycler":
				var v := int(State.flag_value(p["flag"], p.get("start", 0)))
				_cycler_visual(p, v)
			"radial":
				for r in p["rings"]:
					_part(r[0]).rotation.z = deg_to_rad(float(p.get("rotate", -90))) * int(State.flag_value(r[0], 0))
			"swap":
				## {"kind":"swap","parts":[ids],"flag":"order","start":"31402","tex":"mural_%s"}: part i shows tex % order[i]
				var order: String = str(State.flag_value(p["flag"], p["start"]))
				for i in p["parts"].size():
					PixelBox.set_texture(_part(p["parts"][i]), tex(p["tex"] % order[i]))
			"sequence":
				var pulled: String = State.flag_value(p["flag"], "")
				for part_id in p["parts"]:
					var k: String = p["parts"][part_id]
					PixelBox.set_texture(_part(part_id), tex(p["tex"][part_id] + (p.get("pulled_suffix", "_pulled") if k in pulled else "")))
			"pickup":
				var show := cond(p.get("show_if")) and not State.has(p["flag"])
				var n := _part(p["part"])
				n.visible = show
				PixelBox.set_tappable(n, show)
			"beam":
				_draw_beam(p)
			"lights":
				var bits: String = State.flag_value(p["flag"], p["start"])
				for i in p["parts"].size():
					PixelBox.set_texture(_part(p["parts"][i]), tex(p["on"] if bits[i] == "1" else p["off"]))
			"roll":
				var at := _roll_at(p)
				var tok := _part(p["token"])
				var uv := _cell_uv(p, at.x, at.y)
				tok.position = Vector3(uv.x, uv.y, tok.position.z)
			"dark":
				var lit := State.has(p["until"])
				longest = maxf(longest, _apply_value("wall:" + p["wall"], "dim", 1.0 if lit else float(p.get("dim", 0.25)), animate, float(p.get("anim", 1.2)), 0.0))
	for b in data.get("bindings", []):
		var props: Dictionary = b.get("then", {}) if cond(b.get("when")) else b.get("else", {})
		for prop in props:
			longest = maxf(longest, _apply_value(b["target"], prop, props[prop], animate, float(b.get("anim", 0.0)), float(b.get("delay", 0.0))))
	if animate and longest > 0.0:
		await get_tree().create_timer(longest).timeout


func _cycler_visual(p: Dictionary, v: int, animate := false) -> void:
	var n := _part(p["part"])
	if p.has("offsets"):
		if not base_pos.has(p["part"]):
			base_pos[p["part"]] = n.position
		var o: Array = p["offsets"][v]
		var to: Vector3 = base_pos[p["part"]] + Vector3(o[0], o[1], 0)
		if animate:
			create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT).tween_property(n, "position", to, 0.2)
		else:
			n.position = to
	if p.has("rotate"):
		n.rotation.z = deg_to_rad(float(p["rotate"])) * v
	if p.has("textures"):
		PixelBox.set_texture(n, tex(p["textures"][v]))


## Apply one property to one target. Returns how long its animation runs (0 if none).
## Text values can show a flag: "tally_{turns:30}" is tally_ plus the turns flag, capped at 30.
func _fmt(v):
	if not (v is String) or not "{" in v:
		return v
	var re := RegEx.create_from_string("\\{(\\w+)(?::(\\d+))?\\}")
	var out: String = v
	for m in re.search_all(v):
		var n := int(State.flag_value(m.get_string(1), 0))
		if m.get_string(2) != "":
			n = mini(n, int(m.get_string(2)))
		out = out.replace(m.get_string(0), str(n))
	return out


func _apply_value(target: String, prop: String, value, animate: bool, anim: float, delay: float) -> float:
	value = _fmt(value)
	var key := target + "/" + prop
	var changed: bool = not last.has(key) or last[key] != value
	var had_value := last.has(key)
	last[key] = value
	var tween_it := animate and anim > 0.0 and changed and had_value
	if target.begins_with("wall:"):
		var w := target.substr(5)
		if tween_it:
			var from: float = groups[w].get_meta("dim", 1.0)
			var tw := create_tween()
			tw.tween_interval(delay)
			tw.tween_method(func(x: float): set_wall_dim(w, x), from, float(value), anim)
		else:
			set_wall_dim(w, float(value))
		groups[w].set_meta("dim", float(value))
		return delay + anim if tween_it else 0.0
	if target.begins_with("hinge:"):
		var bf := target.substr(6).split(".")
		var b: PixelBox = box_nodes[bf[0]]
		if tween_it:
			var tw := create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
			tw.tween_interval(delay)
			tw.tween_method(func(d: float): b.set_hinge(bf[1], d), b.get_hinge(bf[1]), float(value), anim)
			return delay + anim
		b.set_hinge(bf[1], float(value))
		return 0.0
	var n: Node3D
	if target.begins_with("box:") and prop == "visible":
		box_nodes[target.substr(4)].visible = value   ## the whole box, not just its touch area
		return 0.0
	if target.begins_with("box:"):
		n = box_nodes[target.substr(4)].blocker
	else:
		n = _part(target)
	match prop:
		"texture":
			if tween_it and delay > 0.0:
				get_tree().create_timer(delay).timeout.connect(func(): PixelBox.set_texture(n, tex(value)))
				return delay
			PixelBox.set_texture(n, tex(value))
		"visible":
			n.visible = value
		"tappable":
			PixelBox.set_tappable(n, value)
		"gone":
			n.set_meta("gone", value)
		"offset":
			if not base_pos.has(target):
				base_pos[target] = n.position
			var to: Vector3 = base_pos[target] + Vector3(value[0], value[1], 0)
			if tween_it:
				var tw := create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
				tw.tween_interval(delay)
				tw.tween_property(n, "position", to, anim)
				return delay + anim
			n.position = to
	return 0.0


func _part(id: String) -> Node3D:
	if nodes.has(id):
		return nodes[id]
	return ids[id]


# ---------------- actions ----------------

## Run a list of actions in order. Everything visual follows from the state, so most
## actions just change state; the room refreshes (animated) at the end.
func run(actions: Array, node: Node = null) -> void:
	game.busy = true
	for a in actions:
		if a.has("if") and not cond(a["if"]):
			continue
		if a.has("ask"):
			## ["title", "text", ["Yes", "No"]]: the rest of the actions run only on the first answer
			game.busy = false
			var choice: String = await game._dialog(_fill(a["ask"][0]), _fill(a["ask"][1]), a["ask"][2])
			game.busy = true
			if choice != a["ask"][2][0]:
				break
		if a.has("burn"):
			## feed the newest page you still have to the fire ("burn": "<key>" burns that page first)
			var title := State.tear_key(a["burn"]) if a["burn"] is String else State.tear_page()
			if title == "":
				game.say("There is nothing left in your journal to burn.", 4.0)
				break
			State.flags["burned"] = int(State.flag_value("burned", 0)) + 1
			State.save_game()
			game.say("The fire takes a page from your journal: %s." % title, 4.0)
		if a.has("add"):
			State.set_flag(a["add"], int(State.flag_value(a["add"], 0)) + int(a.get("value", 1)))
		if a.has("set"):
			State.set_flag(a["set"], a.get("value", true))
		if a.has("unset"):
			State.flags.erase(a["unset"])
			State.save_game()
		if a.has("give"):
			State.add_item(a["give"])
		if a.has("take"):
			State.remove_item(a["take"])
		if a.has("sfx"):
			game.play(a["sfx"], float(a.get("db", 0.0)))
		if a.has("journal"):
			State.add_journal(a["journal"][0], a["journal"][1], _fill(a["journal"][2]))
		if a.has("fragment"):
			State.fragments += 1
			State.save_game()
		if a.has("shake") and node:
			game.shake(node)
		if a.has("refresh"):
			await refresh(true)
			if game.lens_on:
				set_lens(true)
		if a.has("wait"):
			await get_tree().create_timer(float(a["wait"])).timeout
		if a.has("face") and game.mode == game.Mode.BOX:
			await game.show_face(a["face"])
		if a.has("say"):
			game.say(_fill(a["say"]), float(a.get("secs", 3.5)))
		if a.has("complete_room"):
			var c: Array = a["complete_room"]
			game.complete_room.call_deferred(int(c[0]), _fill(c[1]), _fill(c[2]))
	await refresh(true)
	set_lens(game.lens_on)
	game.busy = false
	await _check_beams()
	if not _combos_running:
		_combos_running = true
		await _check_combos()   ## combos made only of flags (all three latches open at once)
		_combos_running = false


func _fill(s: String) -> String:
	return s.replace("{fragments}", str(State.fragments)) \
		.replace("{bargains_line}", "" if State.bargains == 0 else "\n\nBargains made: %d." % State.bargains)


# ---------------- taps and items ----------------

func on_tap(id: String, node: Node) -> bool:
	for p in puzzles:
		if p["kind"] == "dark" and not State.has(p["until"]) and wall_of(node) == p["wall"]:
			game.say(p.get("say", "Too dark to see."))
			return true
	for p in puzzles:
		match p["kind"]:
			"cycler":
				if p["part"] == id:
					await _turn_cycler(p, node)
					return true
			"radial":
				if p["part"] == id:
					var local: Vector3 = node.global_transform.affine_inverse() * game.last_hit
					var r := Vector2(local.x, local.y).length()
					for ring in p["rings"]:
						if r < float(ring[1]):
							await _turn_radial(p, ring[0])
							break
					return true
			"swap":
				if id in p["parts"]:
					if p.has("lock") and cond(p["lock"]):
						return false
					await _swap(p, id)
					return true
			"sequence":
				if p["parts"].has(id):
					await _pull(p, p["parts"][id])
					return true
			"combo":
				if p.get("commit", "") == id:
					await _commit_all(id, node)
					return true
			"lights":
				if id in p["parts"]:
					await _toggle(p, p["parts"].find(id), node)
					return true
			"melody":
				if p["parts"].has(id):
					await _note(p, p["parts"][id])
					return true
			"roll":
				if p["buttons"].has(id):
					await _roll(p, p["buttons"][id], node)
					return true
			"pickup":
				if p["part"] == id:
					State.set_flag(p["flag"])
					State.add_item(p["item"])
					await run([{"sfx": p.get("sfx", "pickup")}] + p.get("then", []), node)
					return true
	for it in data.get("interactions", []):
		if it["on"] == "tap" and _matches(it, id) and cond(it.get("when")):
			await run(it["do"], node)
			return it.get("handled", true)
	return false


func _matches(it: Dictionary, id: String) -> bool:
	return it.get("id", "") == id or id in it.get("ids", [])


func on_use(item: String, id: String, node: Node) -> bool:
	for it in data.get("interactions", []):
		if it["on"] == "use" and it["item"] == item and _matches(it, id) and cond(it.get("when")):
			await run(it["do"], node)
			return true
	return false


func _turn_cycler(p: Dictionary, node: Node3D) -> void:
	if cond(p.get("lock")) and p.has("lock"):
		if p.has("locked_say"):
			game.say(p["locked_say"])
		return
	game.busy = true
	var count := int(p["count"])
	var v := (int(State.flag_value(p["flag"], p.get("start", 0))) + 1) % count
	State.set_flag(p["flag"], v)
	game.play(p.get("sfx", "click"))
	if not p.get("spin", true):
		_cycler_visual(p, v, true)
		game.busy = false
		var on0: Dictionary = p.get("on", {})
		if on0.has(str(v)):
			await run(on0[str(v)], node)
		await _check_combos()
		await _check_beams()
		return
	var tw := create_tween()
	if p.has("rotate"):
		var step := deg_to_rad(float(p["rotate"]))
		tw.tween_property(node, "rotation:z", step * (v if v != 0 else count), 0.15)
		await tw.finished
		node.rotation.z = step * v
	else:
		tw.tween_property(node, "rotation:z", -PI / 2, 0.1)
		await tw.finished
		node.rotation.z = 0.0
		_cycler_visual(p, v)
	game.busy = false
	var on: Dictionary = p.get("on", {})
	if on.has(str(v)):
		await run(on[str(v)], node)
	await _check_combos()
	await _check_beams()


func _turn_radial(p: Dictionary, ring: String) -> void:
	if p.has("lock") and cond(p["lock"]):
		return
	game.busy = true
	var count := int(p.get("count", 4))
	var v := (int(State.flag_value(ring, 0)) + 1) % count
	State.set_flag(ring, v)
	game.play(p.get("sfx", "click"))
	var n := _part(ring)
	var step := deg_to_rad(float(p.get("rotate", -90)))
	var tw := create_tween()
	tw.tween_property(n, "rotation:z", step * (v if v != 0 else count), 0.18)
	await tw.finished
	n.rotation.z = step * v
	game.busy = false
	await _check_combos()


func _check_combos() -> void:
	for p in puzzles:
		if p["kind"] != "combo" or p.has("commit") or cond(p.get("lock")) and p.has("lock"):
			continue
		var ok := true
		for i in p["flags"].size():
			ok = ok and int(State.flag_value(p["flags"][i], -1)) == int(p["code"][i])
		if ok:
			await run(p["do"])


## Several combinations can share one commit part (an index lever that opens different drawers).
## The first whose code matches runs; if none does, the first one's "fail" runs.
func _commit_all(id: String, node: Node3D) -> void:
	var first := {}
	for p in puzzles:
		if p["kind"] != "combo" or p.get("commit", "") != id:
			continue
		if first.is_empty():
			first = p
		if p.has("lock") and cond(p["lock"]):
			continue
		var ok := true
		for i in p["flags"].size():
			ok = ok and int(State.flag_value(p["flags"][i], 0)) == int(p["code"][i])
		if ok:
			await run(p["do"], node)
			return
	await _commit(first, node)


## A combination with a commit part (a winding key, a catch, a lever) is only tried when the
## player works that part. A wrong try tells them nothing about which setting is wrong.
func _commit(p: Dictionary, node: Node3D) -> void:
	if p.has("lock") and cond(p["lock"]):
		if p.has("locked_say"):
			game.say(p["locked_say"])
		return
	var ok := true
	for i in p["flags"].size():
		var start = p.get("starts", {}).get(p["flags"][i], 0)
		ok = ok and int(State.flag_value(p["flags"][i], start)) == int(p["code"][i])
	if ok:
		await run(p["do"], node)
	else:
		await run(p.get("fail", [{"sfx": "thunk"}, {"say": "Nothing happens."}]), node)


func _pull(p: Dictionary, k: String) -> void:
	var pulled: String = State.flag_value(p["flag"], "")
	if (p.has("lock") and cond(p["lock"])) or (k in pulled and not p.get("repeat", false)):
		return   ## "repeat": true for notes, which can be played twice; levers can't be pulled twice
	pulled += k
	State.set_flag(p["flag"], pulled)
	game.play(p.get("sfx", "slide"), -4.0)
	await refresh(false)
	var order: String = p["order"]
	if p.get("silent", false):
		## Silent: nothing tells you you're wrong until the whole sequence is in.
		if pulled.length() < order.length():
			return
		if pulled == order:
			await run(p["do"])
			return
		game.busy = true
		await get_tree().create_timer(0.6).timeout
		State.set_flag(p["flag"], "")
		game.busy = false
		await run(p.get("fail", [{"sfx": "thunk"}, {"say": "They slide back into place."}]))
		return
	if not order.begins_with(pulled):
		game.busy = true
		await get_tree().create_timer(0.6).timeout
		State.set_flag(p["flag"], "")
		game.busy = false
		await run(p.get("fail", [{"sfx": "thunk"}, {"say": "They slide back into place."}]))
	elif pulled == order:
		await run(p["do"])


# ---------------- light beams ----------------
# A beam crosses a grid of cells drawn on one face of a box or furniture. It starts at a
# source cell, is turned by mirrors (cyclers with 4 states: / - \ |), stopped by blocks,
# and lights a target when it reaches it. Mirrors marked "lens" exist only through the Lens.

const DIRS := {"e": Vector2i(1, 0), "w": Vector2i(-1, 0), "n": Vector2i(0, -1), "s": Vector2i(0, 1)}
const OPP := {"e": "w", "w": "e", "n": "s", "s": "n"}
const TURN := [{"e": "n", "n": "e", "w": "s", "s": "w"}, {"e": "e", "w": "w"},
	{"e": "s", "s": "e", "w": "n", "n": "w"}, {"n": "n", "s": "s"}]
var beam_quads := {}     ## beam id -> {Vector3i(col, row, side) -> quad}
var _beam_running := false
var _combos_running := false


func _holder(name: String) -> PixelBox:
	if box_nodes.has(name):
		return box_nodes[name]
	return nodes[name]


func _cell_uv(p: Dictionary, c: int, r: int) -> Vector2:
	var cell := float(p.get("cell", 0.75))
	var ctr := _v2(p.get("center", [0, 0]))
	return ctr + Vector2((c - (int(p["cols"]) - 1) / 2.0) * cell, ((int(p["rows"]) - 1) / 2.0 - r) * cell)


func _build_beam(p: Dictionary) -> void:
	var b := _holder(p["box"])
	var face: MeshInstance3D = b.faces[p.get("face", "front")]
	var cell := float(p.get("cell", 0.75))
	var th := float(p.get("thick", 2.0)) / 16.0
	var glow: bool = p.get("additive", true)
	var th_h: Material = _additive(tex(p.get("tex_h", "glow_beam_h"))) if glow else PixelBox.make_material(tex(p.get("tex_h", "")))
	var th_v: Material = _additive(tex(p.get("tex_v", "glow_beam_v"))) if glow else PixelBox.make_material(tex(p.get("tex_v", "")))
	var q := {}
	for c in int(p["cols"]):
		for r in int(p["rows"]):
			var uv := _cell_uv(p, c, r)
			for side in ["n", "e", "s", "w"]:
				var horiz: bool = side in ["e", "w"]
				var quad := PixelBox.quad(Vector2(cell / 2, th) if horiz else Vector2(th, cell / 2), null)
				quad.material_override = th_h if horiz else th_v
				var d: Vector2i = DIRS[side]
				quad.position = Vector3(uv.x + d.x * cell / 4, uv.y - d.y * cell / 4, float(p.get("depth", 0.05)))
				quad.visible = false
				face.add_child(quad)
				q[Vector3i(c, r, ["n", "e", "s", "w"].find(side))] = quad
	beam_quads[p["id"]] = q


func _mirror_at(p: Dictionary, cell: Vector2i) -> int:
	for m in p.get("mirrors", []):
		if int(m[2]) == cell.x and int(m[3]) == cell.y:
			return int(State.flag_value(m[1], m[4] if m.size() > 4 else 0))
	for m in p.get("fixed", []):
		if int(m[0]) == cell.x and int(m[1]) == cell.y and (m.size() < 4 or game.lens_on):
			return int(m[2])
	return -1


## Follow the beam. Returns {"halves": [[col, row, side]], "hit": target index or -1}.
func _trace(p: Dictionary) -> Dictionary:
	var out := {"halves": [], "hit": -1}
	if not cond(p.get("when")):
		return out
	var src: Array = p["source"]
	var at := Vector2i(int(src[0]), int(src[1]))
	var d: String = src[2]
	out["halves"].append([at.x, at.y, d])
	var blocks := {}
	for bl in p.get("blocks", []):
		blocks[Vector2i(int(bl[0]), int(bl[1]))] = true
	for i in 200:
		at += DIRS[d]
		if at.x < 0 or at.y < 0 or at.x >= int(p["cols"]) or at.y >= int(p["rows"]):
			break
		out["halves"].append([at.x, at.y, OPP[d]])
		if blocks.has(at):
			break
		var hit := -1
		for t in p.get("targets", []).size():
			var tc: Array = p["targets"][t]["cell"]
			if int(tc[0]) == at.x and int(tc[1]) == at.y:
				hit = t
		if hit >= 0:
			out["hit"] = hit
			break
		var m := _mirror_at(p, at)
		if m >= 0:
			if not TURN[m].has(d):
				break
			d = TURN[m][d]
		out["halves"].append([at.x, at.y, d])
	return out


func _draw_beam(p: Dictionary) -> void:
	var q: Dictionary = beam_quads[p["id"]]
	for k in q:
		q[k].visible = false
	for h in _trace(p)["halves"]:
		q[Vector3i(h[0], h[1], ["n", "e", "s", "w"].find(h[2]))].visible = true


func _check_beams() -> void:
	if _beam_running:
		return
	_beam_running = true
	for p in puzzles:
		if p["kind"] != "beam":
			continue
		_draw_beam(p)
		var hit: int = _trace(p)["hit"]
		if hit >= 0:
			var t: Dictionary = p["targets"][hit]
			if not State.has(t["flag"]):
				State.set_flag(t["flag"])
				await run(t.get("do", []))
	_beam_running = false


func on_lens_changed() -> void:
	for p in puzzles:
		if p["kind"] == "beam":
			_draw_beam(p)
	await _check_beams()


# ---------------- rolling token (tilt maze) ----------------
# A pearl in a grid of cells. Tilting (tapping a button part) rolls it in that direction
# until a wall cell or the edge stops it. Reaching the goal runs "do" once.

func _roll_at(p: Dictionary) -> Vector2i:
	var s = State.flag_value(p["flag"], "")
	if s is String and "," in s:
		var a: PackedStringArray = s.split(",")
		return Vector2i(int(a[0]), int(a[1]))
	return Vector2i(int(p["start"][0]), int(p["start"][1]))


func _roll(p: Dictionary, dir: String, node: Node3D) -> void:
	if p.has("lock") and cond(p["lock"]):
		if p.has("locked_say"):
			game.say(p["locked_say"])
		return
	var walls := {}
	for w in p.get("walls", []):
		walls[Vector2i(int(w[0]), int(w[1]))] = true
	var at := _roll_at(p)
	var start := at
	while true:
		var nxt: Vector2i = at + DIRS[dir]
		if nxt.x < 0 or nxt.y < 0 or nxt.x >= int(p["cols"]) or nxt.y >= int(p["rows"]) or walls.has(nxt):
			break
		at = nxt
	if at == start:
		game.play("tick")
		game.shake(node)
		return
	game.busy = true
	State.set_flag(p["flag"], "%d,%d" % [at.x, at.y])
	game.play(p.get("sfx", "slide"), -2.0)
	var tok := _part(p["token"])
	var uv := _cell_uv(p, at.x, at.y)
	var tw := create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_property(tok, "position", Vector3(uv.x, uv.y, tok.position.z), 0.08 * (absi(at.x - start.x) + absi(at.y - start.y)) + 0.05)
	await tw.finished
	game.play("tick", -6.0)
	game.busy = false
	var g: Array = p["goal"]
	if at == Vector2i(int(g[0]), int(g[1])) and not State.has(p["done"]):
		State.set_flag(p["done"])
		await run(p.get("do", []))


# ---------------- toggle grid (lights out) ----------------
# Pressing a cell flips it and its four neighbours. Reach the goal pattern to run "do" once.

func _toggle(p: Dictionary, i: int, node: Node3D) -> void:
	if p.has("lock") and cond(p["lock"]):
		if p.has("locked_say"):
			game.say(p["locked_say"])
		return
	var cols := int(p["cols"])
	var rows := int(p["rows"])
	var bits: PackedByteArray = str(State.flag_value(p["flag"], p["start"])).to_ascii_buffer()
	var c := i % cols
	var r := i / cols
	for d in [Vector2i(0, 0), Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
		var cc: int = c + d.x
		var rr: int = r + d.y
		if cc >= 0 and rr >= 0 and cc < cols and rr < rows:
			var k := rr * cols + cc
			bits[k] = 49 if bits[k] == 48 else 48
	var s := bits.get_string_from_ascii()
	State.set_flag(p["flag"], s)
	game.play(p.get("sfx", "click"))
	await refresh(false)
	if s == p["goal"] and not State.has(p["done"]):
		State.set_flag(p["done"])
		await run(p.get("do", []), node)


func on_turned() -> void:
	State.flags["facing"] = "nesw"[game.view]   ## "facing=e": which wall you're looking at
	if data.has("street"):
		_walk_street()
	await refresh(false)
	set_lens(game.lens_on)


# ---------------- moves: rot and growth ----------------
# rot: once "watch" is set, it decays "after" moves later unless "until" holds; its "decay" actions run.
#   {"kind":"rot","watch":"root_cut","after":8,"until":"safe_open","decay":[actions]}
# grow: while "while" holds, "flag" goes up by one each move, up to "max".
#   {"kind":"grow","flag":"bean","while":"planted","max":5}
# The flag "rot_age" is the age of the oldest decaying part, for a wilting flower: "flower_{rot_age:4}".

func on_moved() -> void:
	var moves := int(State.flag_value("moves", 0))
	var oldest := 0
	var to_run: Array = []
	for p in puzzles:
		match p["kind"]:
			"rot":
				var key: String = p["watch"] + "@"
				if not State.has(p["watch"]) or (p.has("until") and cond(p["until"])):
					State.flags.erase(key)
					continue
				if not State.flags.has(key):
					State.flags[key] = moves
				var age := moves - int(State.flags[key])
				oldest = maxi(oldest, age)
				if age >= int(p["after"]):
					State.flags.erase(key)
					to_run.append(p)
			"tick":
				## {"kind":"tick","flag":"heat","every":6,"step":-1,"min":0}: the hut cools as you work
				if not cond(p.get("while")):
					continue   ## "while": the sand only runs while nobody is watching it
				var k: String = p["flag"] + "#"
				var cnt := int(State.flag_value(k, 0)) + 1
				if cnt >= int(p["every"]):
					cnt = 0
					var v := clampi(int(State.flag_value(p["flag"], 0)) + int(p.get("step", -1)), int(p.get("min", 0)), int(p.get("max", 99)))
					if v != int(State.flag_value(p["flag"], 0)):
						State.flags[p["flag"]] = v
						if p.has("say"):
							game.say(_fill(p["say"]), 3.0)
				State.flags[k] = cnt
			"grow":
				if cond(p.get("while")):
					State.flags[p["flag"]] = mini(int(State.flag_value(p["flag"], 0)) + 1, int(p.get("max", 99)))
	State.flags["rot_age"] = oldest
	State.save_game()
	for p in to_run:
		await run(p.get("decay", []))
	await refresh(false)
	set_lens(game.lens_on)


# ---------------- melody (the answering echo) ----------------
# Parts are notes ("parts": {"chime_0": "0", ...}, played as sfx tone_<note>). Play "order".
# A right note is answered, after a moment, by a faint echo of the NEXT right note.
# A wrong note resets quietly. "echo": false turns the echo off.

func _note(p: Dictionary, k: String) -> void:
	if p.has("lock") and cond(p["lock"]):
		game.play("tone_" + k)
		return
	var played: String = str(State.flag_value(p["flag"], "")) + k
	game.play("tone_" + k)
	var order: String = p["order"]
	if not order.begins_with(played):
		State.set_flag(p["flag"], "")
		if p.has("wrong"):
			await run(p["wrong"])
		if p.get("lead", false) and played.length() == 1:
			## the stone hums the first note before you find it
			await get_tree().create_timer(0.55).timeout
			_echo(p, order[0])
		return
	State.set_flag(p["flag"], played)
	if played == order:
		await get_tree().create_timer(0.5).timeout
		await run(p.get("do", []))
		return
	## "echo_from": n: the ice only answers once the first n notes are right (the part the score can't give you)
	if p.get("echo", true) and played.length() >= int(p.get("echo_from", 0)):
		await get_tree().create_timer(0.55).timeout
		_echo(p, order[played.length()])


## The echo: a faint note, and the part that makes it shivers, so it can be seen as well as heard.
func _echo(p: Dictionary, note: String) -> void:
	game.play("tone_" + note, -14.0)
	for id in p["parts"]:
		if p["parts"][id] == note:
			game.flash(_part(id))

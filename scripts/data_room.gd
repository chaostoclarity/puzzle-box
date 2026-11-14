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
	build_walls(data["walls"])
	for o in data.get("objects", []):
		_build_object(o)
	puzzles = data.get("puzzles", [])
	for s in data.get("steps", []):
		var spec: Dictionary = s
		steps.append({"id": spec["id"], "hints": spec["hints"], "said": spec.get("said", "It is done."),
			"done": func(): return cond(spec["done"]),
			"solve": func(): await run(spec["solve"])})
	walkthrough = _walkthrough(data.get("walkthrough", []))
	for a in data.get("on_enter", []):
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
			var b := add_furniture(o["wall"], o["id"], _v2(o["pos"]), _v3(o["size"]), _faces(o["faces"]), o.get("zoom", {}))
			nodes[o["id"]] = b
			_parts(b, o.get("parts", []))
		"sprite":
			var q := add_sprite(o["wall"], o["id"], _v2(o["center"]), _v2(o["size"]), o["tex"], o.get("depth", 0.03), o.get("tappable", true))
			if o.get("additive", false):
				var m := StandardMaterial3D.new()
				m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
				m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
				m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
				m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
				m.albedo_texture = tex(o["tex"])
				q.material_override = m
			if o.get("lens", false):
				q.add_to_group("lens_only")
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
		nodes[p["id"]] = part


func _walkthrough(w: Array) -> Array:
	var out: Array = []
	for a in w:
		if a[0] == "repeat":
			for i in int(a[1]):
				out.append(a[2])
		elif a[0] == "tapat":
			out.append(["tapat", a[1], Vector2(a[2][0], a[2][1])])
		else:
			out.append(a)
	return out


# ---------------- conditions ----------------

## "flag", "!flag", "item:x", "!item:x", "lens", "!lens", "flag=3", or an array of these (all must hold).
func cond(c) -> bool:
	if c == null:
		return true
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
	if "=" in s:
		var kv := s.split("=")
		return str(State.flag_value(kv[0], "")) == kv[1] or (str(kv[1]).is_valid_int() and int(State.flag_value(kv[0], -999)) == int(kv[1]))
	return State.has(s)


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
			"dark":
				var lit := State.has(p["until"])
				longest = maxf(longest, _apply_value("wall:" + p["wall"], "dim", 1.0 if lit else float(p.get("dim", 0.25)), animate, float(p.get("anim", 1.2)), 0.0))
	for b in data.get("bindings", []):
		var props: Dictionary = b.get("then", {}) if cond(b.get("when")) else b.get("else", {})
		for prop in props:
			longest = maxf(longest, _apply_value(b["target"], prop, props[prop], animate, float(b.get("anim", 0.0)), float(b.get("delay", 0.0))))
	if animate and longest > 0.0:
		await get_tree().create_timer(longest).timeout


func _cycler_visual(p: Dictionary, v: int) -> void:
	var n := _part(p["part"])
	if p.has("rotate"):
		n.rotation.z = deg_to_rad(float(p["rotate"])) * v
	if p.has("textures"):
		PixelBox.set_texture(n, tex(p["textures"][v]))


## Apply one property to one target. Returns how long its animation runs (0 if none).
func _apply_value(target: String, prop: String, value, animate: bool, anim: float, delay: float) -> float:
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
			"sequence":
				if p["parts"].has(id):
					await _pull(p, p["parts"][id])
					return true
			"pickup":
				if p["part"] == id:
					State.set_flag(p["flag"])
					State.add_item(p["item"])
					await run([{"sfx": p.get("sfx", "pickup")}] + p.get("then", []), node)
					return true
	for it in data.get("interactions", []):
		if it["on"] == "tap" and it["id"] == id and cond(it.get("when")):
			await run(it["do"], node)
			return it.get("handled", true)
	return false


func on_use(item: String, id: String, node: Node) -> bool:
	for it in data.get("interactions", []):
		if it["on"] == "use" and it["item"] == item and it["id"] == id and cond(it.get("when")):
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
		_cycler_visual(p, v)
		game.busy = false
		var on0: Dictionary = p.get("on", {})
		if on0.has(str(v)):
			await run(on0[str(v)], node)
		await _check_combos()
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
		if p["kind"] != "combo" or cond(p.get("lock")) and p.has("lock"):
			continue
		var ok := true
		for i in p["flags"].size():
			ok = ok and int(State.flag_value(p["flags"][i], -1)) == int(p["code"][i])
		if ok:
			await run(p["do"])


func _pull(p: Dictionary, k: String) -> void:
	var pulled: String = State.flag_value(p["flag"], "")
	if (p.has("lock") and cond(p["lock"])) or k in pulled:
		return
	pulled += k
	State.set_flag(p["flag"], pulled)
	game.play(p.get("sfx", "slide"), -4.0)
	await refresh(false)
	var order: String = p["order"]
	if not order.begins_with(pulled):
		game.busy = true
		await get_tree().create_timer(0.6).timeout
		State.set_flag(p["flag"], "")
		game.busy = false
		await run(p.get("fail", [{"sfx": "thunk"}, {"say": "They slide back into place."}]))
	elif pulled == order:
		await run(p["do"])

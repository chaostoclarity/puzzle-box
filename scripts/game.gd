## The Ninefold Seal: game controller.
## Three ways of looking:
##   ROOM  - one wall at a time, straight on. Drag sideways to turn to the next wall.
##   ZOOM  - a closer look at one piece of furniture.
##   BOX   - a hero box in your hands. Drag to turn it, it snaps to faces.
## Taps go to whatever you touch; with an item selected in the tray, you use it on what you touch.
extends Node3D

const PixelBox = preload("res://scripts/pixel_box.gd")
const DataRoom = preload("res://scripts/data_room.gd")
const STAGE := Vector3(500, 0, 0)
const SKIP_LABEL := "Skip to Seal II"
const HUD_TOP := 56.0
const HUD_BOTTOM := 76.0
const SNAP := PI / 2
const DRAG_PX_PER_TURN := 110.0
const LENS_COL := Color(0.72, 1.0, 0.9)
const INK := Color(0.91, 0.87, 0.77)
const DIM_INK := Color(0.62, 0.58, 0.5)
const BRASS := Color(0.86, 0.7, 0.33)

enum Mode { ROOM, ZOOM, BOX }

signal dialog_done(choice: String)

var camera: Camera3D
var ROOMS := {}            ## room number -> JSON path, from data/rooms/index.json
var stage: Node3D
var room
var mode := Mode.ROOM
var return_mode := Mode.ROOM
var view_size := Vector2(270, 480)
var view := 0
var pitch := 0             ## 0 = a wall, 1 = looking down at the floor, -1 = up at the ceiling
var busy := false
var modal := false
var lens_on := false
var selected := ""
var zoom_target: Node3D
var box_stack: Array = []
var hint_tier := {}
var idle := 0.0
var autotest := false
var last_hit := Vector3.ZERO
var test_fails: Array = []

var touch_down := false
var touch_start := Vector2.ZERO
var touch_time := 0
var drag_axis := Vector3.ZERO
var drag_angle := 0.0
var start_basis := Basis.IDENTITY
var start_rot := 0.0

var font: FontFile
var hud_root: Control
var top_bar: ColorRect
var back_btn: Label
var title_lbl: Label
var journal_btn: Label
var msg_lbl: Label
var lens_btn: Label
var hint_btn: Label
var tray_bg: ColorRect
var slots: Array = []
var lens_tint: ColorRect
var fade: ColorRect
var overlay_layer: CanvasLayer
var msg_tween: Tween

var sfx := {}
var players: Array = []
var drone: AudioStreamPlayer


func _ready() -> void:
	autotest = "--autotest" in OS.get_cmdline_user_args()
	var idx = JSON.parse_string(FileAccess.open("res://data/rooms/index.json", FileAccess.READ).get_as_text())
	for k in idx:
		ROOMS[int(k)] = "res://data/rooms/" + idx[k]
	camera = Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.keep_aspect = Camera3D.KEEP_WIDTH
	camera.far = 200.0
	add_child(camera)
	camera.current = true
	stage = Node3D.new()
	add_child(stage)
	_load_audio()
	_build_hud()
	get_tree().root.size_changed.connect(_fit_screen)
	_fit_screen()
	if autotest:
		State.saving = false
		State.reset()
		load_room(1)
		_autotest()
		return
	if OS.has_feature("web") and "seal=2" in str(JavaScriptBridge.eval("location.search")):
		drone.play()
		_skip_to_seal2()
		return
	var has_save := State.load_game()
	load_room(State.room if has_save else 1)
	_title_screen(has_save)


# ---------------- screen ----------------

## Biggest whole-number pixel scale that fits 270x480, then the view grows to fill the screen.
func _fit_screen() -> void:
	var win := Vector2(get_window().size)
	if win.x <= 0 or win.y <= 0:
		return
	var k := maxf(1.0, floorf(minf(win.x / 270.0, win.y / 480.0)))
	var v := Vector2i(int(win.x / k), int(win.y / k))
	get_tree().root.content_scale_size = v
	view_size = Vector2(v)
	if hud_root:
		_layout_hud()
	if room and not busy:
		_frame_camera(false)


func _content_center_offset() -> float:
	return ((view_size.y / 2.0) - (HUD_TOP + (view_size.y - HUD_TOP - HUD_BOTTOM) / 2.0))


## Camera size and position for the current mode. k = game pixels per texel.
func _camera_target() -> Dictionary:
	match mode:
		Mode.ROOM:
			var k := 1.0
			return {"size": view_size.x / (16.0 * k), "pos": Vector3(0, room.WALL_H / 2 - _content_center_offset() / (16.0 * k), 40)}
		Mode.ZOOM:
			return _zoom_frame(zoom_target)
		_:
			return {"size": view_size.x / 32.0, "pos": Vector3(STAGE.x, STAGE.y - _content_center_offset() / 32.0, 40)}


func _zoom_frame(t: Node3D) -> Dictionary:
	var z: Dictionary = t.get_meta("zoom", {})
	var dims: Vector3 = t.dims if t is PixelBox else Vector3(2, 2, 1)
	var center := t.global_position + Vector3(z.get("dx", 0.0), z.get("dy", 0.0), 0)
	var w: float = z.get("w", dims.x)
	var h: float = z.get("h", dims.y)
	var avail_h := view_size.y - HUD_TOP - HUD_BOTTOM
	var k := floorf(minf(view_size.x * 0.92 / (w * 16.0), avail_h * 0.92 / (h * 16.0)))
	k = clampf(z.get("k", k), 2.0, 4.0)
	var off := _content_center_offset() / (16.0 * k)
	return {"size": view_size.x / (16.0 * k), "pos": Vector3(center.x, center.y - off, 40)}


func _frame_camera(animate := true, dur := 0.35) -> void:
	var t := _camera_target()
	if not animate:
		camera.size = t["size"]
		camera.position = t["pos"]
		return
	var tw := create_tween().set_parallel().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(camera, "size", t["size"], dur)
	tw.tween_property(camera, "position", t["pos"], dur)
	await tw.finished


# ---------------- rooms ----------------

func load_room(n: int) -> void:
	if room:
		room.queue_free()
		room = null
	for c in stage.get_children():
		c.queue_free()
	State.room = n
	State.save_game()
	room = DataRoom.new()
	room.load_file(ROOMS[n])
	room.game = self
	add_child(room)
	room.build()
	room.index_ids()
	room.apply_state()
	mode = Mode.ROOM
	box_stack.clear()
	zoom_target = null
	view = 0
	pitch = 0
	_aim_room(0.0, 0.0)
	lens_on = false
	room.set_lens(false)
	lens_tint.visible = false
	selected = ""
	hint_tier.clear()
	title_lbl.text = room.title
	_refresh_hud()
	_frame_camera(false)
	if room.data.has("intro") and not autotest:
		say(room.data["intro"], 6.0)


func complete_room(next: int, card_title: String, card_text: String) -> void:
	busy = true
	await _fade_to(1.0, 0.8)
	if next in ROOMS:
		load_room(next)
		await _fade_to(0.0, 0.8)
		busy = false
		await _dialog(card_title, card_text, ["Continue"])
	else:
		busy = false
		var choice: String = await _dialog(card_title, card_text, ["Close", "Begin again"])
		if choice == "Begin again":
			State.reset()
			load_room(1)
		await _fade_to(0.0, 0.8)


func _fade_to(a: float, dur: float) -> void:
	fade.visible = true
	var tw := create_tween()
	tw.tween_property(fade, "color:a", a, dur)
	await tw.finished
	fade.visible = a > 0.0


# ---------------- input ----------------

func _process(delta: float) -> void:
	if room and room.pivot:
		for k in room.groups:
			var g: Node3D = room.groups[k]
			g.visible = g.global_transform.basis.z.z > 0.05
	if not modal:
		idle += delta
	if idle > 180.0 and hint_btn:
		hint_btn.modulate.a = 0.55 + 0.45 * sin(Time.get_ticks_msec() / 250.0)


func _input(event: InputEvent) -> void:
	if modal:
		return
	if event is InputEventScreenTouch:
		if event.pressed:
			touch_down = not busy
			touch_start = event.position
			touch_time = Time.get_ticks_msec()
			drag_axis = Vector3.ZERO
			drag_angle = 0.0
			if mode == Mode.BOX:
				start_basis = _active_box().transform.basis
			start_rot = view * SNAP
		elif touch_down:
			touch_down = false
			idle = 0.0
			if drag_axis != Vector3.ZERO:
				_finish_drag()
			elif event.position.distance_to(touch_start) < 10.0:
				_tap(event.position, Time.get_ticks_msec() - touch_time)
	elif event is InputEventScreenDrag and touch_down:
		var d: Vector2 = event.position - touch_start
		var in_play := touch_start.y > HUD_TOP and touch_start.y < view_size.y - HUD_BOTTOM
		if drag_axis == Vector3.ZERO and d.length() > 8.0 and in_play and mode != Mode.ZOOM:
			if mode == Mode.ROOM:
				var vertical := absf(d.y) > absf(d.x)
				if pitch != 0 and not vertical:
					touch_down = false
					return
				drag_axis = Vector3.RIGHT if vertical else Vector3.UP
			else:
				drag_axis = Vector3.UP if absf(d.x) > absf(d.y) else Vector3.RIGHT
		if drag_axis != Vector3.ZERO:
			var px := d.x if drag_axis == Vector3.UP else d.y
			drag_angle = clampf(px / DRAG_PX_PER_TURN * SNAP, -SNAP, SNAP)
			if mode == Mode.ROOM:
				if drag_axis == Vector3.UP:
					_aim_room(start_rot - drag_angle, 0.0)
				else:
					_aim_room(start_rot, _pitch_limit(pitch * SNAP - drag_angle))
			else:
				_active_box().transform.basis = Basis(drag_axis, drag_angle) * start_basis


func _finish_drag() -> void:
	var target := roundf(drag_angle / SNAP) * SNAP
	if target == 0.0 and absf(drag_angle) > PI / 6.0:
		target = signf(drag_angle) * SNAP
	if absf(target) > 0.0:
		play("turn")
	busy = true
	var tw := create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	if mode == Mode.ROOM and drag_axis == Vector3.RIGHT:
		var p0 := pitch * SNAP
		target = _pitch_limit(p0 - target) 
		var from := _pitch_limit(p0 - drag_angle)
		tw.tween_method(func(a: float): _aim_room(start_rot, a), from, target, 0.22)
		await tw.finished
		pitch = int(roundf(target / SNAP))
		_aim_room(view * SNAP, pitch * SNAP)
	elif mode == Mode.ROOM:
		tw.tween_method(func(a: float): _aim_room(start_rot - a, 0.0), drag_angle, target, 0.22)
		await tw.finished
		view = posmod(int(roundf((start_rot - target) / SNAP)), 4)
		_aim_room(view * SNAP, 0.0)
	else:
		var b := _active_box()
		var axis := drag_axis
		var base := start_basis
		tw.tween_method(func(a: float): b.transform.basis = Basis(axis, a) * base, drag_angle, target, 0.22)
		await tw.finished
		b.transform.basis = _snap_basis(b.transform.basis)
	busy = false


func _snap_basis(b: Basis) -> Basis:
	var o := b.orthonormalized()
	for i in 3:
		var v := o[i]
		o[i] = Vector3(roundf(v.x), roundf(v.y), roundf(v.z))
	return o


func set_view(v: int) -> void:
	view = posmod(v, 4)
	pitch = 0
	_aim_room(view * SNAP, 0.0)


## Look down at the floor (1), up at the ceiling (-1) or straight at a wall (0).
func set_pitch(p: int) -> void:
	pitch = p
	_aim_room(view * SNAP, pitch * SNAP)


## Turn the room: yaw picks the wall, pitch tips it to show the floor or ceiling.
func _aim_room(yaw: float, pitch_angle: float) -> void:
	room.pivot.transform.basis = Basis(Vector3.RIGHT, pitch_angle) * Basis(Vector3.UP, yaw)


## Clamp a pitch angle to the faces this room has.
func _pitch_limit(a: float) -> float:
	var lo := -SNAP if room.groups.has(room.CEILING) else 0.0
	var hi := SNAP if room.groups.has(room.FLOOR) else 0.0
	return clampf(a, lo, hi)


func _tap(pos: Vector2, held_ms := 0) -> void:
	if busy:
		return
	if _hud_tap(pos, held_ms):
		return
	if pos.y < HUD_TOP or pos.y > view_size.y - HUD_BOTTOM:
		return
	var hit := _pick(pos)
	if hit.is_empty():
		return
	var id: String = hit.collider.get_meta("id", "")
	var node: Node3D = hit.collider.get_parent()
	last_hit = hit.position
	if id == "":
		return
	# lift a hero box into your hands
	var lift := _liftable(node)
	if lift != "" and mode != Mode.BOX:
		if await room.on_tap("lift:" + lift, node):
			return
		await enter_box(lift)
		return
	# dive into a nested box
	if id.begins_with("dive:"):
		if await room.on_tap(id, node):
			return
		await dive(node, id.substr(5))
		return
	if selected != "":
		var item := selected
		if await room.on_use(item, id, node):
			flash(node)
			if not State.has_item(item):
				selected = ""
			_refresh_hud()
		else:
			play("nope")
			say("That doesn't work there.")
		return
	if await room.on_tap(id, node):
		return
	if node.has_meta("zoom") and (mode != Mode.ZOOM or zoom_target != node):
		await zoom_to(node)


## Ray from the screen into the world. Things on walls turned away from you are skipped.
func _pick(pos: Vector2) -> Dictionary:
	var from := camera.project_ray_origin(pos)
	var to := from + camera.project_ray_normal(pos) * 150.0
	var q := PhysicsRayQueryParameters3D.create(from, to)
	var exclude: Array[RID] = []
	for i in 12:
		q.exclude = exclude
		var hit := get_world_3d().direct_space_state.intersect_ray(q)
		if hit.is_empty():
			return {}
		if not (hit.collider.get_parent() as Node3D).is_visible_in_tree():
			exclude.append(hit.rid)
			continue
		if mode == Mode.BOX:
			return hit
		var w: String = room.wall_of(hit.collider)
		if w == "" or room.wall_facing(w):
			return hit
		exclude.append(hit.rid)
	return {}


func _liftable(node: Node) -> String:
	var n := node
	while n and n != room:
		if n.has_meta("liftable"):
			return n.get_meta("liftable")
		n = n.get_parent()
	return ""


func zoom_to(node: Node3D) -> void:
	busy = true
	zoom_target = node
	mode = Mode.ZOOM
	play("turn")
	_refresh_hud()
	await _frame_camera(true)
	busy = false


func go_back() -> void:
	if busy:
		return
	busy = true
	if mode == Mode.BOX:
		if box_stack.size() > 1:
			var inner: Node3D = _active_box()
			box_stack.pop_back()
			await _fade_to(1.0, 0.12)
			inner.visible = false
			_active_box().visible = true
			_frame_camera(false)
			await _fade_to(0.0, 0.12)
		else:
			await exit_box()
	elif mode == Mode.ZOOM:
		mode = Mode.ROOM
		zoom_target = null
		await _frame_camera(true)
	busy = false
	_refresh_hud()


# ---------------- boxes ----------------

func _active_box() -> PixelBox:
	return room.boxes[box_stack.back()]["box"]


func enter_box(name: String) -> void:
	busy = true
	var info: Dictionary = room.boxes[name]
	var b: PixelBox = info["box"]
	return_mode = mode
	await _fade_to(1.0, 0.15)
	b.get_parent().remove_child(b)
	stage.add_child(b)
	b.transform = Transform3D(Basis.from_euler(PixelBox.FACE_VIEW[info["view"]] * (PI / 180.0)), STAGE)
	b.visible = true
	box_stack = [name]
	mode = Mode.BOX
	room.on_box_mode(name, true)
	_frame_camera(false)
	_refresh_hud()
	play("pickup")
	await _fade_to(0.0, 0.15)
	busy = false


func exit_box() -> void:
	busy = true
	await _fade_to(1.0, 0.15)
	for name in box_stack:
		var info: Dictionary = room.boxes[name]
		var b: PixelBox = info["box"]
		if info.get("stage_only", false):
			b.visible = false
		else:
			b.get_parent().remove_child(b)
			(info["home_parent"] as Node).add_child(b)
			b.transform = info["home_xform"]
			b.visible = true
		room.on_box_mode(name, false)
	box_stack.clear()
	mode = return_mode if return_mode != Mode.BOX else Mode.ROOM
	if mode == Mode.ZOOM and not is_instance_valid(zoom_target):
		mode = Mode.ROOM
	_frame_camera(false)
	_refresh_hud()
	await _fade_to(0.0, 0.15)
	busy = false


## Zoom into a small box nested inside the one in your hands, then swap in its full-size twin.
## A camera zoomed to the small box's scale sees exactly what a normal camera sees of the big one.
func dive(mini: Node3D, name: String) -> void:
	busy = true
	var s := mini.global_transform.basis.get_scale().x
	var gp := mini.global_position
	play("whisper", -14.0)
	var tw := create_tween().set_parallel().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(camera, "size", camera.size * s, 0.9)
	tw.tween_property(camera, "position", Vector3(gp.x, gp.y - _content_center_offset() / 32.0 * s, camera.position.z), 0.9)
	await tw.finished
	var gb := _snap_basis(mini.global_transform.basis)
	_active_box().visible = false
	var b: PixelBox = room.boxes[name]["box"]
	b.transform = Transform3D(gb, STAGE)
	b.visible = true
	box_stack.append(name)
	_frame_camera(false)
	_refresh_hud()
	await show_face(room.boxes[name]["view"])
	busy = false


## Turn the box in your hands to show one face (animated).
func show_face(face: String) -> void:
	var b := _active_box()
	var target := Basis.from_euler(PixelBox.FACE_VIEW[face] * (PI / 180.0))
	var q0 := b.transform.basis.get_rotation_quaternion()
	var q1 := target.get_rotation_quaternion()
	var tw := create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	tw.tween_method(func(t: float): b.transform.basis = Basis(q0.slerp(q1, t)), 0.0, 1.0, 0.7)
	await tw.finished
	b.transform.basis = _snap_basis(b.transform.basis)


# ---------------- juice ----------------

func flash(node: Node) -> void:
	if not node is MeshInstance3D or not node.material_override is ShaderMaterial:
		return
	var m: ShaderMaterial = node.material_override
	var tw := create_tween()
	tw.tween_method(func(v: float): m.set_shader_parameter("highlight", v), 0.3, 0.0, 0.3)


func shake(node: Node3D) -> void:
	var x := node.position.x
	var tw := create_tween()
	for o in [0.08, -0.08, 0.05, -0.03, 0.0]:
		tw.tween_property(node, "position:x", x + o, 0.04)
	play("nope", -6.0)


func say(text: String, secs := 3.5) -> void:
	msg_lbl.text = text
	msg_lbl.modulate.a = 1.0
	if msg_tween:
		msg_tween.kill()
	msg_tween = create_tween()
	msg_tween.tween_interval(secs)
	msg_tween.tween_property(msg_lbl, "modulate:a", 0.0, 0.6)


func toggle_lens() -> void:
	lens_on = not lens_on
	room.set_lens(lens_on)
	lens_tint.visible = lens_on
	play("lens")
	_refresh_hud()
	room.on_lens_changed()


# ---------------- audio ----------------

func _load_audio() -> void:
	for n in ["click", "tick", "unlock", "slide", "thunk", "paper", "match", "pickup", "turn", "door", "nope", "whisper", "lens", "reveal",
			"water", "hum", "horn", "flame", "creak"]:
		sfx[n] = load("res://assets/sfx/%s.wav" % n)
	for i in 6:
		var p := AudioStreamPlayer.new()
		add_child(p)
		players.append(p)
	drone = AudioStreamPlayer.new()
	drone.stream = load("res://assets/sfx/drone.wav")
	drone.volume_db = -10.0
	add_child(drone)
	drone.finished.connect(drone.play)


func play(n: String, db := 0.0) -> void:
	if not sfx.has(n):
		return
	for p in players:
		if not p.playing:
			p.stream = sfx[n]
			p.volume_db = db
			p.play()
			return


# ---------------- HUD ----------------

func _label(text: String, size := 16, col := INK) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_override("font", font)
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", col)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return l


func _build_hud() -> void:
	font = load("res://assets/fonts/VT323.ttf")
	font.antialiasing = TextServer.FONT_ANTIALIASING_NONE
	font.hinting = TextServer.HINTING_NONE
	font.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED

	var lens_layer := CanvasLayer.new()
	lens_layer.layer = 1
	add_child(lens_layer)
	lens_tint = ColorRect.new()
	lens_tint.color = LENS_COL
	var mat := CanvasItemMaterial.new()
	mat.blend_mode = CanvasItemMaterial.BLEND_MODE_MUL
	lens_tint.material = mat
	lens_tint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	lens_tint.visible = false
	lens_layer.add_child(lens_tint)

	var hud := CanvasLayer.new()
	hud.layer = 2
	add_child(hud)
	hud_root = Control.new()
	hud_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(hud_root)

	top_bar = ColorRect.new()
	top_bar.color = Color(0.06, 0.045, 0.04, 0.92)
	top_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud_root.add_child(top_bar)
	back_btn = _label("< Back", 16, BRASS)
	hud_root.add_child(back_btn)
	title_lbl = _label("", 16, INK)
	title_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hud_root.add_child(title_lbl)
	journal_btn = _label("Journal", 16, BRASS)
	journal_btn.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	hud_root.add_child(journal_btn)
	msg_lbl = _label("", 16, INK)
	msg_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	msg_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hud_root.add_child(msg_lbl)

	tray_bg = ColorRect.new()
	tray_bg.color = Color(0.06, 0.045, 0.04, 0.92)
	tray_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud_root.add_child(tray_bg)
	lens_btn = _label("[ Lens ]", 16, LENS_COL)
	hud_root.add_child(lens_btn)
	hint_btn = _label("[ Hint ]", 16, BRASS)
	hint_btn.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	hud_root.add_child(hint_btn)
	for i in 8:
		var frame := ColorRect.new()
		frame.size = Vector2(30, 30)
		frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var inner := ColorRect.new()
		inner.color = Color(0.03, 0.02, 0.02)
		inner.position = Vector2(1, 1)
		inner.size = Vector2(28, 28)
		inner.mouse_filter = Control.MOUSE_FILTER_IGNORE
		frame.add_child(inner)
		var icon := TextureRect.new()
		icon.position = Vector2(3, 3)
		icon.size = Vector2(24, 24)
		icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
		frame.add_child(icon)
		hud_root.add_child(frame)
		slots.append({"frame": frame, "icon": icon})

	overlay_layer = CanvasLayer.new()
	overlay_layer.layer = 5
	add_child(overlay_layer)
	var fade_layer := CanvasLayer.new()
	fade_layer.layer = 4
	add_child(fade_layer)
	fade = ColorRect.new()
	fade.color = Color(0, 0, 0, 0)
	fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	fade.visible = false
	fade_layer.add_child(fade)
	State.changed.connect(_refresh_hud)


func _layout_hud() -> void:
	var vs := view_size
	lens_tint.size = vs
	fade.size = vs
	top_bar.size = Vector2(vs.x, 22)
	back_btn.position = Vector2(4, 2)
	title_lbl.position = Vector2(0, 2)
	title_lbl.size = Vector2(vs.x, 18)
	journal_btn.position = Vector2(vs.x - 64, 2)
	journal_btn.size = Vector2(60, 18)
	msg_lbl.position = Vector2(8, 24)
	msg_lbl.size = Vector2(vs.x - 16, 32)
	tray_bg.position = Vector2(0, vs.y - HUD_BOTTOM)
	tray_bg.size = Vector2(vs.x, HUD_BOTTOM)
	lens_btn.position = Vector2(6, vs.y - HUD_BOTTOM + 2)
	hint_btn.position = Vector2(vs.x - 70, vs.y - HUD_BOTTOM + 2)
	hint_btn.size = Vector2(64, 18)
	var x0 := (vs.x - (8 * 33 - 3)) / 2.0
	for i in 8:
		(slots[i]["frame"] as ColorRect).position = Vector2(x0 + i * 33, vs.y - 38)


func _refresh_hud() -> void:
	if not hud_root:
		return
	back_btn.visible = mode != Mode.ROOM
	title_lbl.visible = mode == Mode.ROOM
	lens_btn.visible = State.has_item("lens")
	lens_btn.text = "[ Lens: on ]" if lens_on else "[ Lens ]"
	for i in 8:
		var frame: ColorRect = slots[i]["frame"]
		var icon: TextureRect = slots[i]["icon"]
		if i < State.inventory.size():
			var item: String = State.inventory[i]
			icon.texture = load("res://assets/rooms/item_%s.png" % item)
			frame.color = BRASS if item == selected else Color(0.35, 0.24, 0.14)
		else:
			icon.texture = null
			frame.color = Color(0.18, 0.13, 0.09)


func _rect(c: Control, grow := 6.0) -> Rect2:
	return Rect2(c.position, c.size).grow(grow)


func _hud_tap(pos: Vector2, held_ms: int) -> bool:
	if back_btn.visible and _rect(back_btn).has_point(pos):
		play("click")
		go_back()
		return true
	if _rect(journal_btn).has_point(pos):
		play("paper")
		open_journal()
		return true
	if lens_btn.visible and _rect(lens_btn).has_point(pos):
		toggle_lens()
		return true
	if _rect(hint_btn).has_point(pos):
		play("click")
		hint_btn.modulate.a = 1.0
		ask_hint()
		return true
	for i in 8:
		var frame: ColorRect = slots[i]["frame"]
		if _rect(frame, 1.5).has_point(pos):
			if i < State.inventory.size():
				var item: String = State.inventory[i]
				if held_ms > 450:
					examine(item)
				else:
					select_item("" if selected == item else item)
			return true
	return pos.y > view_size.y - HUD_BOTTOM or pos.y < 22


func select_item(item: String) -> void:
	selected = item
	play("click")
	if item != "":
		say("%s. Touch where to use it. Hold an item to examine it." % State.ITEMS[item][0])
	_refresh_hud()


# ---------------- hints and bargains ----------------

func ask_hint() -> void:
	idle = 0.0
	var s: Dictionary = room.current_step()
	if s.is_empty():
		say("There is nothing more to find here.")
		return
	var t: int = hint_tier.get(s["id"], 0)
	if t < 2:
		say(s["hints"][t], 6.0)
		hint_tier[s["id"]] = t + 1
		return
	play("whisper")
	var choice: String = await _dialog("The Whisper",
		"A voice behind your eyes, patient as deep water:\n\n\"Let me. It is a small thing. It will cost you one page.\"",
		["Accept", "Refuse"])
	if choice == "Accept":
		await bargain(s)


func bargain(s: Dictionary) -> void:
	State.bargains += 1
	var torn := State.tear_page()
	if mode == Mode.BOX:
		await exit_box()
	await (s["solve"] as Callable).call()
	room.apply_state()
	if lens_on:
		room.set_lens(true)
	_refresh_hud()
	play("whisper", -6.0)
	say(s.get("said", "It is done.") + (" A page is gone: %s." % torn if torn != "" else ""), 6.0)


# ---------------- overlays ----------------

func _overlay_root() -> Control:
	var root := Control.new()
	root.size = view_size
	var bg := ColorRect.new()
	bg.color = Color(0.03, 0.02, 0.025, 0.94)
	bg.size = view_size
	root.add_child(bg)
	overlay_layer.add_child(root)
	modal = true
	return root


func _button(parent: Control, text: String, pos: Vector2, w := 120.0) -> Button:
	var b := Button.new()
	b.text = text
	b.position = pos
	b.size = Vector2(w, 24)
	b.add_theme_font_override("font", font)
	b.add_theme_font_size_override("font_size", 16)
	b.add_theme_color_override("font_color", BRASS)
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.12, 0.08, 0.06)
	sb.border_color = BRASS
	sb.set_border_width_all(1)
	b.add_theme_stylebox_override("normal", sb)
	b.add_theme_stylebox_override("hover", sb)
	b.add_theme_stylebox_override("pressed", sb)
	b.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	parent.add_child(b)
	return b


func _close_overlay(root: Control) -> void:
	root.queue_free()
	modal = false
	touch_down = false


## A modal card with a title, some text and buttons. Returns the chosen button's text.
func _dialog(title: String, text: String, buttons: Array) -> String:
	var root := _overlay_root()
	var t := _label(title, 16, BRASS)
	t.position = Vector2(12, 90)
	t.size = Vector2(view_size.x - 24, 20)
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(t)
	var body := _label(text, 16, INK)
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body.custom_minimum_size = Vector2(view_size.x - 32, 0)
	body.position = Vector2(16, 120)
	body.size = Vector2(view_size.x - 32, 220)
	body.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(body)
	var y := 350.0
	for b in buttons:
		var btn := _button(root, b, Vector2((view_size.x - 160) / 2, y), 160)
		btn.pressed.connect(func(): dialog_done.emit(b))
		y += 32
	if autotest:
		get_tree().create_timer(0.6).timeout.connect(func():
			await _shot("card_" + title.to_lower().replace(" ", "_"))
			dialog_done.emit(buttons[0]))
	var choice: String = await dialog_done
	play("click")
	_close_overlay(root)
	return choice


func _title_screen(has_save: bool) -> void:
	var text := "Arkham, Massachusetts. Winter, 1927.\n\nProfessor Hollis Wren has vanished from his locked study. He left you a black cabinet with nine seals, and a letter.\n\nDrag sideways to turn to the next wall, up or down to look at the floor and ceiling. Touch things to examine them."
	var buttons := ["Continue", "Start over"] if has_save else ["Begin"]
	buttons.append(SKIP_LABEL)
	var choice: String = await _dialog("THE NINEFOLD SEAL", text, buttons)
	drone.play()
	if choice == SKIP_LABEL:
		_skip_to_seal2()
		return
	if choice == "Start over":
		State.reset()
		load_room(1)
	if choice != "Continue":
		say("Wren's study. The door is locked from the inside.", 5.0)


## Playtest shortcut: start seal II as if seal I were done. Also reachable with ?seal=2 in the URL.
func _skip_to_seal2() -> void:
	State.reset()
	State.inventory = ["lens", "seal_stone"]
	State.fragments = 1
	load_room(101)
	say("Thorne's study, after the first seal.", 5.0)


func open_journal() -> void:
	var root := _overlay_root()
	var t := _label("Journal of Elias Thorne", 16, BRASS)
	t.position = Vector2(10, 6)
	root.add_child(t)
	var scroll := ScrollContainer.new()
	scroll.position = Vector2(8, 30)
	scroll.size = Vector2(view_size.x - 16, view_size.y - 80)
	root.add_child(scroll)
	var box := VBoxContainer.new()
	box.custom_minimum_size = Vector2(view_size.x - 28, 0)
	box.add_theme_constant_override("separation", 6)
	scroll.add_child(box)
	if State.journal.is_empty():
		box.add_child(_label("Nothing yet.", 16, DIM_INK))
	for i in range(State.journal.size() - 1, -1, -1):
		var e: Dictionary = State.journal[i]
		var h := _label(e["title"], 16, BRASS)
		box.add_child(h)
		var body := _label("[This page has been torn out.]" if e["torn"] else e["text"], 16, DIM_INK if e["torn"] else INK)
		body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		body.custom_minimum_size = Vector2(view_size.x - 32, 0)
		box.add_child(body)
	if State.bargains > 0:
		box.add_child(_label("Bargains made: %d" % State.bargains, 16, Color(0.5, 0.9, 0.8)))
	var close := _button(root, "Close", Vector2(8, view_size.y - 40), 110)
	close.pressed.connect(func(): _close_overlay(root))
	var reset := _button(root, "Start over", Vector2(view_size.x - 118, view_size.y - 40), 110)
	reset.pressed.connect(func():
		_close_overlay(root)
		var c: String = await _dialog("Start over?", "Everything you have done will be forgotten.", ["Keep playing", "Erase it all"])
		if c == "Erase it all":
			State.reset()
			load_room(1))
	if autotest:
		await get_tree().create_timer(0.4).timeout
		await RenderingServer.frame_post_draw
		await _shot("journal")
		_close_overlay(root)


func examine(item: String) -> void:
	play("paper")
	var root := _overlay_root()
	var big := "res://assets/rooms/examine_%s.png" % item
	var texr := TextureRect.new()
	texr.texture = load(big) if ResourceLoader.exists(big) else load("res://assets/rooms/item_%s.png" % item)
	var k := floorf(minf((view_size.x - 40) / texr.texture.get_width(), 160.0 / texr.texture.get_height()))
	texr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	texr.size = texr.texture.get_size() * k
	texr.position = Vector2((view_size.x - texr.size.x) / 2, 90)
	root.add_child(texr)
	var name := _label(State.ITEMS[item][0], 16, BRASS)
	name.position = Vector2(10, 270)
	name.size = Vector2(view_size.x - 20, 18)
	name.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(name)
	var desc := _label(State.ITEMS[item][1], 16, INK)
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	desc.custom_minimum_size = Vector2(view_size.x - 32, 0)
	desc.position = Vector2(16, 294)
	desc.size = Vector2(view_size.x - 32, 120)
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(desc)
	var close := _button(root, "Put it away", Vector2((view_size.x - 140) / 2, 420), 140)
	close.pressed.connect(func(): _close_overlay(root))
	if autotest:
		await get_tree().create_timer(0.4).timeout
		await _shot("examine_" + item)
		_close_overlay(root)


# ---------------- automated playthrough ----------------
# Run: godot --path . -- --autotest   (screenshots go to user://shots)
# Plays both rooms with real taps: each target is brought into view, projected to the
# screen and tapped through the same code path a finger uses.

func _shot(n: String) -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("user://shots")
	get_viewport().get_texture().get_image().save_png("user://shots/%s.png" % n)
	print("shot ", n)


func _wait(s: float) -> void:
	await get_tree().create_timer(s).timeout
	while busy:
		await get_tree().process_frame


func _box_of(node: Node) -> String:
	for name in room.boxes:
		var b: Node = room.boxes[name]["box"]
		if b == node or b.is_ancestor_of(node):
			return name
	return ""


func _face_of(node: Node, b: PixelBox) -> String:
	for f in b.faces:
		var q: Node = b.faces[f]
		if q == node or q.is_ancestor_of(node):
			return f
	return ""


## Bring a target into view the way a player would, then tap it on screen.
func test_tap(id: String, offset := Vector2.ZERO) -> void:
	await _wait(0.05)
	if not room.ids.has(id):
		test_fails.append("no target " + id)
		return
	var node: Node3D = room.ids[id]
	var bname := _box_of(node)
	var box_part := bname != "" and not node.has_meta("liftable")
	if box_part:
		if not (mode == Mode.BOX and box_stack.back() == bname):
			if mode == Mode.BOX and bname in box_stack:
				while box_stack.back() != bname:
					await go_back()
			else:
				if room.boxes[bname].get("stage_only", false):
					test_fails.append("unreachable %s (inside %s)" % [id, bname])
					return
				if mode == Mode.BOX:
					await exit_box()
				await enter_box(bname)
		var f := _face_of(node, room.boxes[bname]["box"])
		if f == "" and node.has_meta("face"):
			f = node.get_meta("face")
		if f != "" and not id.begins_with("dive:"):
			await show_face(f)
	else:
		if mode == Mode.BOX:
			await exit_box()
		if mode == Mode.ZOOM:
			mode = Mode.ROOM
			zoom_target = null
			_frame_camera(false)
		var w: String = room.wall_of(node)
		if w == room.FLOOR or w == room.CEILING:
			set_view(0)
			set_pitch(1 if w == room.FLOOR else -1)
		elif w != "":
			set_view(room.WALLS.find(w))
	await _wait(0.1)
	var pos := camera.unproject_position(node.global_transform * Vector3(offset.x, offset.y, 0))
	await _tap(pos)
	await _wait(0.35)


func _swipe(dx: float) -> void:
	var c := view_size / 2
	var ft := get_viewport().get_final_transform()
	var ev := InputEventScreenTouch.new()
	ev.position = ft * c
	ev.pressed = true
	ev.set_meta("test", true)
	Input.parse_input_event(ev)
	for i in range(1, 7):
		var dr := InputEventScreenDrag.new()
		dr.position = ft * (c + Vector2(dx * i / 6.0, 0))
		dr.set_meta("test", true)
		Input.parse_input_event(dr)
		await get_tree().process_frame
	var up := InputEventScreenTouch.new()
	up.position = ft * (c + Vector2(dx, 0))
	up.pressed = false
	up.set_meta("test", true)
	Input.parse_input_event(up)
	await _wait(0.4)


func _autotest() -> void:
	await _wait(0.6)
	var done_rooms := {}
	while true:
		var n: int = State.room
		if done_rooms.has(n):
			break
		done_rooms[n] = true
		for a in room.walkthrough:
			match a[0]:
				"tap": await test_tap(a[1])
				"use":
					if not State.has_item(a[1]):
						test_fails.append("not holding %s for %s" % [a[1], a[2]])
					selected = a[1]
					_refresh_hud()
					await test_tap(a[2])
					selected = ""
					_refresh_hud()
				"tapat": await test_tap(a[1], a[2])
				"expect":
					if not State.has(a[1]):
						test_fails.append("expected flag " + a[1])
				"shot": await _shot("%d_%s" % [n, a[1]])
				"lens":
					if lens_on != a[1]:
						toggle_lens()
					await _wait(0.2)
				"back":
					await go_back()
					await _wait(0.2)
				"face": await show_face(a[1])
				"swipe": await _swipe(a[1])
				"hint":
					await ask_hint()
					await _wait(0.2)
				"examine": await examine(a[1])
				"journal": await open_journal()
				"wait": await _wait(a[1])
		var waited := 0.0
		while (State.room == n or busy or modal) and waited < 10.0:
			await _wait(0.25)
			waited += 0.25
		if State.room == n:
			break
		await _wait(1.0)
	await _shot("final")
	print("AUTOTEST DONE room=%d bargains=%d items=%s" % [State.room, State.bargains, str(State.inventory)])
	print("AUTOTEST FAILS: %d %s" % [test_fails.size(), str(test_fails)])
	get_tree().quit()

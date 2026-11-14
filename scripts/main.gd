## Puzzle Box prototype, level 1.
## Controls (touch, or mouse on desktop):
##   Drag   - the box follows your finger, then snaps to the nearest face (90 degrees).
##   Tap    - touch a part: turn a dial, try the panel, take the key, use the lock.
##   Tap the key slot at the bottom to select the key, then tap the lock.
## Puzzle chain: clue on the back -> dials on the left -> panel on the right slides open
##   -> key -> lock on the front -> lid opens -> tap the inner box to dive into it.
extends Node3D

const PixelBox := preload("res://scripts/pixel_box.gd")
const SYMS := ["sun", "moon", "star", "eye"]
const CODE := [1, 3, 2]            # moon, eye, star (painted on the back face)
const BASE := Vector2(270, 480)     # minimum view, in game pixels
const PX_PER_UNIT := 32.0          # 2 game pixels per texel at 16 texels per unit
const SNAP := PI / 2
const DRAG_PX_PER_TURN := 110.0    # finger travel for a full 90 degree turn
const HUD_H := 48.0

var tex := {}
var cam_width := 270.0 / 32.0
var camera: Camera3D
var pivot: Node3D          # the box currently in your hands
var box                    # outer PixelBox
var inner                  # nested PixelBox

var busy := false
var touch_down := false
var touch_start := Vector2.ZERO
var drag_axis := Vector3.ZERO
var drag_angle := 0.0
var start_basis := Basis.IDENTITY

var dials: Array[MeshInstance3D] = []
var dial_vals := [0, 0, 0]
var panel: MeshInstance3D
var key_part: MeshInstance3D
var lock_part: MeshInstance3D
var has_key := false
var key_selected := false
var panel_open := false
var lid_open := false
var nested := false

var hud: CanvasLayer
var hud_bar: ColorRect
var slot_frame: ColorRect
var slot_icon: TextureRect
var hint: Label
var hint_tween: Tween


func _ready() -> void:
	for n in ["outer_front", "outer_back", "outer_left", "outer_right", "outer_top", "outer_bottom",
			"inner_front", "inner_back", "inner_left", "inner_right", "inner_top", "inner_bottom",
			"liner", "panel", "key", "lock", "lock_open",
			"dial_sun", "dial_moon", "dial_star", "dial_eye"]:
		tex[n] = load("res://assets/%s.png" % n)

	camera = Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.keep_aspect = Camera3D.KEEP_WIDTH
	camera.size = cam_width
	camera.position = Vector3(0, 0, 20)
	camera.far = 60.0
	add_child(camera)
	camera.current = true

	box = PixelBox.new()
	add_child(box)
	box.build(_faces("outer"), 6.0, true, tex["liner"])
	pivot = box

	lock_part = box.add_part("front", Vector2(0, -1.2), Vector2(1.5, 1.5), tex["lock"], "lock")
	for i in 3:
		dials.append(box.add_part("left", Vector2((i - 1) * 1.6, 0), Vector2(1.25, 1.25), tex["dial_sun"], "dial%d" % i))
	key_part = box.add_part("right", Vector2(0, -0.5), Vector2(2, 2), tex["key"], "key", 0.015)
	panel = box.add_part("right", Vector2(0, -0.5), Vector2(2, 2), tex["panel"], "panel", 0.03)

	inner = PixelBox.new()
	box.add_child(inner)
	inner.scale = Vector3.ONE * 0.4
	inner.position = Vector3(0, -3.0 + 1.2 + 0.06, 0)
	inner.build(_faces("inner"), 6.0)
	inner.set_meta("id", "inner")
	inner.blocker.set_meta("id", "inner")

	_build_hud()
	get_tree().root.size_changed.connect(_fit_screen)
	_fit_screen()
	_say("Drag to turn the box. Tap to touch.", 3.5)

	if "--autotest" in OS.get_cmdline_user_args():
		_autotest()


## Fill any screen with whole-number pixel scaling: pick the biggest integer scale that fits
## 270x480, then grow the game view to cover the rest of the screen (no black bars).
func _fit_screen() -> void:
	var win := Vector2(get_window().size)
	if win.x <= 0 or win.y <= 0:
		return
	var k := maxf(1.0, floorf(minf(win.x / BASE.x, win.y / BASE.y)))
	var view := Vector2i(int(win.x / k), int(win.y / k))
	get_tree().root.content_scale_size = view
	if not (busy and lid_open and not nested):  # never mid-zoom
		cam_width = view.x / PX_PER_UNIT
		camera.size = cam_width
	if hud_bar:
		_layout_hud(Vector2(view))


func _faces(prefix: String) -> Dictionary:
	var d := {}
	for f in ["front", "back", "left", "right", "top", "bottom"]:
		d[f] = tex["%s_%s" % [prefix, f]]
	return d


# ---------------- input ----------------

func _hud_top() -> float:
	return hud_bar.position.y


func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		if event.pressed:
			touch_down = not busy
			touch_start = event.position
			drag_axis = Vector3.ZERO
			drag_angle = 0.0
			start_basis = pivot.transform.basis
		elif touch_down:
			touch_down = false
			if drag_axis != Vector3.ZERO:
				_finish_drag()
			elif event.position.distance_to(touch_start) < 10.0:
				_tap(event.position)
	elif event is InputEventScreenDrag and touch_down:
		var d: Vector2 = event.position - touch_start
		if drag_axis == Vector3.ZERO and d.length() > 8.0 and touch_start.y < _hud_top():
			drag_axis = Vector3.UP if absf(d.x) > absf(d.y) else Vector3.RIGHT
		if drag_axis != Vector3.ZERO:
			var px := d.x if drag_axis == Vector3.UP else d.y
			drag_angle = clampf(px / DRAG_PX_PER_TURN * SNAP, -SNAP, SNAP)
			pivot.transform.basis = Basis(drag_axis, drag_angle) * start_basis


func _finish_drag() -> void:
	var target := roundf(drag_angle / SNAP) * SNAP
	if target == 0.0 and absf(drag_angle) > PI / 6.0:
		target = signf(drag_angle) * SNAP   # 30 degrees is enough to commit to the turn
	await _turn(drag_axis, drag_angle, target, start_basis)


## Animate a turn about a world axis, then clean the basis so it stays exactly axis-aligned.
func _turn(axis: Vector3, from: float, to: float, base: Basis, dur := 0.22) -> void:
	busy = true
	var t := create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	t.tween_method(func(a: float): pivot.transform.basis = Basis(axis, a) * base, from, to, dur)
	await t.finished
	pivot.transform.basis = _snap_basis(pivot.transform.basis)
	busy = false


func _snap_basis(b: Basis) -> Basis:
	var s := pivot.scale
	var o := b.orthonormalized()
	for i in 3:
		var v := o[i]
		o[i] = Vector3(roundf(v.x), roundf(v.y), roundf(v.z))
	return o.scaled(s)


func _tap(pos: Vector2) -> void:
	if busy:
		return
	if pos.y >= _hud_top():
		_tap_hud(pos)
		return
	var from := camera.project_ray_origin(pos)
	var to := from + camera.project_ray_normal(pos) * 100.0
	var hit := get_world_3d().direct_space_state.intersect_ray(PhysicsRayQueryParameters3D.create(from, to))
	if hit.is_empty():
		return
	var id: String = hit.collider.get_meta("id", "")
	if id != "":
		_on_part(id, hit.collider.get_parent())


# ---------------- puzzle logic ----------------

func _on_part(id: String, node: Node) -> void:
	if id.begins_with("dial"):
		_turn_dial(int(id.substr(4)))
	elif id == "panel":
		if not panel_open:
			_shake(panel)
			_say("It won't budge.")
	elif id == "key":
		_flash(key_part)
		key_part.visible = false
		PixelBox.set_tappable(key_part, false)
		has_key = true
		_update_hud()
		_say("A small brass key.")
	elif id == "lock":
		if lid_open:
			return
		if key_selected:
			_unlock()
		elif has_key:
			_flash(lock_part)
			_say("Select the key below first.")
		else:
			_shake(lock_part)
			_say("A keyhole.")
	elif id == "inner":
		if lid_open and not nested:
			_enter_inner()


func _turn_dial(i: int) -> void:
	if panel_open:
		return
	busy = true
	var d := dials[i]
	var t := create_tween()
	t.tween_property(d, "rotation:z", -PI / 2, 0.1)
	await t.finished
	dial_vals[i] = (dial_vals[i] + 1) % SYMS.size()
	d.rotation.z = 0.0
	d.material_override.set_shader_parameter("tex", tex["dial_" + SYMS[dial_vals[i]]])
	busy = false
	if dial_vals == CODE:
		await get_tree().create_timer(0.25).timeout
		_open_panel()


func _open_panel() -> void:
	panel_open = true
	for d in dials:
		_flash(d)
	_say("Something clicked.")
	var t := create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	t.tween_property(panel, "position:y", panel.position.y + 2.0, 0.6)
	PixelBox.set_tappable(panel, false)


func _unlock() -> void:
	busy = true
	key_selected = false
	has_key = false
	_update_hud()
	lock_part.material_override.set_shader_parameter("tex", tex["lock_open"])
	_flash(lock_part)
	_say("Click.")
	await get_tree().create_timer(0.5).timeout
	var t := create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	t.tween_property(box.lid_hinge, "rotation:x", deg_to_rad(-115.0), 0.9)
	await t.finished
	PixelBox.set_tappable(box.blocker, false)
	lid_open = true
	# Tip the box so you look down into it.
	var base := _snap_basis(pivot.transform.basis)
	var t2 := create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	t2.tween_method(func(q: Quaternion): pivot.transform.basis = Basis(q), base.get_rotation_quaternion(),
			Basis(Vector3.RIGHT, PI / 2).get_rotation_quaternion(), 0.8)
	await t2.finished
	pivot.transform.basis = _snap_basis(pivot.transform.basis)
	busy = false
	_say("There's another box inside.")


## Zoom into the inner box, then make it the box in your hands. The swap is invisible:
## a camera zoomed 0.4x on a 0.4-scale box looks identical to a normal camera on a full-size box.
func _enter_inner() -> void:
	busy = true
	nested = true
	var gp: Vector3 = inner.global_position
	var t := create_tween().set_parallel().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	t.tween_property(camera, "size", cam_width * 0.4, 1.0)
	t.tween_property(camera, "position", Vector3(gp.x, gp.y, camera.position.z), 1.0)
	await t.finished
	var gb: Basis = inner.global_transform.basis.orthonormalized()
	box.remove_child(inner)
	add_child(inner)
	inner.transform = Transform3D(gb, Vector3.ZERO)
	camera.size = cam_width
	camera.position = Vector3(0, 0, 20)
	box.queue_free()
	pivot = inner
	PixelBox.set_tappable(inner.blocker, false)
	busy = false
	_say("Box two. To be continued...", 4.0)


# ---------------- juice ----------------

func _flash(node: MeshInstance3D) -> void:
	var m: ShaderMaterial = node.material_override
	var t := create_tween()
	t.tween_method(func(v: float): m.set_shader_parameter("highlight", v), 0.3, 0.0, 0.3)


func _shake(node: Node3D) -> void:
	var x := node.position.x
	var t := create_tween()
	for o in [0.12, -0.12, 0.08, -0.05, 0.0]:
		t.tween_property(node, "position:x", x + o, 0.04)


# ---------------- HUD ----------------

func _build_hud() -> void:
	hud = CanvasLayer.new()
	add_child(hud)
	var vs := get_viewport().get_visible_rect().size
	hud_bar = ColorRect.new()
	hud_bar.color = Color(0.1, 0.07, 0.06)
	hud_bar.position = Vector2(0, vs.y - HUD_H)
	hud_bar.size = Vector2(vs.x, HUD_H)
	hud_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(hud_bar)
	slot_frame = ColorRect.new()
	slot_frame.size = Vector2(36, 36)
	slot_frame.position = Vector2(vs.x / 2 - 18, vs.y - HUD_H + 6)
	slot_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(slot_frame)
	var inside := ColorRect.new()
	inside.color = Color(0.05, 0.03, 0.03)
	inside.position = Vector2(2, 2)
	inside.size = Vector2(32, 32)
	inside.mouse_filter = Control.MOUSE_FILTER_IGNORE
	slot_frame.add_child(inside)
	slot_icon = TextureRect.new()
	slot_icon.texture = tex["key"]
	slot_icon.position = Vector2(2, 2)
	slot_icon.size = Vector2(32, 32)
	slot_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	slot_frame.add_child(slot_icon)
	hint = Label.new()
	hint.position = Vector2(0, 14)
	hint.size = Vector2(vs.x, 20)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.add_theme_font_size_override("font_size", 10)
	hint.add_theme_color_override("font_color", Color(0.91, 0.87, 0.77))
	hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(hint)
	_update_hud()


func _layout_hud(vs: Vector2) -> void:
	hud_bar.position = Vector2(0, vs.y - HUD_H)
	hud_bar.size = Vector2(vs.x, HUD_H)
	slot_frame.position = Vector2(vs.x / 2 - 18, vs.y - HUD_H + 6)
	hint.size = Vector2(vs.x, 20)


func _update_hud() -> void:
	slot_icon.visible = has_key
	slot_frame.color = Color(0.98, 0.85, 0.45) if key_selected else Color(0.35, 0.24, 0.14)


func _tap_hud(pos: Vector2) -> void:
	var r := Rect2(slot_frame.position, slot_frame.size).grow(6)
	if has_key and r.has_point(pos):
		key_selected = not key_selected
		_update_hud()
		_say("Key selected. Use it on something." if key_selected else "")


func _say(text: String, secs := 2.5) -> void:
	hint.text = text
	hint.modulate.a = 1.0
	if hint_tween:
		hint_tween.kill()
	hint_tween = create_tween()
	hint_tween.tween_interval(secs)
	hint_tween.tween_property(hint, "modulate:a", 0.0, 0.6)


# ---------------- automated playthrough for verification ----------------
# Run: godot --path . -- --autotest   (saves screenshots to user://shots)

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("user://shots")
	get_viewport().get_texture().get_image().save_png("user://shots/%s.png" % name)
	print("shot ", name)


## Test input arrives in window pixels, like a real finger, and Godot scales it to the 270x480 view.
func _w(p: Vector2) -> Vector2:
	return get_viewport().get_final_transform() * p


func _swipe(d: Vector2) -> void:
	var c := get_viewport().get_visible_rect().size / 2 - Vector2(0, 40)
	var ev := InputEventScreenTouch.new(); ev.position = _w(c); ev.pressed = true
	Input.parse_input_event(ev)
	for i in range(1, 7):
		var dr := InputEventScreenDrag.new(); dr.position = _w(c + d * i / 6.0)
		Input.parse_input_event(dr)
		await get_tree().process_frame
	var up := InputEventScreenTouch.new(); up.position = _w(c + d); up.pressed = false
	Input.parse_input_event(up)
	await get_tree().create_timer(0.4).timeout


func _press(id: String) -> void:
	_on_part(id, null)
	await get_tree().create_timer(0.3).timeout


func _autotest() -> void:
	await get_tree().create_timer(0.5).timeout
	await _shot("01_front")
	# mid-drag shot to show the hybrid look
	var c := get_viewport().get_visible_rect().size / 2
	var ev := InputEventScreenTouch.new(); ev.position = _w(c); ev.pressed = true
	Input.parse_input_event(ev)
	var dr := InputEventScreenDrag.new(); dr.position = _w(c + Vector2(45, 0))
	Input.parse_input_event(dr)
	await get_tree().process_frame
	await _shot("02_mid_drag")
	var up := InputEventScreenTouch.new(); up.position = _w(c + Vector2(45, 0)); up.pressed = false
	Input.parse_input_event(up)
	await get_tree().create_timer(0.4).timeout   # 45px > 30 deg, so it commits: left face in front
	await _shot("03_left_dials")
	await _swipe(Vector2(80, 0))                     # back face
	await _shot("04_back_clue")
	await _swipe(Vector2(80, 0))                     # right face
	await _press("panel")
	await _shot("05_right_locked")
	await _swipe(Vector2(80, 0))                     # front
	await _swipe(Vector2(80, 0))                     # left again
	for i in 3:
		for k in CODE[i]:
			await _press("dial%d" % i)
	await get_tree().create_timer(1.0).timeout
	await _shot("06_dials_solved")
	await _swipe(Vector2(-80, 0)); await _swipe(Vector2(-80, 0))  # left -> front -> right
	await _shot("07_panel_open_key")
	await _press("key")
	await _swipe(Vector2(80, 0))                     # right -> front
	key_selected = true; _update_hud()
	await _shot("08_front_key_selected")
	_on_part("lock", null)
	await get_tree().create_timer(1.0).timeout
	await _shot("09_lid_opening")
	await get_tree().create_timer(1.5).timeout
	await _shot("10_top_view_inner")
	_on_part("inner", null)
	await get_tree().create_timer(0.5).timeout
	await _shot("11_zooming")
	await get_tree().create_timer(1.0).timeout
	await _shot("12_inner_box")
	await _swipe(Vector2(0, -80))                    # pitch: bring inner box front around
	await _shot("13_inner_turned")
	print("AUTOTEST DONE")
	get_tree().quit()

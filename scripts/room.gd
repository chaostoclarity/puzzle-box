## Base for every escape room: four walls you turn between, furniture, wall sprites,
## hero boxes you can lift, and the ordered list of puzzle steps that drives hints,
## bargains and the automated playthrough.
## Wall-local coordinates: x along the wall (-7.5..7.5), y up from the floor (0..22),
## depth = distance out from the wall surface.
extends Node3D

const PixelBox = preload("res://scripts/pixel_box.gd")
const HALF := 7.5
const WALL_H := 22.0
const WALLS := ["n", "e", "s", "w"]

var game                     ## the Game node, set before build()
var title := ""
var pivot: Node3D
var groups := {}             ## wall key -> Node3D
var ids := {}                ## tappable id -> node
var boxes := {}              ## hero box name -> {"box", "home_parent", "home_xform", "view"}
var steps: Array = []        ## [{id, done: Callable, hints: [a, b], solve: Callable, said: String}]
var walkthrough: Array = []  ## real taps for the automated playthrough
var tex_cache := {}


func tex(name: String) -> Texture2D:
	if not tex_cache.has(name):
		var path := "res://assets/rooms/%s.png" % name
		if not ResourceLoader.exists(path):
			path = "res://assets/%s.png" % name
		tex_cache[name] = load(path)
	return tex_cache[name]


# ---------------- building ----------------

func build_walls(prefix: String) -> void:
	pivot = Node3D.new()
	add_child(pivot)
	var turns := [0.0, -PI / 2, PI, PI / 2]
	for i in 4:
		var g := Node3D.new()
		g.rotation.y = turns[i]
		pivot.add_child(g)
		groups[WALLS[i]] = g
		var w := PixelBox.quad(Vector2(HALF * 2, WALL_H), tex(prefix + WALLS[i]))
		w.position = Vector3(0, WALL_H / 2, -HALF)
		g.add_child(w)


## Furniture: a box standing against a wall. pos = (x along wall, y of its base).
func add_furniture(wall: String, id: String, pos: Vector2, size: Vector3, textures: Dictionary, zoom := {}) -> PixelBox:
	var b := PixelBox.new()
	groups[wall].add_child(b)
	b.build(textures, size)
	b.position = Vector3(pos.x, pos.y + size.y / 2, -HALF + size.z / 2 + 0.02)
	b.blocker.set_meta("id", id)
	b.set_meta("id", id)
	b.set_meta("zoom", zoom)
	return b


## A flat sprite: on a wall, or standing on furniture at some depth. center is wall-local (x, y).
func add_sprite(wall: String, id: String, center: Vector2, size: Vector2, texname: String, depth := 0.03, tappable := true) -> MeshInstance3D:
	var q := PixelBox.quad(size, tex(texname))
	q.position = Vector3(center.x, center.y, -HALF + depth)
	groups[wall].add_child(q)
	if tappable:
		PixelBox.add_body(q, size, id)
	else:
		q.set_meta("id", id)
	return q


## A hero box: sits somewhere in the room and can be lifted into your hands.
func register_box(name: String, b: PixelBox, view := "front") -> void:
	b.set_meta("liftable", name)
	boxes[name] = {"box": b, "home_parent": b.get_parent(), "home_xform": b.transform, "view": view}


## A full-size box that only exists in your hands (you reach it by diving into a nested box).
func add_stage_box(name: String, b: PixelBox, view := "front") -> void:
	b.visible = false
	game.stage.add_child(b)
	boxes[name] = {"box": b, "home_parent": game.stage, "home_xform": Transform3D(), "view": view, "stage_only": true}


func index_ids() -> void:
	ids.clear()
	for body in find_children("*", "StaticBody3D", true, false):
		if body.has_meta("id"):
			ids[body.get_meta("id")] = body.get_parent()
	for b in boxes.values():
		for body in (b["box"] as Node).find_children("*", "StaticBody3D", true, false):
			if body.has_meta("id"):
				ids[body.get_meta("id")] = body.get_parent()


func wall_of(node: Node) -> String:
	var n := node
	while n:
		for k in groups:
			if groups[k] == n:
				return k
		n = n.get_parent()
	return ""


## Is this wall turned toward the camera right now?
func wall_facing(key: String) -> bool:
	return (groups[key] as Node3D).global_transform.basis.z.z > 0.7


func set_wall_dim(key: String, v: float) -> void:
	for mi in groups[key].find_children("*", "MeshInstance3D", true, false):
		var m = mi.material_override
		if m is ShaderMaterial:
			m.set_shader_parameter("dim", v)


## Show or hide everything that only exists through the Lens.
func set_lens(on: bool) -> void:
	for n in get_tree().get_nodes_in_group("lens_only"):
		var gone: bool = n.get_meta("gone", false)
		n.visible = on and not gone
		PixelBox.set_tappable(n, on and not gone)


func current_step() -> Dictionary:
	for s in steps:
		if not (s["done"] as Callable).call():
			return s
	return {}


# ---------------- to override ----------------

func build() -> void:
	pass

## Snap every visual to the saved state (used on load and after a bargain).
func apply_state() -> void:
	pass

## Tap on something with no item selected. Return true if handled.
func on_tap(_id: String, _node: Node) -> bool:
	return false

## Use an inventory item on something. Return true if it worked.
func on_use(_item: String, _id: String, _node: Node) -> bool:
	return false

## Called when a box is lifted or dropped, so rooms can react.
func on_box_mode(_name: String, _entered: bool) -> void:
	pass

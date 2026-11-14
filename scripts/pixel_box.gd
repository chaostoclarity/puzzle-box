## A box made of six pixel-art faces: hero puzzle boxes and room furniture alike.
## Any size (Vector3, in world units). 16 texels per world unit.
## Parts (dials, locks, keys, sprites) attach to a face and are tappable by id.
## Faces can be hinged on any edge to make lids, doors and covers.
extends Node3D

const SHADER := preload("res://shaders/pixel_surface.gdshader")

const FACE_ROT := {
	"front": Vector3(0, 0, 0), "back": Vector3(0, 180, 0),
	"right": Vector3(0, 90, 0), "left": Vector3(0, -90, 0),
	"top": Vector3(-90, 0, 0), "bottom": Vector3(90, 0, 0),
}
const FACE_DIR := {
	"front": Vector3(0, 0, 1), "back": Vector3(0, 0, -1),
	"right": Vector3(1, 0, 0), "left": Vector3(-1, 0, 0),
	"top": Vector3(0, 1, 0), "bottom": Vector3(0, -1, 0),
}
## Basis that turns the box so a face points at the camera (+Z).
const FACE_VIEW := {
	"front": Vector3(0, 0, 0), "back": Vector3(0, 180, 0),
	"left": Vector3(0, 90, 0), "right": Vector3(0, -90, 0),
	"top": Vector3(90, 0, 0), "bottom": Vector3(-90, 0, 0),
}

var dims := Vector3(6, 6, 6)
var faces := {}
var hinges := {}
var blocker: StaticBody3D


static func make_material(tex: Texture2D) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = SHADER
	m.set_shader_parameter("tex", tex)
	return m


static func quad(dim: Vector2, tex: Texture2D) -> MeshInstance3D:
	var q := QuadMesh.new()
	q.size = dim
	var mi := MeshInstance3D.new()
	mi.mesh = q
	mi.material_override = make_material(tex)
	return mi


## A tappable body the size of a quad, so any sprite can be touched.
static func add_body(node: Node3D, dim: Vector2, id: String, thickness := 0.1) -> StaticBody3D:
	var body := StaticBody3D.new()
	body.set_meta("id", id)
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(dim.x, dim.y, thickness)
	cs.shape = shape
	body.add_child(cs)
	node.add_child(body)
	node.set_meta("id", id)
	return body


static func set_tappable(node: Node, on: bool) -> void:
	for c in node.find_children("*", "CollisionShape3D", true, false):
		c.set_deferred("disabled", not on)


static func set_texture(node: MeshInstance3D, tex: Texture2D) -> void:
	(node.material_override as ShaderMaterial).set_shader_parameter("tex", tex)


func face_size(f: String) -> Vector2:
	match f:
		"front", "back": return Vector2(dims.x, dims.y)
		"left", "right": return Vector2(dims.z, dims.y)
	return Vector2(dims.x, dims.z)


func face_offset(f: String) -> float:
	match f:
		"front", "back": return dims.z * 0.5
		"left", "right": return dims.x * 0.5
	return dims.y * 0.5


## face_textures: {"front": Texture2D, ...}; missing faces use "default".
## liner: a texture for the inside walls, shown when a face swings open.
func build(face_textures: Dictionary, box_dims = 6.0, liner: Texture2D = null, liner_skip := ["top"], solid := true) -> void:
	dims = box_dims if box_dims is Vector3 else Vector3.ONE * float(box_dims)
	for f in FACE_ROT:
		var b := Basis.from_euler(FACE_ROT[f] * (PI / 180.0))
		var tex: Texture2D = face_textures.get(f, face_textures.get("default"))
		var q := quad(face_size(f), tex)
		q.transform = Transform3D(b, FACE_DIR[f] * face_offset(f))
		add_child(q)
		faces[f] = q
		if liner and not f in liner_skip:
			var l := quad(face_size(f) * 0.98, liner)
			l.transform = Transform3D(b * Basis(Vector3.UP, PI), FACE_DIR[f] * (face_offset(f) - 0.05))
			add_child(l)
	if solid:
		blocker = StaticBody3D.new()
		var cs := CollisionShape3D.new()
		var shape := BoxShape3D.new()
		shape.size = dims * 0.98
		cs.shape = shape
		blocker.add_child(cs)
		add_child(blocker)


## Hinge a face on one of its edges (edge in face-local terms: top, bottom, left, right).
## Afterwards set_hinge(face, degrees) swings it open outward.
func hinge_face(f: String, edge: String) -> void:
	var q: MeshInstance3D = faces[f]
	var fb := q.transform.basis
	var half := face_size(f) * 0.5
	var off: Vector3 = {"top": Vector3(0, half.y, 0), "bottom": Vector3(0, -half.y, 0),
		"left": Vector3(-half.x, 0, 0), "right": Vector3(half.x, 0, 0)}[edge]
	var hinge := Node3D.new()
	hinge.transform = Transform3D(fb, q.transform.origin + fb * off)
	add_child(hinge)
	remove_child(q)
	hinge.add_child(q)
	q.transform = Transform3D(Basis.IDENTITY, -off)
	var axis := Vector3.RIGHT if edge in ["top", "bottom"] else Vector3.UP
	var sgn := -1.0 if edge in ["top", "left"] else 1.0
	hinges[f] = {"node": hinge, "base": fb, "axis": axis, "sign": sgn, "deg": 0.0}


func set_hinge(f: String, deg: float) -> void:
	var h: Dictionary = hinges[f]
	h["deg"] = deg
	(h["node"] as Node3D).transform.basis = (h["base"] as Basis) * Basis(h["axis"], deg_to_rad(deg) * h["sign"])


func get_hinge(f: String) -> float:
	return hinges[f]["deg"]


## Attach a tappable part to a face. uv = offset from the face centre in world units
## (x right, y up, as seen when that face points at the camera).
func add_part(face: String, uv: Vector2, dim: Vector2, tex: Texture2D, id: String, depth := 0.03, tappable := true) -> MeshInstance3D:
	var part := quad(dim, tex)
	part.position = Vector3(uv.x, uv.y, depth)
	faces[face].add_child(part)
	if tappable:
		add_body(part, dim, id)
	else:
		part.set_meta("id", id)
	return part

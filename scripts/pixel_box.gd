## A rotatable box made of six pixel-art faces.
## Parts (dials, panels, locks, keys) attach to a face and can be tapped.
## Every box uses the same texel density: 16 texels per world unit.
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

var size := 6.0
var faces := {}
var lid_hinge: Node3D
var blocker: StaticBody3D


static func make_material(tex: Texture2D) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = SHADER
	m.set_shader_parameter("tex", tex)
	return m


func _quad(dim: Vector2, tex: Texture2D) -> MeshInstance3D:
	var q := QuadMesh.new()
	q.size = dim
	var mi := MeshInstance3D.new()
	mi.mesh = q
	mi.material_override = make_material(tex)
	return mi


## face_textures: {"front": Texture2D, ...}. hinged_lid makes the top face a lid hinged at the back edge.
func build(face_textures: Dictionary, box_size := 6.0, hinged_lid := false, liner: Texture2D = null) -> void:
	size = box_size
	var h := size * 0.5
	for f in FACE_ROT:
		var b := Basis.from_euler(FACE_ROT[f] * (PI / 180.0))
		var q := _quad(Vector2(size, size), face_textures[f])
		if f == "top" and hinged_lid:
			lid_hinge = Node3D.new()
			lid_hinge.position = Vector3(0, h, -h)
			add_child(lid_hinge)
			q.transform = Transform3D(b, Vector3(0, 0, h))
			lid_hinge.add_child(q)
		else:
			q.transform = Transform3D(b, FACE_DIR[f] * h)
			add_child(q)
		faces[f] = q
		# Inner lining, facing inward, so an opened box has an inside.
		if liner and f != "top":
			var l := _quad(Vector2(size, size) * 0.98, liner)
			l.transform = Transform3D(b * Basis(Vector3.UP, PI), FACE_DIR[f] * (h - 0.05))
			add_child(l)

	# One solid body for the whole box so taps can't pass through to parts on the far side.
	blocker = StaticBody3D.new()
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3.ONE * size * 0.98
	cs.shape = shape
	blocker.add_child(cs)
	add_child(blocker)


## Attach a tappable part to a face. uv is the offset from the face center in world units
## (x right, y up, as seen when that face points at the camera).
func add_part(face: String, uv: Vector2, dim: Vector2, tex: Texture2D, id: String, depth := 0.03) -> MeshInstance3D:
	var part := _quad(dim, tex)
	part.position = Vector3(uv.x, uv.y, depth)
	part.set_meta("id", id)
	faces[face].add_child(part)
	var body := StaticBody3D.new()
	body.set_meta("id", id)
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(dim.x, dim.y, 0.1)
	cs.shape = shape
	body.add_child(cs)
	part.add_child(body)
	return part


static func set_tappable(node: Node, on: bool) -> void:
	for c in node.find_children("*", "CollisionShape3D", true, false):
		c.set_deferred("disabled", not on)

## Everything the player has done: one store, saved after every change.
## Autoloaded as `State`.
extends Node

signal changed

const SAVE_PATH := "user://save.json"
const VERSION := 1

## Item catalog: name and examine text. Icons live at res://assets/rooms/item_<id>.png
const ITEMS := {
	"brass_key": ["Small brass key", "Warm from the clock's works. Too small for any door."],
	"iron_key": ["Iron key", "Plain and heavy. The bow is stamped with a drawer pull."],
	"matches": ["Matches", "Lucifers, half the box gone. Wren never smoked."],
	"photo": ["Photograph", "Wren at his bookshelf. Someone has inked numbers above three of the books."],
	"ring": ["Signet ring", "Wren's ring. The bezel is cut with a W, worn smooth by a thumb."],
	"door_key": ["Study door key", "Black iron. Cold in a way metal shouldn't be."],
	"lens": ["Wren's Lens", "A ground lens of green glass in a brass collar. Things look truer through it. Or less true."],
	"chain_key": ["Padlock key", "A tiny key on a ribbon, marked with the library's seal."],
	"seal_stone": ["The first seal", "A five-sided stone, warm, faintly humming. It fits the cabinet. You know this the way you know your own name."],
}

var room := 1
var flags := {}
var inventory: Array = []
var journal: Array = []
var bargains := 0
var fragments := 0
var saving := true


func has(f: String) -> bool:
	return flags.get(f, false)


func flag_value(f: String, default = 0):
	return flags.get(f, default)


func set_flag(f: String, v = true) -> void:
	flags[f] = v
	save_game()


func has_item(id: String) -> bool:
	return id in inventory


func add_item(id: String) -> void:
	if not id in inventory:
		inventory.append(id)
	save_game()
	changed.emit()


func remove_item(id: String) -> void:
	inventory.erase(id)
	save_game()
	changed.emit()


func add_journal(key: String, title: String, text: String) -> bool:
	for e in journal:
		if e["key"] == key:
			return false
	journal.append({"key": key, "title": title, "text": text, "torn": false})
	save_game()
	changed.emit()
	return true


## The price of a bargain: the newest page you still have is torn out.
func tear_page() -> String:
	for i in range(journal.size() - 1, -1, -1):
		if not journal[i]["torn"]:
			journal[i]["torn"] = true
			save_game()
			changed.emit()
			return journal[i]["title"]
	return ""


func reset() -> void:
	room = 1
	flags = {}
	inventory = []
	journal = []
	bargains = 0
	fragments = 0
	save_game()
	changed.emit()


func save_game() -> void:
	if not saving:
		return
	var data := {"v": VERSION, "room": room, "flags": flags, "inventory": inventory,
		"journal": journal, "bargains": bargains, "fragments": fragments}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(data))


func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not f:
		return false
	var data = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY or int(data.get("v", 0)) != VERSION:
		return false
	room = int(data.get("room", 1))
	flags = data.get("flags", {})
	inventory = data.get("inventory", [])
	journal = data.get("journal", [])
	bargains = int(data.get("bargains", 0))
	fragments = int(data.get("fragments", 0))
	changed.emit()
	return true

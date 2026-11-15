## Everything the player has done: one store, saved after every change.
## Autoloaded as `State`.
extends Node

signal changed

const SAVE_PATH := "user://save.json"
const VERSION := 1

## Item catalog (name, examine text) lives in data/items.json. Icons: res://assets/rooms/item_<id>.png
var ITEMS := {}

var room := 1
var flags := {}
var inventory: Array = []
var journal: Array = []
var bargains := 0
## Mercy: the Whisper helps for free (no page, no bargain counted). A setting, kept across new games.
var mercy := false
var fragments := 0
var saving := true


func _ready() -> void:
	var f := FileAccess.open("res://data/items.json", FileAccess.READ)
	ITEMS = JSON.parse_string(f.get_as_text())


## Flags that carry from room to room. Everything else belongs to the room that set it.
const CARRY := ["burned", "slots_given", "hints_burned"]


func clear_room_flags() -> void:
	for k in flags.keys():
		if not (k in CARRY or (k.begins_with("seal") and k.ends_with("_placed"))):
			flags.erase(k)
	save_game()


func has(f: String) -> bool:
	var v = flags.get(f, false)
	if v is String:
		return v != ""
	if v == null:
		return false
	return bool(v)


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


## Tear out one page by its key (the stove asks for the blank page first).
func tear_key(key: String) -> String:
	for e in journal:
		if e["key"] == key and not e["torn"]:
			e["torn"] = true
			save_game()
			changed.emit()
			return e["title"]
	return tear_page()


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
		"journal": journal, "bargains": bargains, "fragments": fragments, "mercy": mercy}
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
	mercy = bool(data.get("mercy", false))
	changed.emit()
	return true

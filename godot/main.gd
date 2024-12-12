class_name Main extends Control

static var _instance: Main

var _basepath: String


func _init() -> void:
	if is_instance_valid(_instance):
		printerr("singleton violation")
		return
	_instance = self


func set_basepath(to: String) -> void:
	_basepath = to


static func get_base_path() -> String:
	if not is_instance_valid(_instance):
		return "./"
	return _instance._basepath

class_name FilenamePicker extends HBoxContainer

@export var file_mode: FileDialog.FileMode
@export var placeholder: String

@onready var file_dialog: FileDialog = $FileDialog
@onready var text_edit: LineEdit = $TextEdit


func _ready() -> void:
	text_edit.placeholder_text = placeholder
	$Button.pressed.connect(func() -> void:
		file_dialog.file_mode = file_mode
		file_dialog.root_subfolder = Main.get_base_path()
		file_dialog.popup_centered()
		match file_mode:
			FileDialog.FileMode.FILE_MODE_OPEN_FILE, FileDialog.FileMode.FILE_MODE_SAVE_FILE:
				file_dialog.file_selected.connect(func(s: String) -> void:
					text_edit.text = s
				, CONNECT_ONE_SHOT)
	)


func fgetp() -> String:
	return text_edit.text

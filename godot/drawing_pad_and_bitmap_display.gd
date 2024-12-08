extends MarginContainer

const DrawingPad := preload("res://drawing_pad.gd")

@onready var bitmap_display: TextureRect = %BitmapDisplay
@onready var drawing_pad: DrawingPad = %DrawingPad
@onready var filename_edit: LineEdit = %FilenameEdit

@onready var _placeholder_texture := bitmap_display.texture


func _ready() -> void:
	%ClearButton.pressed.connect(func() -> void:
		drawing_pad.clear()
		bitmap_display.texture = _placeholder_texture
	)
	%ConvertButton.pressed.connect(func() -> void:
		var drawing := drawing_pad.to_object()
		var image := drawing.get_image()
		image.resize(28, 28, Image.INTERPOLATE_LANCZOS)
		bitmap_display.texture = ImageTexture.create_from_image(image)
		var err := Drawing.image_to_npy(image, filename_edit.text)
		if err != OK:
			filename_edit.placeholder_text = error_string(err)
			filename_edit.modulate = Color.RED
			filename_edit.text = ""
			filename_edit.mouse_entered.connect(func() -> void:
				filename_edit.placeholder_text = "filename"
				filename_edit.modulate = Color.WHITE
			, CONNECT_ONE_SHOT)
	)

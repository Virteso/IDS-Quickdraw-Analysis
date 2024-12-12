extends PanelContainer

const DrawingPad := preload("res://components/drawing_pad.gd")

@onready var bitmap_display: TextureRect = %BitmapDisplay
@onready var drawing_pad: DrawingPad = %DrawingPad
@onready var filename_edit: FilenamePicker = %FilenameEdit

@onready var _placeholder_texture := bitmap_display.texture


func _ready() -> void:
	%ClearButton.pressed.connect(func() -> void:
		drawing_pad.clear()
		bitmap_display.texture = _placeholder_texture
	)
	%SaveAsBitmap.pressed.connect(func() -> void:
		var image := display_image()
		var err := Drawing.image_to_npy(image, filename_edit.fgetp())
		if err != OK:
			filename_edit.modulate = Color.RED
			filename_edit.mouse_entered.connect(func() -> void:
				filename_edit.modulate = Color.WHITE
			, CONNECT_ONE_SHOT)
	)
	drawing_pad.stroke_finished.connect(display_image)


func display_image() -> Image:
	var drawing := drawing_pad.to_object()
	var image := drawing.get_image()
	image.resize(28, 28, Image.INTERPOLATE_LANCZOS)
	bitmap_display.texture = ImageTexture.create_from_image(image)
	return image

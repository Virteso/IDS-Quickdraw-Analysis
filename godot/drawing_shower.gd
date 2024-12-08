extends Node2D

@export var sprite: Sprite2D
@onready var label: Label = $Sprite2D/Label
@onready var back_button: Button = $BackButton
@onready var forwar_button: Button = $ForwarButton

var i := 0

func _ready() -> void:
	var reader := NDSJONReader.open("full_simplified_animal migration.ndjson", 56991)
	forwar_button.pressed.connect(func():
		i = (i + 1) % reader.drawings.size()
		var drawing: Drawing = reader.drawings[i]
		display(drawing)
	)
	back_button.pressed.connect(func():
		i = (i - 1) % reader.drawings.size()
		var drawing: Drawing = reader.drawings[i]
		display(drawing)
	)


func display(drawing: Drawing) -> void:
	sprite.texture = ImageTexture.create_from_image(drawing.get_image())
	label.text = "word: %s
countrycode: %s
timestamp: %s
recognised: %s
" % [drawing.word, drawing.countrycode, drawing.timestamp, drawing.recognised]

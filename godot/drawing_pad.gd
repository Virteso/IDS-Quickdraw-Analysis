extends ColorRect

signal stroke_finished

var _mouse_on := false

var _strokes: Array[PackedVector2Array] = []
var _current_stroke: PackedVector2Array


func _ready() -> void:
	mouse_entered.connect(func() -> void: _mouse_on = true)
	mouse_exited.connect(func() -> void: _mouse_on = false)


func _process(delta: float) -> void:
	var current_pos := get_local_mouse_position().clamp(Vector2.ZERO, size)
	if not _mouse_on:
		return
	
	if Input.is_action_pressed("mouse_click"):
		_current_stroke.append(current_pos)
	elif Input.is_action_just_released("mouse_click") and not _current_stroke.is_empty():
		_strokes.append(_current_stroke)
		_current_stroke = []
		stroke_finished.emit()
	
	queue_redraw()


func _draw() -> void:
	for stroke in _strokes:
		if not stroke.size() < 2:
			draw_polyline(stroke, Color.BLACK, 8)
	if not _current_stroke.size() < 2:
		draw_polyline(_current_stroke, Color.REBECCA_PURPLE, 8)


func to_object() -> Drawing:
	var d := Drawing.new()
	d.strokes = []
	for stroke in _strokes:
		d.strokes.append(PackedVector2Array())
		for point in stroke:
			d.strokes.back().append(point / 2)
	return d


func clear() -> void:
	_strokes.clear()
	_current_stroke.clear()

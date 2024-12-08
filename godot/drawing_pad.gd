extends ColorRect

var _last_time: int = -1

var _strokes: Array[PackedVector2Array] = []
var _current_stroke: PackedVector2Array


func _process(delta: float) -> void:
	var current_pos := get_local_mouse_position().clamp(Vector2.ZERO, size)
	
	if Input.is_action_pressed("mouse_click"):
		_current_stroke.append(current_pos)
	elif Input.is_action_just_released("mouse_click"):
		_strokes.append(_current_stroke)
		_current_stroke = []
	
	queue_redraw()


func _draw() -> void:
	for stroke in _strokes:
		if not stroke.size() < 2:
			draw_polyline(stroke, Color.BLACK, 8)
	if not _current_stroke.size() < 2:
		draw_polyline(_current_stroke, Color.REBECCA_PURPLE, 8)


func to_object() -> Drawing:
	var d := Drawing.new()
	d.strokes = _strokes
	return d


func clear() -> void:
	_strokes.clear()
	_current_stroke.clear()

class_name Drawing

var word: String
var countrycode: String
var timestamp: String
var recognised: bool
var key_id: String
var strokes: Array[PackedVector2Array]


static func from_json_object(json: String) -> Drawing:
	var d := Drawing.new()
	var object: Dictionary = JSON.parse_string(json)
	if object == null:
		printerr("couldnt parse json")
		return null
	d.word = object.get("word")
	d.countrycode = object.get("countrycode")
	d.timestamp = object.get("timestamp")
	d.recognised = object.get("recognized")
	d.key_id = object.get("key_id")
	d.strokes = []
	var obds := object.get("drawing") as Array
	for stroke: Array in obds:
		var s: PackedVector2Array = []
		for i in stroke[0].size():
			var x: int = stroke[0][i]
			var y: int = stroke[1][i]
			s.append(Vector2(x, y))
		d.strokes.append(s)

	return d


static func image_to_npy(image: Image, output_filename: String) -> Error:
	if output_filename.is_empty():
		printerr("output filename is empty")
		return ERR_FILE_BAD_PATH
	if FileAccess.file_exists(output_filename):
		printerr("file " + output_filename + " already exists")
		return ERR_ALREADY_EXISTS
	var file := FileAccess.open(output_filename, FileAccess.WRITE)
	if file == null:
		printerr("error opening file")
		return FileAccess.get_open_error()
	# \x93NUMPY magic header
	file.store_8(0x93)
	file.store_buffer("NUMPY".to_ascii_buffer())
	# format version 1.0
	file.store_8(1)
	file.store_8(0)
	# header_len, hopefully not longer than this
	file.store_16(99)
	file.store_buffer(
		("{'descr': '|u1', 'fortran_order': False, 'shape': (%d, %d), }"
				% [1, image.get_size().x * image.get_size().y]).to_ascii_buffer()
	)
	# pad with spaces
	while file.get_length() != 128:
		file.store_8(0x20)
	# store the actual information
	for y in image.get_size().y:
		for x in image.get_size().x:
			# 0 is blank 1 is drawn
			file.store_8(255 - image.get_pixel(x, y).r8)
	file.close()
	return OK


func get_image() -> Image:
	var img := Image.create(256, 256, false, Image.FORMAT_RGB8)
	img.fill(Color.WHITE)
	for stroke in self.strokes:
		for l in range(1, stroke.size()):
			var p1 := stroke[l - 1]
			var p2 := stroke[l]
			var dx := p2.x - p1.x
			var dy := p2.y - p1.y
			var step := absf(dx) if absf(dx) >= absf(dy) else absf(dy)
			dx /= step
			dy /= step
			var x := p1.x
			var y := p1.y
			var i = 0
			while i <= step:
				img.set_pixel(int(x) % 256, int(y) % 256, Color.BLACK)
				for rr in range(-4, 4, 1):
					img.set_pixel(int(x + rr) % 256, int(y) % 256, Color.BLACK)
					img.set_pixel(int(x) % 256, int(y + rr) % 256, Color.BLACK)
					img.set_pixel(int(x + rr) % 256, int(y + rr) % 256, Color.BLACK)
				x += dx
				y += dy
				i += 1

	return img

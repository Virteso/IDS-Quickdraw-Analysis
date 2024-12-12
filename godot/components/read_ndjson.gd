class_name NDSJONReader

var drawings: Array[Drawing] = []

static func open(filename: String, readlines: int = 0xffffffff) -> NDSJONReader:
	var reader := NDSJONReader.new()
	var file := FileAccess.open(filename, FileAccess.READ)
	var read := 0
	while file.get_position() < file.get_length() and read < readlines:
		var line: String = file.get_line()
		reader.drawings.append(Drawing.from_json_object(line))
		read += 1
	return reader

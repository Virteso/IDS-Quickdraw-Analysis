extends PanelContainer

@onready var model_file_location_edit: LineEdit = %ModelFileLocationEdit
@onready var prediction_file_location_edit: LineEdit = %PredictionFileLocationEdit
@onready var prediction_result_label: Label = %PredictionResultLabel
@onready var predict_button: Button = %PredictButton


func _ready() -> void:
	predict_button.pressed.connect(predict)


func predict() -> Error:
	if model_file_location_edit.text.is_empty():
		printerr("model file location empty")
		prediction_result_label.text = "model file location empty"
		return ERR_DOES_NOT_EXIST
	if not FileAccess.file_exists(model_file_location_edit.text):
		printerr("model file doesn't exist at " + model_file_location_edit.text)
		prediction_result_label.text = "model file doesn't exist"
		return ERR_DOES_NOT_EXIST
	if prediction_file_location_edit.text.is_empty():
		printerr("prediction file location empty")
		prediction_result_label.text = "drawing file location empty"
		return ERR_DOES_NOT_EXIST
	if not FileAccess.file_exists(prediction_file_location_edit.text):
		printerr("prediction file doesn't exist at " + prediction_file_location_edit.text)
		prediction_result_label.text = "drawing file doesn't exist"
		return ERR_DOES_NOT_EXIST
	
	var outpud := []
	prediction_result_label.text = "predicting..........."
	await get_tree().process_frame
	await get_tree().process_frame
	OS.execute("python3",
			[
				"../cnn.py", "-m",
				model_file_location_edit.text,
				prediction_file_location_edit.text
			],
			outpud,
			true
	)
	
	var rsplit: PackedStringArray = outpud[0].split("\n")
	var outdict := {}
	var next_is_results_dict := false
	for s in rsplit:
		if next_is_results_dict:
			outdict = str_to_var(s.replace("\\", "").replace("'", '"'))
			break
		if s.begins_with("RESULTS"):
			next_is_results_dict = true
	print(outdict)
	
	var kys := outdict.keys()
	kys.sort_custom(func(a: String, b: String) -> bool:
		return outdict[a] > outdict[b]
	)
	prediction_result_label.text = ""
	for i in kys.size():
		var k: String = kys[i]
		prediction_result_label.text += str(i + 1) + ": " + k.capitalize()
		prediction_result_label.text += " (" + str(outdict[k]) + ")\n"
		if outdict[k] < 0 or i >= 2:
			break
	
	return OK

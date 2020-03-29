ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_image(filename):
	# Check if extension exists
	if not "." in filename:
		return False
	
	# If valid extension
	ext = filename.rsplit(".", 1)[1]
	if ext.lower() in ALLOWED_EXTENSIONS:
		return True
	else:
		return False
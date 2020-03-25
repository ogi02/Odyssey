ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_image(filename):
	if not "." in filename:
		return False
	ext = filename.rsplit(".", 1)[1]
	if ext.lower() in ALLOWED_EXTENSIONS:
		return True
	else:
		return False

def get_extension(filename):
	return filename.rsplit('.', 1)[1].lower()


def timestamp() -> str:
	from datetime import datetime

	return datetime.now().strftime("_%Y%m%d_%H%M%S")

def uuid4() -> str:
	import uuid

	return str(uuid.uuid4())

def email() -> str:
	return "user_email@example.com"

def datetime() -> str:
	from datetime import datetime

	return datetime.now().isoformat()

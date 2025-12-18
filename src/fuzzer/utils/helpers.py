

def timestamp() -> str:
	from datetime import datetime

	return datetime.now().strftime("_%Y%m%d_%H%M%S")
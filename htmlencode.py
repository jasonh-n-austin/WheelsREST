html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
}

def html_escape(text):
	"""Produce entities within text."""
	if text != None:
		return "".join(html_escape_table.get(c,c) for c in text)
	else: 
		return None

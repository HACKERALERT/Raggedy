class ProviderNotFoundException(Exception):
	"""
	The 'to' parameter in chat(to: str, ...) is not found/supported.
	"""

class UnsupportedDocumentException(Exception):
	"""
	The provided filepath's file format/extension is unsupported.
	"""

class EmptyOllamaResponseException(Exception):
	"""
	If ollama's response message content is None or empty.
	"""

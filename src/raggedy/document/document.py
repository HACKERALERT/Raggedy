from PySide6.QtGui import QImage
from raggedy.document.doctype import DocumentType

class Document:
	"""
	A Document is an abstract type that can be attached to a chat.
	This is an internal type and subject to change; use at your own risk.
	"""
	_doctype: DocumentType
	_filename: str

	def __init__(self, doctype: DocumentType, filename: str) -> None:
		self._doctype = doctype
		self._filename = filename

	def _get_image(self) -> QImage: # Overridden by VisualDocument
		raise NotImplementedError

	def _get_text(self) -> str: # Overridden by TextualDocument
		raise NotImplementedError

	def _get_audio(self): # Actually not implemented for now
		raise NotImplementedError

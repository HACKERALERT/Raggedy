from PySide6.QtGui import QImage

from raggedy.document.doctype import DocumentType
from raggedy.document.image.types import Image

class Document:
	"""
	Abstract type.
	"""
	_doctype: DocumentType

	def __init__(self, typ: DocumentType) -> None:
		self.doctype = typ

	def doctype(self) -> DocumentType:
		return self._doctype

	def _get_image(self) -> QImage:
		raise NotImplementedError

	def _get_text(self) -> str:
		raise NotImplementedError

class TextualDocument(Document):
	pass

class VisualDocument(Document):
	pass

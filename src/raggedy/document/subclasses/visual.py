from PySide6.QtGui import QImage
from raggedy.document.document import Document
from raggedy.document.doctype import DocumentType

class VisualDocument(Document):
	"""
	A VisualDocument is a Document containing image content.
	For example, the contents of a .jpg, .png, or a rendered PDF page.
	"""
	_image: QImage

	def __init__(self, filename: str, image: QImage) -> None:
		super().__init__(DocumentType.VISUAL, filename)
		self._image = image

	def _get_image(self) -> QImage:
		return self._image

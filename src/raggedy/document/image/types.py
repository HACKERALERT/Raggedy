from PySide6.QtGui import QImage
from raggedy.document.doctype import DocumentType
from raggedy.document.document import Document

class Image(Document):
	"""
	Image is one type of Document that can be attached to a chat.
	"""
	_image: QImage

	def __init__(self, filepath: str) -> None:
		pass

	def _from(self, image: QImage) -> None:
		super(DocumentType.VISUAL)
		self._image = image


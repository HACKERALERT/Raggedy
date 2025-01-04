from raggedy.document.document import Document
from raggedy.document.image.types import Image

class PDFPage:
	pass

class PDF(Document):
	slides: list[PDFPage]

	def __init__(self, filepath) -> None:
		pass

	def page(self, int) -> PDFPage:
		pass

	def page_as_image(self, int) -> Image:
		pass

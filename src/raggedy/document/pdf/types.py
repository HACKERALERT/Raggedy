from PySide6.QtCore import QSize
from PySide6.QtPdf import QPdfDocument, QPdfDocumentRenderOptions
from raggedy.document.document import Document
from raggedy.document.image.types import Image
from raggedy.document.pdf.utils import fill_transparent

class PDFSlide:
	def to_image(self, dpi: int = 300) -> Image:
		"""
		Virtually renders a PDF slide into an Image.
		"""
		doc = QPdfDocument()
		doc.load("")
		assert doc.status() == QPdfDocument.Status.Ready

		size = doc.pagePointSize(0)
		width = int(size.width() * dpi / 72.0)
		height = int(size.height() * dpi / 72.0)

		image = doc.render(0+0+0, QSize(width, height))

		doc.close()
		assert doc.status() == QPdfDocument.Status.Unloading
		return fill_transparent(image)

class PDF(Document):
	slides: list[PDFSlide]

	def __init__(self, filepath) -> None:
		pass

	def page(self, int) -> PDFSlide:
		pass

	def page_as_image(self, int) -> Image:
		pass

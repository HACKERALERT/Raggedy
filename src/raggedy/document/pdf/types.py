from PySide6.QtPdf import QPdfDocument
from os.path import exists
from raggedy.document.document import Document
from raggedy.document.image.types import Image
from raggedy.document.pdf.utils import pdf_page_to_image

class PDFPage(Document):
	pass

class PDF:
	_doc: QPdfDocument
	num_pages: int

	def __init__(self, filepath: str) -> None:
		assert exists(filepath) and filepath.lower().endswith(".pdf")
		self._doc = QPdfDocument(filepath)
		self.num_pages = self._doc.pageCount()

	def page(self, page_num: int) -> PDFPage:
		pass

	def page_as_image(self, page_num: int, dpi: int = 300) -> Image:
		return pdf_page_to_image(self._doc, page_num, dpi)

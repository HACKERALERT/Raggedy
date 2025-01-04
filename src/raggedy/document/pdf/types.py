from PySide6.QtPdf import QPdfDocument
from os.path import exists
from raggedy.document.document import Document
from raggedy.document.pdf.utils import pdf_page_to_image
from raggedy.document.subclasses.visual import VisualDocument
from raggedy.document.subclasses.textual import TextualDocument

class PDF:
	_doc: QPdfDocument
	num_pages: int

	def __init__(self, filepath: str) -> None:
		assert exists(filepath) and filepath.lower().endswith(".pdf")
		self._doc = QPdfDocument(filepath)
		self.num_pages = self._doc.pageCount()

	def page(self, page_num: int) -> TextualDocument:
		pass

	def page_as_image(self, page_num: int, dpi: int = 300) -> VisualDocument:
		return pdf_page_to_image(self._doc, page_num, dpi)

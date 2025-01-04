from PySide6.QtPdf import QPdfDocument
from os.path import basename, exists
from raggedy.document.pdf.utils import pdf_page_to_image
from raggedy.document.subclasses.visual import VisualDocument
from raggedy.document.subclasses.textual import TextualDocument

class PDFParser:
	"""
	A PDFParser is a high-level helper to create Documents from a .pdf file.
	It is the caller's responsibility to pass in a valid filepath.
	DO NOT delete the filepath while using the PDFParser.
	Call .close() when finished, at which point you may delete the .pdf freely.
	"""
	_doc: QPdfDocument
	_filepath: str
	num_pages: int

	def __init__(self, filepath: str) -> None:
		assert exists(filepath) and filepath.lower().endswith(".pdf")
		self._doc = QPdfDocument(filepath)
		self._filepath = filepath
		self.num_pages = self._doc.pageCount()

	def page(self, page_num: int) -> TextualDocument:
		"""
		Extract all text from a PDF page.
		For complex PDFs with formatting, consider .page_as_image() instead.

		Args:
			page_num: the page number (0-indexed)

		Returns:
			TextualDocument: contains the text contents
		"""
		return TextualDocument(
			basename(self._filepath),
			self._doc.getAllText(page_num)
		)

	def page_as_image(self, page_num: int, dpi: int = 300) -> VisualDocument:
		"""
		Render the PDF page into an image and return as a VisualDocument.

		Args:
			page_num: the page number (0-indexed)
			dpi: the dots per inch ("resolution") to render at (default is 300)

		Returns:
			VisualDocument: contains the image contents
		"""
		return pdf_page_to_image(self._doc, page_num, dpi)

	def close(self) -> None:
		return self._doc.close()

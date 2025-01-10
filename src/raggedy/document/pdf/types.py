from PySide6.QtPdf import QPdfDocument
from raggedy.document.pdf.utils import pdf_page_to_image
from raggedy.document.subclasses.visual import VisualDocument
from raggedy.document.subclasses.textual import TextualDocument
from os.path import basename, exists

class PDFParser:
	"""
	PDFParser is a high-level helper to create Documents from a .pdf file.
	It is the caller's responsibility to pass in a valid filepath.
	DO NOT delete the filepath while using the PDFParser.
	Call .close() when finished, at which point you may delete the .pdf freely.
	"""
	_doc: QPdfDocument
	_filepath: str
	num_pages: int

	def __init__(self, filepath: str) -> None:
		assert exists(filepath) and filepath.lower().endswith(".pdf")
		self._doc = QPdfDocument()
		error = self._doc.load(filepath)
		assert error == QPdfDocument.Error.None_ and self._doc.status() == QPdfDocument.Status.Ready
		self._filepath = filepath
		self.num_pages = self._doc.pageCount()

	def page(self, page_num: int) -> TextualDocument:
		"""
		Extract all text from a PDF page into a TextualDocument.
		For PDFs with complex formatting, consider .page_as_image() instead.

		Args:
			page_num: the page number (0-indexed) from [0, self.num_pages).

		Returns:
			TextualDocument: contains the text contents of the PDF page.

		Raises:
			ValueError: if the provided page_num is out of range
		"""
		if page_num not in range(0, self.num_pages):
			raise ValueError(f"page_num={page_num} out of range [0, {self.num_pages})")

		return TextualDocument(
			basename(self._filepath),
			self._doc.getAllText(page_num).text(),
		)

	def page_as_image(self, page_num: int, dpi: int = 300) -> VisualDocument:
		"""
		Render the PDF page into an image and return as a VisualDocument.
		Suitable for complex PDF pages where structure must be preserved.

		Args:
			page_num: the page number (0-indexed) from [0, self.num_pages).
			dpi: the dots per inch ("resolution") to render at (default is 300).

		Returns:
			VisualDocument: contains the image contents of the rendered PDF page.

		Raises:
			ValueError: if the provided page_num is out of range
		"""
		if page_num not in range(0, self.num_pages):
			raise ValueError(f"page_num={page_num} out of range [0, {self.num_pages})")

		return pdf_page_to_image(self._filepath, self._doc, page_num, dpi)

	def close(self) -> None:
		return self._doc.close()

from raggedy.document.document import Document
from raggedy.document.doctype import DocumentType

class TextualDocument(Document):
	"""
	A TextualDocument is a Document with text contents.
	For example, the contents of a .txt, .csv, .json, .md, .pdf, etc.
	"""
	_text: str

	def __init__(self, filename: str, text: str) -> None:
		super().__init__(DocumentType.TEXTUAL, filename)
		self._text = text

	def _get_text(self) -> str:
		return self._text

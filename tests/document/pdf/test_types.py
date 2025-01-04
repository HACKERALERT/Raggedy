from PySide6.QtGui import QImage
from raggedy.document.subclasses.textual import TextualDocument
from raggedy.document.subclasses.visual import VisualDocument
from raggedy.document.pdf.types import PDFParser

def test_PDFParser_num_pages() -> None:
	parser = PDFParser("tests/files/test.pdf")
	assert parser.num_pages == 45
	parser.close()

def test_PDFParser_page_0() -> None:
	parser = PDFParser("tests/files/test.pdf")

	doc = parser.page(0)
	assert isinstance(doc, TextualDocument)
	text = doc._get_text()
	assert isinstance(text, str)
	assert all([
		"Internet Research Task Force (IRTF)" in text,
		"ISSN: 2070-1721" in text,
		"Google, Inc." in text,
		"ChaCha20 and Poly1305 for IETF Protocols" in text,
		"Abstract" in text,
		"Status of This Memo" in text,
		"Copyright Notice" in text,
		"Nir & Langley" in text,
		"Informational" in text,
		"[Page 1]" in text,
	])

	parser.close()

def test_PDFParser_page_44() -> None:
	parser = PDFParser("tests/files/test.pdf")

	doc = parser.page(44)
	assert isinstance(doc, TextualDocument)
	text = doc._get_text()
	assert isinstance(text, str)
	assert all([
		"Acknowledgements" in text,
		"Check Point Software Technologies, Ltd." in text,
		"[Page 45]" in text,
	])

	parser.close()

def test_PDFParse_page_out_of_range() -> None:
	parser = PDFParser("tests/files/test.pdf")

	try:
		parser.page(45)
	except ValueError:
		pass # expected since the valid range is [0, 45)
	else:
		raise Exception("ValueError not raised")

	parser.close()

def test_PDFParser_page_as_image() -> None:
	parser = PDFParser("tests/files/test.pdf")

	doc = parser.page_as_image(0)
	assert isinstance(doc, VisualDocument)
	image = doc._get_image()
	assert isinstance(image, QImage)
	assert image.width() and image.height()

	parser.close()

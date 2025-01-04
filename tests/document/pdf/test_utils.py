from PySide6.QtGui import QImage, QColor
from PySide6.QtPdf import QPdfDocument
from raggedy.document.pdf.utils import fill_transparent, pdf_page_to_image
from raggedy.document.subclasses.visual import VisualDocument

def test_fill_transparent_on_black() -> None:
	image = QImage(100, 100, QImage.Format.Format_ARGB32)
	image.fill(QColor(0, 0, 0))
	filled = fill_transparent(image)
	assert isinstance(filled, QImage)
	assert filled.width() == image.width() and filled.height() == image.height()
	for x in range(filled.width()):
		for y in range(filled.height()):
			assert filled.pixelColor(x, y) == QColor(0, 0, 0)

def test_fill_transparent_on_white() -> None:
	image = QImage(100, 100, QImage.Format.Format_ARGB32)
	image.fill(QColor(255, 255, 255))
	filled = fill_transparent(image)
	assert isinstance(filled, QImage)
	assert filled.width() == image.width() and filled.height() == image.height()
	for x in range(filled.width()):
		for y in range(filled.height()):
			assert filled.pixelColor(x, y) == QColor(255, 255, 255)

def test_fill_transparent_on_transparent() -> None:
	image = QImage(100, 100, QImage.Format.Format_ARGB32)
	image.fill(QColor(128, 128, 128, 0))
	filled = fill_transparent(image)
	assert isinstance(filled, QImage)
	assert filled.width() == image.width() and filled.height() == image.height()
	for x in range(filled.width()):
		for y in range(filled.height()):
			assert filled.pixelColor(x, y) == QColor(255, 255, 255)

def test_pdf_page_to_image() -> None:
	filepath = "tests/files/test.pdf"
	doc = QPdfDocument()
	doc.load(filepath)
	image = pdf_page_to_image(filepath, doc, 0)
	assert doc.status() == QPdfDocument.Status.Ready
	assert isinstance(image, VisualDocument)
	assert isinstance(image._get_image(), QImage)
	assert image._filename == "test.pdf"

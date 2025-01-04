from PySide6.QtGui import QImage, QColor
from PySide6.QtPdf import QPdfDocument
from raggedy.document.image.types import Image
from raggedy.document.pdf.utils import fill_transparent, pdf_page_to_image

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
	doc = QPdfDocument()
	doc.load("tests/files/test.pdf")
	image = pdf_page_to_image(doc, 0)
	assert doc.status() == QPdfDocument.Status.Ready
	assert isinstance(image, Image)

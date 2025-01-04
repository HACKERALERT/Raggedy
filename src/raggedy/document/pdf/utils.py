from PySide6.QtCore import QSize
from PySide6.QtGui import QImage, QColor, QPainter
from PySide6.QtPdf import QPdfDocument
from raggedy.document.image.types import Image

def fill_transparent(image: QImage, color: QColor = QColor(255, 255, 255)) -> QImage:
	"""
	Fills in the transparent pixels in 'image' with the specified 'color'.

	Args:
		image: the input QImage with potentially transparent pixels to fill in.
		color: the QColor to fill any transparent pixels with (default is white).

	Returns:
		QImage: a new QImage with the transparent pixels filled in.
	"""
	width, height = image.width(), image.height()
	background = QImage(width, height, QImage.Format.Format_ARGB32)
	background.fill(color)

	painter = QPainter(background)
	painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
	painter.drawImage(0, 0, image.convertToFormat(QImage.Format.Format_ARGB32))
	assert painter.end()

	return background

def pdf_page_to_image(doc: QPdfDocument, page: int, dpi: int = 300) -> Image:
	"""
	Renders a page from a PDF into an Image.
	Automatically fills transparency with white.

	Args:
		doc: the already-loaded QPdfDocument containing the page
		page: the page number to render (0-indexed)
		dpi: the dots per inch ("resolution") to render at (default is 300)

	Returns:
		Image: the PDF page rendered as an image
	"""
	assert doc.status() == QPdfDocument.Status.Ready

	size = doc.pagePointSize(page)
	width = int(size.width() * dpi / 72.0)
	height = int(size.height() * dpi / 72.0)

	image = doc.render(page, QSize(width, height))

	doc.close()
	assert doc.status() == QPdfDocument.Status.Unloading
	return fill_transparent(image)

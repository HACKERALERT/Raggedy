from PySide6.QtGui import QImage, QColor, QPainter

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

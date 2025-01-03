from PySide6.QtGui import QImage, QColor, QPainter
from raggedy.document.pdf.utils import fill_transparent

def test_fill_transparent_on_black() -> None:
    image = QImage(100, 100, QImage.Format.Format_ARGB32)
    image.fill(QColor(0, 0, 0))
    filled = fill_transparent(image)
    assert isinstance(filled, QImage)
    for x in range(filled.width()):
        for y in range(filled.height()):
            assert filled.pixelColor(x, y) == QColor(0, 0, 0)

def test_fill_transparent_on_transparent() -> None:
    image = QImage(100, 100, QImage.Format.Format_ARGB32)
    image.fill(QColor(0, 0, 0, 0))
    filled = fill_transparent(image)
    assert isinstance(filled, QImage)
    for x in range(filled.width()):
        for y in range(filled.height()):
            assert filled.pixelColor(x, y) == QColor(255, 255, 255)

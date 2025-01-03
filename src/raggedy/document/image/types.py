from PySide6.QtGui import QImage

class Image:
    _image: QImage

    def _from(self, image: QImage):
        self._image = image

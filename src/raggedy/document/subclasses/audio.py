from raggedy.document.document import Document
from raggedy.document.doctype import DocumentType

class AudioDocument(Document):
	"""
	An AudioDocument is a Document containing audio content.
	For example, the contents of a .mp3, .m4a, .opus, etc.

	TODO: CURRENTLY UNIMPLEMENTED
	"""
	_audio: None

	def __init__(self, filename: str, audio: None) -> None:
		super().__init__(DocumentType.AUDIO, filename)
		self._audio = audio

		raise NotImplementedError

	def _get_audio(self) -> None:
		raise NotImplementedError

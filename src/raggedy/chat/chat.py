from __future__ import annotations
from raggedy.document.document import Document
from raggedy.chat.attach import _attach
from typing import Iterator

class Chat:
	"""
	An abstract Chat class in which you may attach files to chat with.
	Message history is stored interally by the Chat instance.
	You can call .message() multiple times to have multi-turn conversations.

	Do not initialize directly; use chat(to: str, model: str) instead.
	"""

	def _attach_document(self, doc: Document) -> None:
		raise NotImplementedError # must be implemented in a subclass

	def message(self, message: str) -> str:
		raise NotImplementedError # must be implemented in a subclass

	def message_stream(self, message: str) -> Iterator[str]:
		raise NotImplementedError # must be implemented in a subclass

	# Default universal implementation
	def attach(self, filepath: str, page: int = -1, as_image: bool = False) -> Chat:
		"""
		Attach a document to the chat. Don't delete 'filepath' while using this Chat.

		Args:
			filepath: the filepath to the file to attach. Caller must ensure validity.
			page (optional): the 0-indexed page number (default is -1 for all pages).
			as_image (optional): render as an image to preserve complex structure.

		Returns:
			Chat: the same chat but with the file attached to the next user message.
		"""
		self._attach_document(_attach(filepath, page, as_image))
		return self

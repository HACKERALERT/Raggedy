from __future__ import annotations
from raggedy.document.document import Document
from raggedy.chat.attach import _attach
from typing import Iterator

class Chat:
	"""
	An abstract Chat class in which you may attach files to chat with.
	Message history is automatically stored interally by the Chat instance.
	You can call .message() multiple times to have multi-turn conversations.
	You can call .message_stream() to get an iterator yielding string chunks.

	Do not initialize directly; use chat(to: str, model: str) -> Chat instead.
	"""

	def _attach_document(self, doc: Document) -> None:
		raise NotImplementedError # must be implemented in a subclass

	def message(self, message: str) -> str:
		raise NotImplementedError # must be implemented in a subclass

	def message_stream(self, message: str) -> Iterator[str]:
		raise NotImplementedError # must be implemented in a subclass

	# Default universal implementation (do not override)
	def attach(self, filepath: str, page: int = -1, as_image: bool = False) -> Chat:
		"""
		Attach a file to the chat. Don't delete the file while using this Chat.

		Args:
			filepath: the filepath to the file to attach. Caller must ensure existence and validity.
			page (optional, only for PDFs): the 0-indexed page number (default is -1 for all pages).
			as_image (optional, only for PDFs): render the page as an image to preserve complex structure.

		Returns:
			Chat: the same chat but with the file attached. You may now send a message or attach another file.
		"""
		self._attach_document(_attach(filepath, page, as_image))
		return self

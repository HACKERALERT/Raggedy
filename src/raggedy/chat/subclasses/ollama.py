from ollama import chat
from raggedy.chat.chat import Chat
from raggedy.document.document import Document
from raggedy.document.doctype import DocumentType
from raggedy.exceptions import *
from typing import Iterator
from tempfile import TemporaryDirectory
from pathlib import Path
from os.path import join, exists

class OllamaChat(Chat):
	_model: str # "llama3.2", "llama3.2-vision", etc.
	_messages: list[dict[str, str]] # standard { role, content } format

	def __init__(self, model: str) -> None:
		self._model = model
		self._messages = []

	def _ensure_latest_message_is_user(self) -> None:
		if not self._messages or self._messages[-1]["role"] != "user":
			self._messages.append({ "role": "user", "content": "" })

	# @Override
	def _attach_document(self, doc: Document) -> None:
		self._ensure_latest_message_is_user()

		if doc._doctype == DocumentType.TEXTUAL:
			inline = f"\n\n```{doc._filename}\n{doc._get_text()}\n```"
			self._messages[-1]["content"] += inline

		elif doc._doctype == DocumentType.VISUAL:
			if "images" not in self._messages[-1]:
				self._messages[-1]["images"] = []
			with TemporaryDirectory(delete=True) as tmp:
				path = join(tmp, "tmp.png")
				doc._get_image().save(path)
				raw = Path(path).read_bytes()
				self._messages[-1]["images"].append(raw)
			assert not exists(path)

		elif doc._doctype == DocumentType.AUDIO:
			raise NotImplementedError

		else:
			raise UnsupportedDocumentException

	# @Override
	def message(self, message: str) -> str:
		"""
		Send a message to the chat with ollama with streaming off.

		Args:
			message: the text message to send to the model.

		Returns:
			str: the model's response.

		Raises:
			EmptyOllamaResponseException: if ollama's response is None (unlikely).
		"""
		self._ensure_latest_message_is_user()
		self._messages[-1]["content"] = message + "\n" + self._messages[-1]["content"]

		res = chat(model=self._model, messages=self._messages, stream=False)
		text = res.message.content
		if text is None:
			raise EmptyOllamaResponseException

		self._messages.append({
			"role": "assistant",
			"content": text,
		})
		return text

	# @Override
	def message_stream(self, message: str) -> Iterator[str]:
		"""
		Send a message to the chat with ollama with streaming on.

		Args:
			message: the text to send to the model.

		Returns:
			Iterator[str]: the model's response yielded as chunks come in.

		Raises:
			EmptyOllamaResponseException: if ollama's response is None (unlikely).
		"""
		self._ensure_latest_message_is_user()
		self._messages[-1]["content"] = message + "\n" + self._messages[-1]["content"]

		res = chat(model=self._model, messages=self._messages, stream=True)
		text = ""
		for chunk in res:
			text += chunk.message.content if chunk.message.content else ""
			yield chunk.message.content if chunk.message.content else ""

		if text is None:
			raise EmptyOllamaResponseException

		self._messages.append({
			"role": "assistant",
			"content": text,
		})

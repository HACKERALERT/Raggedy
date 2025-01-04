from ollama import chat
from raggedy.chat.chat import Chat
from raggedy.document.document import Document
from raggedy.document.doctype import DocumentType
from raggedy.exceptions import *
from typing import Iterator
from tempfile import TemporaryDirectory
from pathlib import Path
from os.path import join

class OllamaChat(Chat):
	_model: str # "llama3.2", etc.
	_messages: list[dict[str, str]]

	def __init__(self, model: str) -> None:
		self._model = model
		self._messages = []
		self._to_delete = []

	def _ensure_latest_message_is_user(self) -> None:
		if not self._messages or self._messages[-1]["role"] == "assistant":
			self._messages.append({ "role": "user", "content": "" })

	def _attach_document(self, doc: Document) -> None:
		self._ensure_latest_message_is_user()

		if doc._doctype == DocumentType.TEXTUAL:
			inline = f"\n```{doc._filename}\n{doc._get_text()}```"
			self._messages[-1]["content"] += inline

		elif doc._doctype == DocumentType.VISUAL:
			if "images" not in self._messages[-1]:
				self._messages[-1]["images"] = []
			with TemporaryDirectory() as tmp:
				path = join(tmp, "temp.png")
				doc._get_image().save(path)
				raw = Path(path).read_bytes()
				self._messages[-1]["images"].append(raw)

		elif doc._doctype == DocumentType.AUDIO:
			raise NotImplementedError

		else:
			raise UnsupportedDocumentException

	def message(self, message: str) -> str:
		"""
		Send a message to the chat with ollama with streaming off.

		Args:
			message: the text to send to the model.

		Returns:
			str: the model's response.

		Raises:
			EmptyOllamaResponseException: if upstream ollama's response is None.
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

	def message_stream(self, message: str) -> Iterator[str]:
		"""
		Send a message to the chat with ollama with streaming on.

		Args:
			message: the text to send to the model.

		Returns:
			Iterator[str]: the model's response yielded as chunks come in.

		Raises:
			EmptyOllamaResponseException: if the final combined response is empty.
		"""
		self._ensure_latest_message_is_user()
		self._messages[-1]["content"] = message + "\n" + self._messages[-1]["content"]

		res = chat(model=self._model, messages=self._messages, stream=True)
		text = ""
		for chunk in res:
			text += chunk.message.content if chunk.message.content else ""
			yield text

		if text is None:
			raise EmptyOllamaResponseException

		self._messages.append({
			"role": "assistant",
			"content": text,
		})

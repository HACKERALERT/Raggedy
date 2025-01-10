from ollama import chat, Options
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
	_options: Options

	def __init__(self, model: str, temperature: float, num_ctx: int) -> None:
		self._model = model
		self._messages = []
		if temperature == -1 and num_ctx == -1:
			self._options = Options()
		if temperature != -1 and num_ctx == -1:
			self._options = Options(temperature=temperature)
		if temperature == -1 and num_ctx != -1:
			self._options = Options(num_ctx=num_ctx)
		if temperature != -1 and num_ctx != -1:
			self._options = Options(temperature=temperature, num_ctx=num_ctx)

	def _new_user_message(self, content: str = "") -> None:
		self._messages.append({ "role": "user", "content": content })

	# @Override
	def _attach_document(self, doc: Document) -> None:

		if doc._doctype == DocumentType.TEXTUAL:
			stripped = doc._get_text().strip().replace("```", "")
			self._new_user_message(
				f"File attachment: {doc._filename}\n```{stripped}\n```",
			)

		elif doc._doctype == DocumentType.VISUAL:
			filename = doc._filename
			self._new_user_message(
				f"Image attachment" + f": {filename}" if filename else "",
			)
			with TemporaryDirectory(delete=True) as tmp:
				path = join(tmp, "tmp.png")
				doc._get_image().save(path)
				raw = Path(path).read_bytes()
				self._messages[-1]["images"] = [raw]
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
		self._new_user_message(message)

		res = chat(
			model=self._model,
			messages=self._messages,
			stream=False,
			options=self._options,
		)
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
		self._new_user_message(message)

		res = chat(
			model=self._model,
			messages=self._messages,
			stream=True,
			options=self._options,
		)
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

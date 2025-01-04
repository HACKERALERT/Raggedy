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

	def _ensure_latest_message_is_user(self) -> None:
		if not self._messages or self._messages[-1]["role"] != "user":
			self._messages.append({ "role": "user", "content": "" })

	# @Override
	def _attach_document(self, doc: Document) -> None:
		self._ensure_latest_message_is_user()

		if doc._doctype == DocumentType.TEXTUAL:
			stripped = doc._get_text().strip().replace("```", "")
			inline = f"\n\n```{doc._filename}\n{stripped}\n```"
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
		self._ensure_latest_message_is_user()
		self._messages[-1]["content"] = message + "\n" + self._messages[-1]["content"]

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

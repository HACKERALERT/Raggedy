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
		self._messages = [{
			"role": "system",
			"content": "You are a helpful assistant.",
		}]
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
			cleaned = doc._get_text().strip().replace("```", "\\`\\`\\`")
			self._new_user_message(f"User attached a file: {doc._filename}\n\nContents:\n```\n{cleaned}\n```")

		elif doc._doctype == DocumentType.VISUAL:
			self._new_user_message(f"User attached an image:" + f" {doc._filename}" if doc._filename else "")
			with TemporaryDirectory(delete=True) as tmp:
				png = join(tmp, "tmp.png")
				jpg = join(tmp, "tmp.jpg")
				assert doc._get_image().save(png)
				assert doc._get_image().save(jpg)
				raw_png = Path(png).read_bytes()
				raw_jpg = Path(jpg).read_bytes()

				"""
				Ollama accepts both .png and .jpg as images. Depending on the image contents, one may be a better choice:
				- If the .png has a smaller size, the image likely contains graphical contents such as text or charts.
				- If the .jpg has a smaller size, the image is likely a photographic image like a picture of a puppy.
				Picking the image format with the smaller size optimizes both quality and minimizes context usage.
				"""
				self._messages[-1]["images"] = [raw_png if len(raw_png) <= len(raw_jpg) else raw_jpg]
			assert not exists(png) and not exists(jpg)

		elif doc._doctype == DocumentType.AUDIO:
			raise NotImplementedError

		else:
			raise UnsupportedDocumentException

	# @Override
	def message(self, message: str) -> str:
		"""
		Send a message to the chat with streaming off.

		Args:
			message: the text message to send to the model.

		Returns:
			str: the model's response.

		Raises:
			EmptyOllamaResponseException: if ollama's response is None or empty (unlikely).
		"""
		self._new_user_message(message)

		res = chat(
			model=self._model,
			messages=self._messages,
			stream=False,
			options=self._options,
		)
		text = res.message.content
		if not text:
			raise EmptyOllamaResponseException

		self._messages.append({
			"role": "assistant",
			"content": text,
		})
		return text

	# @Override
	def message_stream(self, message: str) -> Iterator[str]:
		"""
		Send a message to the chat with streaming on.

		Args:
			message: the text to send to the model.

		Returns:
			Iterator[str]: the model's response yielded as chunks come in.

		Raises:
			EmptyOllamaResponseException: if ollama's response is None or empty (unlikely).
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
			content = chunk.message.content if chunk.message.content else ""
			text += content
			yield content

		if not text:
			raise EmptyOllamaResponseException

		self._messages.append({
			"role": "assistant",
			"content": text,
		})

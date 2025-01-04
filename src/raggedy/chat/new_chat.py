from raggedy.chat.chat import Chat
from raggedy.chat.subclasses.ollama import OllamaChat
from raggedy.exceptions import ProviderNotFoundException

def chat(to: str, model: str) -> Chat:
	"""
	Creates a new chat to provider 'to' and model name 'model'.

	Args:
		to: the provider, for example, "ollama" or "openai".
		model: the model name, for example, "llama3.2" or "gpt-4o-mini".

	Returns:
		Chat: a Chat object in which you can .attach() files and .message().

	Raises:
		ProviderNotFoundException: if the 'to' provider is not found or supported.
	"""
	if to == "ollama":
		return OllamaChat(model)

	raise ProviderNotFoundException

from raggedy.chat.chat import Chat
from raggedy.chat.subclasses.ollama import OllamaChat
from raggedy.exceptions import ProviderNotFoundException

def chat(to: str, model: str, temperature: float = -1, num_ctx: int = -1) -> Chat:
	"""
	Creates a new chat to provider 'to' and model name 'model'.
	It is the caller's responsibility to ensure 'model' exists for 'to'.
	If using local providers like ollama, make sure to pull the relevant 'model' in advance.

	Args:
		to: the provider, for example, "ollama" or "openai".
		model: the model name, for example, "llama3.2", "llama3.2-vision", or "gpt-4o-mini".
		temperature (optional): the model temperature to use (use 0 for most consistent and objective).
		num_ctx (optional, only for ollama): the context window size to use as an integer.

	Returns:
		Chat: a Chat object in which you can .attach() files and .message() or .message_stream().

	Raises:
		ProviderNotFoundException: if the 'to' provider is not found or supported.
	"""
	if to == "ollama":
		return OllamaChat(model, temperature, num_ctx)
	assert num_ctx == -1

	raise ProviderNotFoundException

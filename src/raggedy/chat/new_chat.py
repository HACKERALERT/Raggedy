from raggedy.chat.chat import Chat
from raggedy.chat.subclasses.ollama import OllamaChat
from raggedy.exceptions import ProviderNotFoundException

def chat(to: str, model: str, temperature: float = -1, num_ctx: int = -1) -> Chat:
	"""
	Creates a new chat to provider 'to' and model name 'model'.
	It is the caller's responsibility to ensure 'model' exists for 'to'.
	If using local providers, make sure to pull the relevant 'model' first.

	Args:
		to: the provider, for example, "ollama" or "openai".
		model: the model name, for example, "llama3.2" or "gpt-4o-mini".
		temperature (optional): the model temperature to use (0 for most objective)
		num_ctx (optional): the context window size as an integer

	Returns:
		Chat: a Chat object in which you can .attach() files and .message().

	Raises:
		ProviderNotFoundException: if the 'to' provider is not found or supported.
	"""
	if to == "ollama":
		return OllamaChat(model, temperature, num_ctx)

	raise ProviderNotFoundException

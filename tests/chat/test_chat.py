from raggedy.chat.new_chat import chat

def test_ollama_no_attachments_single() -> None:
	c = chat(to="ollama", model="llama3.2")
	res = c.message("What color is the sky? Respond in one word.")
	assert isinstance(res, str) and "blue" in res.lower()

def test_ollama_no_attachments_multiple() -> None:
	c = chat(to="ollama", model="llama3.2")
	res = c.message("My favorite number is 135672. Please remember that.")
	assert isinstance(res, str) and res

	res = c.message("Explain the anthropic principle.")
	assert isinstance(res, str) and res

	res = c.message("Can you recall my favorite number? What is it?")
	assert isinstance(res, str) and res and "135672" in res

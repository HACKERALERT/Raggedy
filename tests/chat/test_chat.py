from raggedy.chat.new_chat import chat

def test_ollama_no_attachments_single_no_stream() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0)
	res = c.message("What color is the sky? Respond in one word.")
	assert isinstance(res, str) and "blue" in res.lower()

def test_ollama_no_attachments_single_streaming() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0)
	res = c.message_stream("What color is the sky? Why is that?")
	total = ""
	for chunk in res:
		assert isinstance(chunk, str)
		total += chunk
	assert "blue" in total.lower()

def test_ollama_no_attachments_multiple_no_stream() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0)
	res = c.message("My favorite number is 135. Please remember that.")
	assert isinstance(res, str) and res

	res = c.message("Explain the anthropic principle.")
	assert isinstance(res, str) and res

	res = c.message("Can you recall my favorite number? What is it?")
	assert isinstance(res, str) and "135" in res

def test_ollama_no_attachments_multiple_streaming() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0)
	res = c.message_stream("My favorite number is 672. Please remember that.")
	total = ""
	for chunk in res:
		assert isinstance(chunk, str)
		total += chunk
	assert total

	res = c.message_stream("Explain the anthropic principle.")
	total = ""
	for chunk in res:
		assert isinstance(chunk, str)
		total += chunk
	assert total

	res = c.message_stream("Can you recall my favorite number? What is it?")
	total = ""
	for chunk in res:
		assert isinstance(chunk, str)
		total += chunk
	assert "672" in total

def test_ollama_image_attachment_no_stream() -> None:
	c = chat(to="ollama", model="llama3.2-vision", temperature=0)
	res = c.message("My favorite number is 283. Please remember that.")
	assert isinstance(res, str) and res

	c.attach("tests/files/test.jpg")
	res = c.message("Please describe this image.")
	assert isinstance(res, str) and "city" in res.lower()

	res = c.message("Can you recall my favorite number? What is it?")
	assert isinstance(res, str) and "283" in res

def test_ollama_text_attachment_no_stream() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0)
	res = c.message("My favorite number is 546. Please remember that.")
	assert isinstance(res, str) and res

	c.attach("tests/files/test.json")
	res = c.message("What is the answer to q2 of maths?")
	assert isinstance(res, str) and "4" in res

	res = c.message("Can you recall my favorite number? What is it?")
	assert isinstance(res, str) and "546" in res

def test_ollama_pdf_single_page_no_stream() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0)
	res = c.message("My favorite number is 629. Please remember that.")
	assert isinstance(res, str) and res

	c.attach("tests/files/test.pdf", page=2) # 3rd page
	res = c.message("In what specific section is Poly1305 described further?")
	assert isinstance(res, str) and "2.5" in res

	res = c.message("Can you recall my favorite number? What is it?")
	assert isinstance(res, str) and "629" in res

def test_ollama_pdf_single_page_as_image_no_stream() -> None:
	c = chat(to="ollama", model="llama3.2-vision", temperature=0)
	res = c.message("My favorite number is 829. Please remember that.")
	assert isinstance(res, str) and res

	c.attach("tests/files/test.pdf", page=33, as_image=True)
	res = c.message("What is the plaintext in this page? Output it verbatim.")
	assert isinstance(res, str) and "gimble in the w" in res.lower()

	res = c.message("Can you recall my favorite number? What is it?")
	assert isinstance(res, str) and "829" in res

def test_ollama_pdf_all_pages_no_stream() -> None:
	c = chat(to="ollama", model="llama3.2", num_ctx=16384, temperature=0)
	res = c.message("My favorite number is 206. Please remember that.")
	assert isinstance(res, str) and res

	c.attach("tests/files/test2.pdf") # attach all pages
	res = c.message("What is the audio DSP controller of the laptop?")
	assert isinstance(res, str) and "Realtek ALC5505" in res

	res = c.message("On what page did you find that? Answer in one word.")
	assert isinstance(res, str) and ("3" in res or "three" in res.lower())

	res = c.message("What is the filename of the attached PDF document?")
	assert isinstance(res, str) and "test2.pdf" in res

	res = c.message("How many total pages does the PDF have? Answer in one word.")
	assert isinstance(res, str) and ("6" in res or "six" in res.lower())

	res = c.message("Can you recall my favorite number? What is it?")
	assert isinstance(res, str) and "206" in res

def test_ollama_options_default() -> None:
	c = chat(to="ollama", model="llama3.2")
	assert c._options.temperature is None and c._options.num_ctx is None

def test_ollama_options_temperature() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0.2)
	assert c._options.temperature == 0.2 and c._options.num_ctx is None

def test_ollama_options_num_ctx() -> None:
	c = chat(to="ollama", model="llama3.2", num_ctx=40000)
	assert c._options.temperature is None and c._options.num_ctx == 40000

def test_ollama_options_temperature_num_ctx() -> None:
	c = chat(to="ollama", model="llama3.2", temperature=0.1, num_ctx=60000)
	assert c._options.temperature == 0.1 and c._options.num_ctx == 60000

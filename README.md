# Raggedy
A refreshingly simple way to chat with LLMs/VLMs programmatically.

# Installation
```
pip install raggedy
```
On Linux, you may also need to install `libegl1`.

# Usage
## Basic single message
```py
from raggedy import chat

res = chat(to="ollama", model="llama3.2").message("Hello!")

print(res) # 'Hello! How can I assist you today?'
```

## Message with files and streaming
```py
c = chat(to="ollama", model="llama3.2-vision")

c.attach("test.png") # See below for supported file extensions

for chunk in c.message_stream("Describe this image."):
    print(chunk, end="", flush=True)
```

## Multi-turn chatting (context memory)
```py
c = chat(to="ollama", model="llama3.2")

print(c.message("My name is Evan. Please remember that."))
# 'I will make sure to remember your name, Evan! ...'

print(c.message("Why is the sky blue?"))
# 'The reason the sky appears blue is due to a phenomenon...'

print(c.message("What's my name again?"))
# 'Your name is Evan! I remember it from our conversation at the start.'
```

## PDF attachments
### Attach all pages
```py
c = chat(to="ollama", model="llama3.2")

c.attach("test.pdf")

res = c.message("What are the contents of this PDF?")
```

### Attach one page by direct text extraction
```py
c = chat(to="ollama", model="llama3.2")

c.attach("test.pdf", page=0) # first page (0-indexed)

res = c.message("Describe this page from a PDF.")
```

### Attach one page by rendering to an image
If the PDF page contains complex formatting, you can render to an image to preserve it:
```py
c = chat(to="ollama", model="llama3.2-vision")

c.attach("test.pdf", page=0, as_image=True)

res = c.message("Extract the table in this image as Markdown.")
```

# Parameters
## `chat(to, model, temperature?, num_ctx?) -> Chat`
#### `to: str`
- Allowed values:
    - `ollama`: ensure Ollama is running and pull models in advance.
    - `openai`: not implemented yet; work in progress.
    - `gemini`: not implemented yet; work in progress.
#### `model: str`
- The model name to talk to. For example, "llama3.2" for `ollama` or "gpt-4o" for `openai`.
#### `temperature?: float`
- An **optional** parameter to specify temperature; 0 is objective, increase for creativity.
#### `num_ctx?: int`
- An **optional** parameter to specify the context size; for example, 32768 for a 32k window.

## `attach(str, page?, as_image?) -> Chat`
The return value is the same Chat instance (so you can chain calls).
#### `filepath: str`
- The path to the file to attach. It is your responsibility to ensure it exists and is valid.
- Currently supported file extensions are:
    - Image formats: `.jpg`, `.png`
    - Textual formats: `.txt`, `.csv`, `.json(l)`, `.xml`, `.md`
    - Other formats: `.pdf`
#### `page?: int`
- An **optional** parameter to specify page number (**for PDFs**). Default is all pages as text.
#### `as_image?: bool`
- An **optional** parameter for rendering **a PDF page** as an image to attach.

## `message(message: str) -> str`
#### `message: str`
- The message to send to the LLM/VLM. Upon calling, any attachments will be sent with this call.

## `message_stream(message: str) -> Iterator[str]`
- Same as `message()` but returns an iterator yielding streamed tokens from the LLM/VLM.

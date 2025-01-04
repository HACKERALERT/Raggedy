# Raggedy
A refreshingly simple way to chat with LLMs/VLMs programmatically.

# Installation
```
pip install raggedy
```

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

print(c.message("My name is Evan. Please remember that"))
# 'I will make sure to remember your name, Evan! ...'

print(c.message("Why is the sky blue?"))
# 'The reason the sky appears blue is due to a phenomenon...'

print(c.message("What's my name again?"))
# 'Your name is Evan! I remember it from our conversation at the start.'
```

## Attach a page from a PDF
### All pages
```py
c = chat(to="ollama", model="llama3.2")

c.attach("test.pdf")

res = c.message("What are the contents of this PDF?")
```

### One page by direct text extraction
```py
c = chat(to="ollama", model="llama3.2")

c.attach("test.pdf", page=0) # first page (0-indexed)

res = c.message("Describe this page from a PDF.")
```

### One page by visual rendering
If the PDF page contains complex formatting, you can render to an image to preserve it:
```py
c = chat(to="ollama", model="llama3.2-vision")

c.attach("test.pdf", page=0, as_image=True)

res = c.message("Extract the table as Markdown.")
```

# Parameters
## `chat(to, model, temperature?, num_ctx?) -> Chat`
#### `to: str`
- "ollama" for Ollama. Make sure to have models pulled in advance.
- ... only Ollama for now, but more can be added later.
#### `model: str`
- The model name to talk to. For example, "llama3.2" or "gpt-4o-mini"
#### `temperature?: float`
- An optional parameter to specify temperature. 0 is the most objective.
#### `num_ctx?: int`
- An optional parameter to specify the context window size as an integer.

## `attach(str, page?, as_image?) -> Chat`
The return value is the same Chat reference (so you can chain calls).
#### `filepath: str`
- A filepath to the file to attach. It is your responsibility to ensure it exists.
- Currently supported file extensions are:
    - Image formats: .jpg, .png
    - Textual formats: .txt, .csv, .json(l), .xml, .md
    - Other formats: .pdf
#### `page?: int`
- An optional parameter to specify page number (if applicable). Default is all pages.
#### `as_image?: bool`
- An optional parameter for rendering a PDF page as an image to attach.

## `message(message: str) -> str`
#### `message: str`

## `message_stream(message: str) -> Iterator[str]`
#### `message: str`

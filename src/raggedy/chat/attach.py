from PySide6.QtGui import QImage
from raggedy.document.document import Document
from raggedy.document.pdf.types import PDFParser
from raggedy.document.subclasses.textual import TextualDocument
from raggedy.document.subclasses.visual import VisualDocument
from raggedy.exceptions import UnsupportedDocumentException
from os.path import basename, exists

def _attach(filepath: str, page: int = -1, as_image: bool = False) -> Document:
	assert exists(filepath) and isinstance(page, int) and isinstance(as_image, bool)

	if filepath.lower().endswith(".pdf"):
		parser = PDFParser(filepath)
		if page == -1: # attach all pages
			all_texts: list[str] = []
			for i in range(parser.num_pages):
				all_texts.append(parser.page(i)._get_text().strip().replace("```","\\`\\`\\`"))

			combined = ""
			for i in range(1, len(all_texts) + 1):
				combined += f"<======================= Begin page {i} =======================>"
				combined += f"\n{all_texts[i - 1]}\n"
				combined += f"<======================== End page {i} ========================>\n\n"

			parser.close()
			return TextualDocument(
				basename(filepath),
				combined,
			)
		else:
			if as_image:
				doc = parser.page_as_image(page)
				parser.close()
				return doc
			else:
				doc = parser.page(page)
				parser.close()
				return doc

	if any(filepath.lower().endswith(i) for i in [
		".txt",
		".csv",
		".json",
		".jsonl",
		".xml",
		".md",
	]):
		with open(filepath, "r") as fin:
			text = fin.read()
			return TextualDocument(
				basename(filepath),
				text,
			)

	if any(filepath.lower().endswith(i) for i in [
		".jpg",
		".png",
	]):
		image = QImage(filepath)
		return VisualDocument(
			basename(filepath),
			image,
		)

	raise UnsupportedDocumentException
